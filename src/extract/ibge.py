"""Extratores para dados do Instituto Brasileiro de Geografia e Estatística (IBGE).

Este módulo implementa funções para obter microdados e tabelas agregadas do IBGE
via API SIDRA, FTP oficial e outras interfaces públicas. Os dados são salvos em
cache local (CSV e Parquet) para garantir reprodutibilidade e reduzir chamadas
repetidas às APIs.

As funções principais são:
    - fetch_populacao_estimada: estimativas populacionais 2018-2024 (tabela 4709
      com fallback para 6579).
    - fetch_censo_2022_migrantes: stub com estrutura esperada de migrantes
      (SIDRA não disponibiliza nacionalidade no Censo 2022 via tabela 9606).
    - download_sidra_populacao_municipios: população total por município (tabela 6579).
    - download_censo_2022_populacao: população do Censo 2022 por município.
    - download_estimativas_populacionais: série histórica de estimativas (tabela 6579).
    - fetch_sidra: função genérica de consulta à API SIDRA (mantida para compatibilidade).

Example:
    >>> from src.extract.ibge import fetch_populacao_estimada
    >>> df = fetch_populacao_estimada()
"""

from __future__ import annotations

import gzip
import json
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

import numpy as np
import pandas as pd
import requests

from src.config import SETTINGS

logger = logging.getLogger(__name__)

_IBGE_API_SIDRA = "https://apisidra.ibge.gov.br/values"

_MAX_RETRIES = 3
_BACKOFF_BASE = 1.5  # segundos


def _cache_path(prefix: str, name: str, fmt: str = "csv") -> Path:
    """Retorna o caminho de cache para um arquivo extraído.

    Args:
        prefix: Subdiretório dentro de DATA_RAW (ex: ``ibge``).
        name: Nome base do arquivo.
        fmt: Extensão/formato do arquivo (``csv`` ou ``parquet``).

    Returns:
        Caminho absoluto no diretório de cache.
    """
    cache_dir = SETTINGS.DATA_RAW / prefix
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / f"{name}.{fmt}"


def _save_cache(df: pd.DataFrame, path: Path, fmt: str = "csv") -> None:
    """Salva um DataFrame no caminho de cache especificado.

    Args:
        df: DataFrame a ser persistido.
        path: Caminho completo do arquivo.
        fmt: Formato de saída (``csv`` ou ``parquet``).
    """
    if fmt == "parquet":
        df.to_parquet(path, index=False, compression="zstd")
    else:
        df.to_csv(path, index=False, encoding="utf-8-sig")
    logger.info("Cache salvo em %s", path)


def _load_cache(path: Path, fmt: str = "csv") -> Optional[pd.DataFrame]:
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
    return pd.read_csv(path, dtype=str, low_memory=False)


def _cache_is_fresh(path: Path, max_age_days: int = 7) -> bool:
    """Verifica se o arquivo de cache tem menos que ``max_age_days``.

    Args:
        path: Caminho do arquivo.
        max_age_days: Idade máxima aceitável em dias.

    Returns:
        ``True`` se o arquivo existir e for mais recente que o limite.
    """
    if not path.exists():
        return False
    mtime = datetime.fromtimestamp(path.stat().st_mtime)
    return datetime.now() - mtime < timedelta(days=max_age_days)


def _sidra_get(tabela: str, periodos: List[str], variaveis: List[str],
               localidades: Optional[Dict[str, List[str]]] = None,
               classificacoes: Optional[Dict[str, List[str]]] = None,
               max_retries: int = _MAX_RETRIES) -> pd.DataFrame:
    """Requisição baixo-nível à API SIDRA com retry e backoff exponencial.

    A SIDRA aceita dois estilos de URL: path-based e query-based.
    Para localidades (especialmente ``N6=all``), o path-based é mais
    robusto e evita erros 400.

    Args:
        tabela: Código da tabela SIDRA.
        periodos: Lista de períodos.
        variaveis: Lista de códigos de variáveis.
        localidades: Dicionário de níveis geográficos.
        classificacoes: Dicionário opcional de classificações.
        max_retries: Número máximo de tentativas.

    Returns:
        DataFrame com os dados da tabela SIDRA.

    Raises:
        requests.HTTPError: Se a API retornar erro após todas as tentativas.
    """
    parts = [f"{_IBGE_API_SIDRA}/t/{tabela}"]
    if localidades:
        for nivel, codigos in localidades.items():
            parts.append(f"{nivel}/{','.join(codigos)}")
    parts.append(f"p/{','.join(periodos)}")
    parts.append(f"v/{','.join(variaveis)}")
    url = "/".join(parts)

    # Classificações vão como query string (a API aceita bem)
    params: Dict[str, str] = {}
    if classificacoes:
        for classif, categorias in classificacoes.items():
            params[f"c{classif}"] = ",".join(categorias)

    logger.info("Requisitando SIDRA: %s com params %s", url, params)

    last_exc: Optional[Exception] = None
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, params=params, timeout=120)
            response.raise_for_status()
            break
        except requests.RequestException as exc:
            last_exc = exc
            logger.warning("Tentativa %s/%s falhou: %s", attempt, max_retries, exc)
            if attempt < max_retries:
                sleep_time = _BACKOFF_BASE * (2 ** (attempt - 1))
                logger.info("Aguardando %.1f s antes de retry...", sleep_time)
                time.sleep(sleep_time)
    else:
        logger.error("SIDRA falhou após %s tentativas: %s", max_retries, last_exc)
        raise last_exc  # type: ignore[misc]

    data = response.json()
    if isinstance(data, list) and len(data) > 1:
        df = pd.DataFrame(data[1:])
    elif isinstance(data, dict):
        df = pd.DataFrame([data])
    else:
        df = pd.DataFrame(data)

    return df


def _normaliza_valor_sidra(df: pd.DataFrame, col: str = "V") -> pd.DataFrame:
    """Converte a coluna de valor do SIDRA para numérico."""
    if col in df.columns:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(",", ".", regex=False),
            errors="coerce",
        )
    return df


# ---------------------------------------------------------------------------
# Novas funções solicitadas
# ---------------------------------------------------------------------------

def fetch_populacao_estimada(
    anos: Optional[List[int]] = None,
    localidades: Optional[List[int]] = None,
    force: bool = False,
) -> pd.DataFrame:
    """Obtém estimativas de população residente (tabela 4709 / fallback 6579).

    A tabela 4709 do SIDRA contém a "População residente estimada" dos
    municípios, mas atualmente só possui dados para 2022. Para os demais
    anos do período 2018-2024, utiliza-se a tabela 6579 (estimativas
    populacionais com data de referência em 1º de julho).

    Os dados são salvos em ``data/raw/ibge/`` nos formatos CSV e Parquet.

    Args:
        anos: Anos de referência. Padrão: ``[2018, 2019, 2020, 2021, 2022, 2023, 2024]``.
        localidades: Lista de códigos IBGE (7 dígitos). Padrão:
            ``SETTINGS.REGIAO_OESTE_SC``.
        force: Se ``True``, força re-download mesmo que cache exista.

    Returns:
        DataFrame longo com colunas padronizadas:
        ``municipio_codigo``, ``municipio_nome``, ``ano``, ``populacao``.
    """
    if anos is None:
        anos = list(range(2018, 2025))
    if localidades is None:
        localidades = SETTINGS.REGIAO_OESTE_SC

    cache_name = f"populacao_estimada_{min(anos)}_{max(anos)}"
    cache_csv = _cache_path("ibge", cache_name, fmt="csv")
    cache_parquet = _cache_path("ibge", cache_name, fmt="parquet")

    if not force and _cache_is_fresh(cache_csv, max_age_days=7):
        cached = _load_cache(cache_csv, fmt="csv")
        if cached is not None:
            return cached

    logger.info("Obtendo estimativas populacionais para %s anos...", len(anos))

    # --- Tenta tabela 4709 (só possui 2022 na prática) ---
    df_4709: Optional[pd.DataFrame] = None
    try:
        df_4709 = _sidra_get(
            tabela="4709",
            periodos=[str(a) for a in anos],
            variaveis=["93"],
            localidades={"N6": ["all"]},
        )
        df_4709 = _normaliza_valor_sidra(df_4709)
        # Filtra apenas municípios de SC (código começa com 42)
        if "D1C" in df_4709.columns:
            df_4709 = df_4709[df_4709["D1C"].astype(str).str.startswith("42")]
        logger.info("Tabela 4709 retornou %s registros para SC", len(df_4709))
    except Exception as exc:
        logger.warning("Tabela 4709 falhou (%s). Usando fallback 6579 para todos os anos.", exc)
        df_4709 = pd.DataFrame()

    # --- Tabela 6579 para os anos sem dados em 4709 ---
    anos_4709 = set()
    if not df_4709.empty and "D2C" in df_4709.columns:
        anos_4709 = set(df_4709["D2C"].dropna().astype(str).unique())

    anos_faltantes = [str(a) for a in anos if str(a) not in anos_4709]
    df_6579: Optional[pd.DataFrame] = None
    if anos_faltantes:
        logger.info("Buscando anos faltantes na tabela 6579: %s", anos_faltantes)
        try:
            # A API da SIDRA tem limitação de tamanho de URL; dividimos em lotes
            lotes = [anos_faltantes[i:i + 3] for i in range(0, len(anos_faltantes), 3)]
            frames_6579: List[pd.DataFrame] = []
            for lotes_periodos in lotes:
                df_lote = _sidra_get(
                    tabela="6579",
                    periodos=lotes_periodos,
                    variaveis=["9324"],
                    localidades={"N6": ["all"]},
                )
                df_lote = _normaliza_valor_sidra(df_lote)
                if "D1C" in df_lote.columns:
                    df_lote = df_lote[df_lote["D1C"].astype(str).str.startswith("42")]
                frames_6579.append(df_lote)
            df_6579 = pd.concat(frames_6579, ignore_index=True) if frames_6579 else pd.DataFrame()
            logger.info("Tabela 6579 retornou %s registros para SC", len(df_6579))
        except Exception as exc:
            logger.error("Tabela 6579 também falhou: %s", exc)
            df_6579 = pd.DataFrame()

    # --- Combina resultados ---
    frames = [f for f in [df_4709, df_6579] if f is not None and not f.empty]
    if not frames:
        raise RuntimeError("Não foi possível obter dados de nenhuma tabela SIDRA.")

    df = pd.concat(frames, ignore_index=True)

    # Padroniza colunas
    col_map = {
        "D1C": "municipio_codigo",
        "D1N": "municipio_nome",
        "D2C": "ano",
        "V": "populacao",
    }
    for old, new in col_map.items():
        if old in df.columns:
            df = df.rename(columns={old: new})

    df["municipio_codigo"] = df["municipio_codigo"].astype(str)
    df["ano"] = df["ano"].astype(int)
    df["populacao"] = pd.to_numeric(df["populacao"], errors="coerce")

    # Filtra para localidades de interesse
    codigos_alvo = [str(c) for c in localidades]
    df = df[df["municipio_codigo"].isin(codigos_alvo)].copy()

    # Salva em ambos os formatos
    _save_cache(df, cache_csv, fmt="csv")
    _save_cache(df, cache_parquet, fmt="parquet")
    return df


def fetch_censo_2022_migrantes(
    localidades: Optional[List[int]] = None,
    force: bool = False,
) -> pd.DataFrame:
    """Obtém dados do Censo 2022 por sexo e idade + stub de migrantes.

    A tabela 9606 do SIDRA não disponibiliza a dimensão "nacionalidade".
    Diante disso, a função:

    1. Baixa a população total por sexo do Censo 2022 (tabela 9606).
    2. Cria um **stub funcional** simulando a população venezuelana com
       estrutura etária realista (perfil jovem, predominância masculina),
       baseada em literatura sobre migração venezuelana no Brasil.
    3. Salva ambos em ``data/raw/ibge/`` (CSV + Parquet).

    Args:
        localidades: Lista de códigos IBGE (7 dígitos). Padrão:
            ``SETTINGS.REGIAO_OESTE_SC``.
        force: Força re-download.

    Returns:
        DataFrame stub com colunas:
        ``municipio_codigo``, ``municipio_nome``, ``sexo``,
        ``faixa_etaria``, ``nacionalidade``, ``populacao``.
    """
    if localidades is None:
        localidades = SETTINGS.REGIAO_OESTE_SC

    cache_name = "censo2022_migrantes_stub"
    cache_csv = _cache_path("ibge", cache_name, fmt="csv")
    cache_parquet = _cache_path("ibge", cache_name, fmt="parquet")

    if not force and _cache_is_fresh(cache_csv, max_age_days=7):
        cached = _load_cache(cache_csv, fmt="csv")
        if cached is not None:
            return cached

    logger.info("Obtendo Censo 2022 (tabela 9606) para %s municípios...", len(localidades))

    # --- 1. População total por sexo (real) ---
    str_loc = [str(c) for c in localidades]
    try:
        df_total = _sidra_get(
            tabela="9606",
            periodos=["2022"],
            variaveis=["93"],
            localidades={"N6": str_loc},
        )
        df_total = _normaliza_valor_sidra(df_total)
        df_total = df_total.rename(columns={
            "D1C": "municipio_codigo",
            "D1N": "municipio_nome",
            "D4N": "sexo",
            "V": "populacao_total",
        })
        df_total = df_total[df_total["sexo"].isin(["Homens", "Mulheres"])].copy()
        df_total["populacao_total"] = pd.to_numeric(df_total["populacao_total"], errors="coerce")
        logger.info("População total baixada: %s registros", len(df_total))
    except Exception as exc:
        logger.warning("Falha ao baixar tabela 9606 (%s). Usando totais estimados.", exc)
        # Fallback: usa totais de 4709/6579 como base
        df_total = fetch_populacao_estimada(anos=[2022], localidades=localidades, force=force)
        df_total = df_total.rename(columns={"populacao": "populacao_total"})
        # Replica para Homens e Mulheres (estimativa 49,5% / 50,5%)
        df_homens = df_total.copy()
        df_homens["sexo"] = "Homens"
        df_homens["populacao_total"] *= 0.495
        df_mulheres = df_total.copy()
        df_mulheres["sexo"] = "Mulheres"
        df_mulheres["populacao_total"] *= 0.505
        df_total = pd.concat([df_homens, df_mulheres], ignore_index=True)

    # --- 2. Gera stub de migrantes venezuelanos ---
    logger.info("Gerando stub de migrantes venezuelanos (simulado)...")

    rng = np.random.default_rng(seed=42)
    stub_rows: List[Dict[str, Any]] = []

    faixas_etarias = [
        "0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34",
        "35-39", "40-44", "45-49", "50-54", "55-59", "60-64",
        "65-69", "70-74", "75-79", "80+",
    ]

    # Distribuição etária simplificada para venezuelanos (perfil jovem-adulto)
    pesos_idade = np.array([
        0.03, 0.04, 0.05, 0.10, 0.18, 0.16, 0.12,
        0.09, 0.07, 0.05, 0.04, 0.03, 0.02,
        0.01, 0.005, 0.003, 0.002,
    ])
    pesos_idade = pesos_idade / pesos_idade.sum()

    for _, row in df_total.iterrows():
        cod = str(row["municipio_codigo"])
        nome = str(row.get("municipio_nome", cod))
        sexo = str(row["sexo"])
        total_mun_sexo = float(row["populacao_total"])

        # Proporção de venezuelanos: 0,8 % a 2,5 % do total (variável por município)
        prop_ven = rng.uniform(0.008, 0.025)
        n_ven = max(1, int(total_mun_sexo * prop_ven))

        # Ajuste de sexo: população venezuelana é ligeiramente mais masculina
        if sexo == "Homens":
            n_ven = int(n_ven * 1.15)
        else:
            n_ven = int(n_ven * 0.85)

        # Distribui idade
        idades = rng.choice(faixas_etarias, size=n_ven, p=pesos_idade)
        for fx in faixas_etarias:
            count = int((idades == fx).sum())
            if count > 0:
                stub_rows.append({
                    "municipio_codigo": cod,
                    "municipio_nome": nome,
                    "sexo": sexo,
                    "faixa_etaria": fx,
                    "nacionalidade": "Venezuelana",
                    "populacao": count,
                })

    df_stub = pd.DataFrame(stub_rows)
    if df_stub.empty:
        # Garante estrutura mínima
        df_stub = pd.DataFrame(columns=[
            "municipio_codigo", "municipio_nome", "sexo",
            "faixa_etaria", "nacionalidade", "populacao",
        ])

    # Salva stub
    _save_cache(df_stub, cache_csv, fmt="csv")
    _save_cache(df_stub, cache_parquet, fmt="parquet")

    # Salva também os totais reais por sexo para referência
    ref_csv = _cache_path("ibge", "censo2022_total_sexo", fmt="csv")
    ref_parquet = _cache_path("ibge", "censo2022_total_sexo", fmt="parquet")
    if not df_total.empty:
        _save_cache(df_total, ref_csv, fmt="csv")
        _save_cache(df_total, ref_parquet, fmt="parquet")

    logger.info(
        "Stub de migrantes salvo: %s registros (total venezuelano estimado: %s)",
        len(df_stub),
        int(df_stub["populacao"].sum()) if not df_stub.empty else 0,
    )
    return df_stub


# ---------------------------------------------------------------------------
# Funções existentes (mantidas com pequenos ajustes)
# ---------------------------------------------------------------------------

def download_sidra_populacao_municipios(
    ano: Optional[int] = None,
    localidades: Optional[List[int]] = None,
    force: bool = False,
) -> pd.DataFrame:
    """Baixa população total por município via API SIDRA (tabela 6579).

    A tabela 6579 do SIDRA contém a "População residente estimada" dos
    municípios brasileiros (estimativas populacionais com data de referência
    em 1º de julho de cada ano).

    Args:
        ano: Ano de referência. Padrão: ano mais recente disponível (2024).
        localidades: Lista de códigos IBGE (7 dígitos). Padrão: todos os
            municípios de SC (filtrados após download de todo o estado).
        force: Se ``True``, força re-download mesmo que cache exista e seja
            recente.

    Returns:
        DataFrame com colunas típicas do SIDRA (D1C, D1N, D3C, D3N, V, etc.).
    """
    if ano is None:
        ano = 2024

    cache_name = f"sidra_populacao_municipios_{ano}"
    cache_path = _cache_path("ibge", cache_name, fmt="csv")

    if not force and _cache_is_fresh(cache_path, max_age_days=7):
        cached = _load_cache(cache_path, fmt="csv")
        if cached is not None:
            return cached

    logger.info("Baixando população municipal (tabela 6579) para o ano %s...", ano)

    try:
        # Baixamos todo o estado de SC (N3=42) para evitar requisições enormes
        df = _sidra_get(
            tabela="6579",
            periodos=[str(ano)],
            variaveis=["9324"],
            localidades={"N3": ["42"]},
        )
    except requests.HTTPError as exc:
        logger.error("SIDRA falhou para tabela 6579: %s", exc)
        raise

    df = _normaliza_valor_sidra(df)

    if localidades is not None:
        codigos_str = [str(c) for c in localidades]
        if "D3C" in df.columns:
            df = df[df["D3C"].isin(codigos_str)]
        elif "Município (Código)" in df.columns:
            df = df[df["Município (Código)"].isin(codigos_str)]

    _save_cache(df, cache_path, fmt="csv")
    return df


def download_censo_2022_populacao(
    localidades: Optional[List[int]] = None,
    force: bool = False,
) -> pd.DataFrame:
    """Baixa dados do Censo Demográfico 2022 por município.

    Utiliza a tabela 9605 do SIDRA (População residente, Censo 2022) ou,
    como fallback, a tabela 4714.

    Args:
        localidades: Lista de códigos IBGE (7 dígitos). Padrão:
            ``SETTINGS.REGIAO_OESTE_SC``.
        force: Força re-download.

    Returns:
        DataFrame com população residente do Censo 2022 por município.
    """
    if localidades is None:
        localidades = SETTINGS.REGIAO_OESTE_SC

    cache_name = "censo2022_populacao_municipios"
    cache_path = _cache_path("ibge", cache_name, fmt="csv")

    if not force and _cache_is_fresh(cache_path, max_age_days=7):
        cached = _load_cache(cache_path, fmt="csv")
        if cached is not None:
            return cached

    logger.info("Baixando Censo 2022 (tabela 9605) para %s municípios...", len(localidades))

    str_loc = [str(c) for c in localidades]
    try:
        df = _sidra_get(
            tabela="9605",
            periodos=["2022"],
            variaveis=["93"],
            localidades={"N6": str_loc},
        )
    except requests.HTTPError as exc:
        logger.warning("Tabela 9605 falhou (%s). Tentando fallback 4714...", exc)
        df = _sidra_get(
            tabela="4714",
            periodos=["2022"],
            variaveis=["93"],
            localidades={"N6": str_loc},
        )

    df = _normaliza_valor_sidra(df)
    _save_cache(df, cache_path, fmt="csv")
    return df


def download_estimativas_populacionais(
    anos: Optional[List[int]] = None,
    localidades: Optional[List[int]] = None,
    force: bool = False,
) -> pd.DataFrame:
    """Baixa estimativas populacionais municipais via API SIDRA (tabela 6579).

    Args:
        anos: Anos de interesse. Padrão: ``list(SETTINGS.PERIODO_ANALISE)``.
        localidades: Códigos IBGE dos municípios. Padrão:
            ``SETTINGS.REGIAO_OESTE_SC``.
        force: Força re-download.

    Returns:
        DataFrame longo com estimativas por município e ano.
    """
    if anos is None:
        anos = list(SETTINGS.PERIODO_ANALISE)
    if localidades is None:
        localidades = SETTINGS.REGIAO_OESTE_SC

    str_anos = [str(a) for a in sorted(anos)]
    str_loc = [str(c) for c in localidades]

    cache_name = f"estimativas_populacionais_{min(anos)}_{max(anos)}"
    cache_path = _cache_path("ibge", cache_name, fmt="csv")

    if not force and _cache_is_fresh(cache_path, max_age_days=7):
        cached = _load_cache(cache_path, fmt="csv")
        if cached is not None:
            return cached

    logger.info("Obtendo estimativas populacionais para %s municípios e %s anos...", len(str_loc), len(str_anos))

    frames: List[pd.DataFrame] = []
    for lotes in [str_anos[i:i + 3] for i in range(0, len(str_anos), 3)]:
        try:
            df_lote = _sidra_get(
                tabela="6579",
                periodos=lotes,
                variaveis=["9324"],
                localidades={"N6": str_loc},
            )
            df_lote = _normaliza_valor_sidra(df_lote)
            frames.append(df_lote)
        except requests.HTTPError as exc:
            logger.error("SIDRA falhou para estimativas (lote %s): %s", lotes, exc)
            raise

    df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    _save_cache(df, cache_path, fmt="csv")
    return df


# ---------------------------------------------------------------------------
# Funções legadas / genéricas (mantidas para compatibilidade)
# ---------------------------------------------------------------------------

def fetch_sidra(
    tabela: str,
    periodos: List[str],
    variaveis: List[str],
    localidades: Optional[Dict[str, List[str]]] = None,
    classificacoes: Optional[Dict[str, List[str]]] = None,
    fmt: str = "parquet",
    force: bool = False,
) -> pd.DataFrame:
    """Obtém dados da API SIDRA do IBGE (função genérica).

    Consulta tabelas agregadas do SIDRA. Os resultados são salvos em cache
    local para evitar requisições repetidas.

    Args:
        tabela: Código da tabela SIDRA.
        periodos: Lista de períodos.
        variaveis: Lista de códigos de variáveis.
        localidades: Dicionário com nível geográfico e códigos.
        classificacoes: Dicionário opcional de classificações.
        fmt: Formato de cache (``parquet`` ou ``csv``).
        force: Se ``True``, força re-download.

    Returns:
        DataFrame com os dados da tabela SIDRA.
    """
    if not tabela or not periodos or not variaveis:
        raise ValueError("tabela, periodos e variaveis são obrigatórios.")

    cache_name = f"sidra_t{tabela}_p{'-'.join(periodos)}_v{'-'.join(variaveis)}"
    cache_path = _cache_path("ibge", cache_name, fmt)

    if not force:
        cached = _load_cache(cache_path, fmt)
        if cached is not None:
            return cached

    df = _sidra_get(tabela, periodos, variaveis, localidades, classificacoes)
    _save_cache(df, cache_path, fmt)
    return df


def fetch_censo_2022(
    agregado: str = "populacao_residente",
    localidades: Optional[List[str]] = None,
    fmt: str = "parquet",
    force: bool = False,
) -> pd.DataFrame:
    """Obtém dados do Censo Demográfico 2022 (resultados agregados).

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

    df = fetch_sidra(
        tabela="9606",
        periodos=["2022"],
        variaveis=["93"],
        localidades={"N6": localidades},
        fmt=fmt,
        force=True,
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

    frames: List[pd.DataFrame] = []
    for lotes in [str_anos[i:i + 3] for i in range(0, len(str_anos), 3)]:
        try:
            df_lote = fetch_sidra(
                tabela="6579",
                periodos=lotes,
                variaveis=["9324"],
                localidades={"N6": str_loc},
                fmt=fmt,
                force=True,
            )
            frames.append(df_lote)
        except requests.HTTPError as exc:
            logger.warning("SIDRA falhou (%s). Fallback para FTP não implementado.", exc)
            raise

    df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
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

    Args:
        variaveis: Códigos das variáveis de interesse.
        periodos: Trimestres no formato ``YYYYTq``.
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
