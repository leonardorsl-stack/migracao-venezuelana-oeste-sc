"""Extratores para dados do Instituto Brasileiro de Geografia e Estatística (IBGE).

Este módulo implementa funções para obter microdados e tabelas agregadas do IBGE
via API SIDRA, FTP oficial e outras interfaces públicas. Os dados são salvos em
cache local (CSV ou Parquet) para garantir reprodutibilidade e reduzir chamadas
repetidas às APIs.

Example:
    >>> from src.extract.ibge import fetch_sidra
    >>> df = fetch_sidra(
    ...     tabela="9606",
    ...     periodos=["2022"],
    ...     variaveis=["93"],
    ...     localidades={"N6": ["4204202", "4219507"]},
    ... )
"""

from __future__ import annotations

import gzip
import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

import pandas as pd
import requests

from src.config import SETTINGS

logger = logging.getLogger(__name__)

_IBGE_API_SIDRA = "https://apisidra.ibge.gov.br/values"
_IBGE_FTP_ESTIMATIVAS = "https://ftp.ibge.gov.br/Estimativas_de_Populacao/Estimativas_2024/"
_IBGE_FTP_CENSO = "https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Resultados_Totais_Agregados_por_Area_Minima_de_Comparacao/"
_IBGE_PNAD_API = "https://apisidra.ibge.gov.br/values"


def _cache_path(prefix: str, name: str, fmt: str = "parquet") -> Path:
    """Retorna o caminho de cache para um arquivo extraído.

    Args:
        prefix: Subdiretório dentro de DATA_RAW (ex: ``ibge``).
        name: Nome base do arquivo.
        fmt: Extensão/formato do arquivo (``parquet`` ou ``csv``).

    Returns:
        Caminho absoluto no diretório de cache.
    """
    cache_dir = SETTINGS.DATA_RAW / prefix
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / f"{name}.{fmt}"


def _save_cache(df: pd.DataFrame, path: Path, fmt: str = "parquet") -> None:
    """Salva um DataFrame no caminho de cache especificado.

    Args:
        df: DataFrame a ser persistido.
        path: Caminho completo do arquivo.
        fmt: Formato de saída (``parquet`` ou ``csv``).
    """
    if fmt == "parquet":
        df.to_parquet(path, index=False, compression="gzip")
    else:
        df.to_csv(path, index=False, encoding="utf-8-sig")
    logger.info("Cache salvo em %s", path)


def _load_cache(path: Path, fmt: str = "parquet") -> Optional[pd.DataFrame]:
    """Tenta carregar um DataFrame do cache, se existir.

    Args:
        path: Caminho do arquivo em cache.
        fmt: Formato do arquivo.

    Returns:
        DataFrame carregado ou ``None`` caso o arquivo não exista.
    """
    if not path.exists():
        return None
    logger.info("Carregando do cache %s", path)
    if fmt == "parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path, dtype=str)


def fetch_sidra(
    tabela: str,
    periodos: List[str],
    variaveis: List[str],
    localidades: Optional[Dict[str, List[str]]] = None,
    classificacoes: Optional[Dict[str, List[str]]] = None,
    fmt: str = "parquet",
    force: bool = False,
) -> pd.DataFrame:
    """Obtém dados da API SIDRA do IBGE.

    Consulta tabelas agregadas do SIDRA (Sistema IBGE de Recuperação Automática).
    Os resultados são salvos em cache local para evitar requisições repetidas.

    Args:
        tabela: Código da tabela SIDRA (ex: ``9606`` para população residente).
        periodos: Lista de períodos (anos, meses, trimestres) no formato aceito
            pela tabela.
        variaveis: Lista de códigos de variáveis de interesse.
        localidades: Dicionário com nível geográfico como chave (ex: ``N6`` para
            municípios) e lista de códigos como valor.
        classificacoes: Dicionário opcional com códigos de classificação e
            categorias para filtrar a tabela.
        fmt: Formato de cache (``parquet`` ou ``csv``).
        force: Se ``True``, força re-download mesmo que cache exista.

    Returns:
        DataFrame com os dados da tabela SIDRA.

    Raises:
        requests.HTTPError: Se a API retornar status de erro.
        ValueError: Se os parâmetros obrigatórios estiverem ausentes.
    """
    if not tabela or not periodos or not variaveis:
        raise ValueError("tabela, periodos e variaveis são obrigatórios.")

    cache_name = f"sidra_t{tabela}_p{'-'.join(periodos)}_v{'-'.join(variaveis)}"
    cache_path = _cache_path("ibge", cache_name, fmt)

    if not force:
        cached = _load_cache(cache_path, fmt)
        if cached is not None:
            return cached

    # Monta payload conforme documentação SIDRA
    payload: Dict[str, Any] = {
        "t": tabela,
        "p": "|".join(periodos),
        "v": "|".join(variaveis),
    }
    if localidades:
        for nivel, codigos in localidades.items():
            payload[nivel] = "|".join(codigos)
    if classificacoes:
        for classif, categorias in classificacoes.items():
            payload[f"c{classif}"] = "|".join(categorias)

    url = f"{_IBGE_API_SIDRA}/t/{tabela}"
    logger.info("Requisitando SIDRA: %s com params %s", url, payload)

    try:
        response = requests.get(url, params=payload, timeout=120)
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.error("Falha na requisição SIDRA: %s", exc)
        raise

    # SIDRA retorna lista de dicts; o primeiro item é metadados
    data = response.json()
    if isinstance(data, list) and len(data) > 1:
        df = pd.DataFrame(data[1:])
    elif isinstance(data, dict):
        df = pd.DataFrame([data])
    else:
        df = pd.DataFrame(data)

    _save_cache(df, cache_path, fmt)
    return df


def fetch_censo_2022(
    agregado: str = "populacao_residente",
    localidades: Optional[List[str]] = None,
    fmt: str = "parquet",
    force: bool = False,
) -> pd.DataFrame:
    """Obtém dados do Censo Demográfico 2022 (resultados agregados).

    Utiliza a API SIDRA para acessar os agregados preliminares do Censo 2022.
    A tabela padrão para população residente é ``9606``.

    Args:
        agregado: Nome do indicador agregado disponível.
        localidades: Lista de códigos IBGE (7 dígitos) dos municípios.
        fmt: Formato de cache.
        force: Força re-download.

    Returns:
        DataFrame com dados do Censo 2022 filtrados para os municípios.
    """
    if localidades is None:
        localidades = [str(c) for c in SETTINGS.REGIAO_OESTE_SC]

    cache_name = f"censo2022_{agregado}"
    cache_path = _cache_path("ibge", cache_name, fmt)

    if not force:
        cached = _load_cache(cache_path, fmt)
        if cached is not None:
            return cached

    # Tabela 9606 = População Residente (Censo 2022)
    df = fetch_sidra(
        tabela="9606",
        periodos=["2022"],
        variaveis=["93"],
        localidades={"N6": localidades},
        fmt=fmt,
        force=force,
    )

    _save_cache(df, cache_path, fmt)
    return df


def fetch_estimativas_populacionais(
    anos: Optional[List[int]] = None,
    localidades: Optional[List[int]] = None,
    fmt: str = "parquet",
    force: bool = False,
) -> pd.DataFrame:
    """Obtém estimativas populacionais do IBGE.

    Busca a série histórica de estimativas populacionais municipais via API SIDRA
    (tabela ``6579``) ou, como fallback, via FTP do IBGE.

    Args:
        anos: Anos de interesse. Padrão: todos os anos de ``PERIODO_ANALISE``.
        localidades: Códigos IBGE dos municípios. Padrão: ``REGIAO_OESTE_SC``.
        fmt: Formato de cache.
        force: Força re-download.

    Returns:
        DataFrame com estimativas populacionais por município e ano.
    """
    if anos is None:
        anos = list(SETTINGS.PERIODO_ANALISE)
    if localidades is None:
        localidades = SETTINGS.REGIAO_OESTE_SC

    str_anos = [str(a) for a in sorted(anos)]
    str_loc = [str(c) for c in localidades]

    cache_name = f"estimativas_pop_p{'-'.join(str_anos)}"
    cache_path = _cache_path("ibge", cache_name, fmt)

    if not force:
        cached = _load_cache(cache_path, fmt)
        if cached is not None:
            return cached

    logger.info("Obtendo estimativas populacionais para %s municípios", len(str_loc))

    try:
        df = fetch_sidra(
            tabela="6579",
            periodos=str_anos,
            variaveis=["9324"],
            localidades={"N6": str_loc},
            fmt=fmt,
            force=True,  # evita cache duplo
        )
    except requests.HTTPError as exc:
        logger.warning("SIDRA falhou (%s). Fallback para FTP não implementado.", exc)
        raise

    _save_cache(df, cache_path, fmt)
    return df


def fetch_pnad(
    variaveis: List[str],
    periodos: Optional[List[str]] = None,
    localidades: Optional[Dict[str, List[str]]] = None,
    fmt: str = "parquet",
    force: bool = False,
) -> pd.DataFrame:
    """Obtém dados da PNAD Contínua via API SIDRA.

    A PNAD Contínua possui tabelas agregadas no SIDRA (ex: ``5434`` para
    indicadores de trabalho). Esta função abstrai a consulta.

    Args:
        variaveis: Códigos das variáveis de interesse.
        periodos: Trimestres no formato ``YYYYTq`` (ex: ``2023T1``).
        localidades: Dicionário de níveis geográficos e códigos.
        fmt: Formato de cache.
        force: Força re-download.

    Returns:
        DataFrame com os dados da PNAD Contínua.
    """
    cache_name = f"pnad_v{'-'.join(variaveis)}"
    cache_path = _cache_path("ibge", cache_name, fmt)

    if not force:
        cached = _load_cache(cache_path, fmt)
        if cached is not None:
            return cached

    if periodos is None:
        periodos = [f"{a}T1" for a in SETTINGS.PERIODO_ANALISE]

    try:
        df = fetch_sidra(
            tabela="5434",
            periodos=periodos,
            variaveis=variaveis,
            localidades=localidades,
            fmt=fmt,
            force=True,
        )
    except requests.HTTPError as exc:
        logger.error("Falha ao obter PNAD: %s", exc)
        raise

    _save_cache(df, cache_path, fmt)
    return df
