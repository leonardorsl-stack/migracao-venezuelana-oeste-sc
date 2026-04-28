"""Extratores para dados do DataSUS via PySUS.

Este módulo encapsula o download de bases do Sistema Único de Saúde (SUS)
utilizando a biblioteca ``pysus``. Os dados brutos são persistidos em
``data/raw/datasus/`` para posterior transformação.

As bases suportadas incluem:
    - SIM (Sistema de Informação sobre Mortalidade)
    - SINASC (Sistema de Informação sobre Nascidos Vivos)
    - AIH (Autorização de Internação Hospitalar – SIH/SUS)
    - BPA (Boletim de Produção Ambulatorial – SIA/SUS)
    - SIPNI (Sistema de Informação do Programa Nacional de Imunizações)

Note:
    A biblioteca ``pysus`` deve estar instalada no ambiente. Em alguns casos
    é necessário aceitar os termos de uso do DataSUS no primeiro download.

Example:
    >>> from src.extract.datasus import download_sim
    >>> df = download_sim(ano=2022, estado="SC")
"""

from __future__ import annotations

import logging
import warnings
from pathlib import Path
from typing import List, Optional, Union

import pandas as pd

from src.config import SETTINGS

logger = logging.getLogger(__name__)

# Tenta importar pysus; caso contrário, funcionam como stubs com aviso
try:
    from pysus.online_data import SIM, SINASC, SIH, SIA, PNI
    _PYSUS_AVAILABLE = True
except ImportError:  # pragma: no cover
    warnings.warn(
        "Biblioteca 'pysus' não encontrada. "
        "As funções de extract/datasus funcionarão como stubs.",
        stacklevel=2,
    )
    SIM = SINASC = SIH = SIA = PNI = None  # type: ignore[assignment]
    _PYSUS_AVAILABLE = False


def _datasus_cache_dir(subdir: str) -> Path:
    """Retorna o diretório de cache para uma sub-base do DataSUS.

    Args:
        subdir: Nome da base (ex: ``sim``, ``sinasc``).

    Returns:
        Path do diretório, criando-o se necessário.
    """
    path = SETTINGS.DATA_RAW / "datasus" / subdir
    path.mkdir(parents=True, exist_ok=True)
    return path


def _save_raw(df: pd.DataFrame, path: Path) -> Path:
    """Salva DataFrame bruto em Parquet comprimido.

    Args:
        df: Dados brutos extraídos.
        path: Caminho do arquivo de destino.

    Returns:
        Caminho do arquivo salvo.
    """
    df.to_parquet(path, index=False, compression="gzip")
    logger.info("Raw DataSUS salvo em %s", path)
    return path


def download_sim(
    ano: Union[int, List[int]],
    estado: str = "SC",
    force: bool = False,
) -> pd.DataFrame:
    """Download dos dados do SIM (Mortalidade) via PySUS.

    Args:
        ano: Ano ou lista de anos de interesse.
        estado: Sigla UF (padrão ``SC``).
        force: Se ``True``, sobrescreve arquivo existente.

    Returns:
        DataFrame com microdados do SIM.

    Raises:
        RuntimeError: Se o PySUS não estiver disponível.
        ValueError: Se ``ano`` estiver fora do intervalo suportado.
    """
    if not _PYSUS_AVAILABLE:
        raise RuntimeError("PySUS não está instalado. Instale com: pip install pysus")

    anos: List[int] = [ano] if isinstance(ano, int) else ano
    cache_dir = _datasus_cache_dir("sim")
    frames: List[pd.DataFrame] = []

    for a in anos:
        if a < 1996 or a > 2024:
            logger.warning("Ano %s pode não estar disponível no SIM.", a)

        file_path = cache_dir / f"SIM_{estado}_{a}.parquet.gz"
        if file_path.exists() and not force:
            logger.info("Carregando SIM %s do cache.", a)
            frames.append(pd.read_parquet(file_path))
            continue

        logger.info("Baixando SIM %s/%s...", estado, a)
        try:
            # API PySUS pode variar conforme versão; esta chamada é representativa
            df = SIM.download(groups=["CIDBR10"], states=[estado], years=[a])
        except Exception as exc:  # pragma: no cover
            logger.error("Erro no download SIM %s: %s", a, exc)
            raise

        _save_raw(df, file_path)
        frames.append(df)

    return pd.concat(frames, ignore_index=True) if len(frames) > 1 else frames[0]


def download_sinasc(
    ano: Union[int, List[int]],
    estado: str = "SC",
    force: bool = False,
) -> pd.DataFrame:
    """Download dos dados do SINASC (Nascidos Vivos) via PySUS.

    Args:
        ano: Ano ou lista de anos.
        estado: Sigla UF (padrão ``SC``).
        force: Sobrescreve cache existente.

    Returns:
        DataFrame com microdados do SINASC.
    """
    if not _PYSUS_AVAILABLE:
        raise RuntimeError("PySUS não está instalado.")

    anos: List[int] = [ano] if isinstance(ano, int) else ano
    cache_dir = _datasus_cache_dir("sinasc")
    frames: List[pd.DataFrame] = []

    for a in anos:
        file_path = cache_dir / f"SINASC_{estado}_{a}.parquet.gz"
        if file_path.exists() and not force:
            frames.append(pd.read_parquet(file_path))
            continue

        logger.info("Baixando SINASC %s/%s...", estado, a)
        try:
            df = SINASC.download(states=[estado], years=[a])
        except Exception as exc:  # pragma: no cover
            logger.error("Erro no download SINASC %s: %s", a, exc)
            raise

        _save_raw(df, file_path)
        frames.append(df)

    return pd.concat(frames, ignore_index=True) if len(frames) > 1 else frames[0]


def download_aih(
    ano: Union[int, List[int]],
    mes: Optional[Union[int, List[int]]] = None,
    estado: str = "SC",
    force: bool = False,
) -> pd.DataFrame:
    """Download de AIH (SIH/SUS) via PySUS.

    Args:
        ano: Ano ou lista de anos.
        mes: Mês ou lista de meses (1-12). Padrão: todos.
        estado: Sigla UF (padrão ``SC``).
        force: Sobrescreve cache existente.

    Returns:
        DataFrame com AIHs baixadas.
    """
    if not _PYSUS_AVAILABLE:
        raise RuntimeError("PySUS não está instalado.")

    anos: List[int] = [ano] if isinstance(ano, int) else ano
    meses: List[int] = list(range(1, 13)) if mes is None else ([mes] if isinstance(mes, int) else mes)
    cache_dir = _datasus_cache_dir("sih")
    frames: List[pd.DataFrame] = []

    for a in anos:
        for m in meses:
            file_path = cache_dir / f"AIH_{estado}_{a}_{m:02d}.parquet.gz"
            if file_path.exists() and not force:
                frames.append(pd.read_parquet(file_path))
                continue

            logger.info("Baixando AIH %s/%s/%02d...", estado, a, m)
            try:
                df = SIH.download(states=[estado], years=[a], months=[m], group="RD")
            except Exception as exc:  # pragma: no cover
                logger.error("Erro no download AIH %s/%02d: %s", a, m, exc)
                continue

            _save_raw(df, file_path)
            frames.append(df)

    if not frames:
        raise RuntimeError("Nenhum dado de AIH foi baixado.")
    return pd.concat(frames, ignore_index=True) if len(frames) > 1 else frames[0]


def download_bpa(
    ano: Union[int, List[int]],
    mes: Optional[Union[int, List[int]]] = None,
    estado: str = "SC",
    force: bool = False,
) -> pd.DataFrame:
    """Download de BPA (SIA/SUS) via PySUS.

    Args:
        ano: Ano ou lista de anos.
        mes: Mês ou lista de meses. Padrão: todos.
        estado: Sigla UF (padrão ``SC``).
        force: Sobrescreve cache existente.

    Returns:
        DataFrame com BPA baixados.
    """
    if not _PYSUS_AVAILABLE:
        raise RuntimeError("PySUS não está instalado.")

    anos: List[int] = [ano] if isinstance(ano, int) else ano
    meses: List[int] = list(range(1, 13)) if mes is None else ([mes] if isinstance(mes, int) else mes)
    cache_dir = _datasus_cache_dir("sia")
    frames: List[pd.DataFrame] = []

    for a in anos:
        for m in meses:
            file_path = cache_dir / f"BPA_{estado}_{a}_{m:02d}.parquet.gz"
            if file_path.exists() and not force:
                frames.append(pd.read_parquet(file_path))
                continue

            logger.info("Baixando BPA %s/%s/%02d...", estado, a, m)
            try:
                df = SIA.download(states=[estado], years=[a], months=[m], group="BPA")
            except Exception as exc:  # pragma: no cover
                logger.error("Erro no download BPA %s/%02d: %s", a, m, exc)
                continue

            _save_raw(df, file_path)
            frames.append(df)

    if not frames:
        raise RuntimeError("Nenhum dado de BPA foi baixado.")
    return pd.concat(frames, ignore_index=True) if len(frames) > 1 else frames[0]


def download_sipni(
    ano: Union[int, List[int]],
    estado: str = "SC",
    force: bool = False,
) -> pd.DataFrame:
    """Download de dados do SIPNI (Imunizações) via PySUS.

    Args:
        ano: Ano ou lista de anos.
        estado: Sigla UF (padrão ``SC``).
        force: Sobrescreve cache existente.

    Returns:
        DataFrame com registros de imunização.
    """
    if not _PYSUS_AVAILABLE:
        raise RuntimeError("PySUS não está instalado.")

    anos: List[int] = [ano] if isinstance(ano, int) else ano
    cache_dir = _datasus_cache_dir("sipni")
    frames: List[pd.DataFrame] = []

    for a in anos:
        file_path = cache_dir / f"SIPNI_{estado}_{a}.parquet.gz"
        if file_path.exists() and not force:
            frames.append(pd.read_parquet(file_path))
            continue

        logger.info("Baixando SIPNI %s/%s...", estado, a)
        try:
            df = PNI.download(states=[estado], years=[a])
        except Exception as exc:  # pragma: no cover
            logger.error("Erro no download SIPNI %s: %s", a, exc)
            raise

        _save_raw(df, file_path)
        frames.append(df)

    return pd.concat(frames, ignore_index=True) if len(frames) > 1 else frames[0]
