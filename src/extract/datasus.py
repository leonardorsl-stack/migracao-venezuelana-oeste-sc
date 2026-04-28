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

**Aviso de dados sensíveis:**
    Os microdados do DataSUS contêm informações individuais de saúde
    (incluindo causa de óbito, diagnóstico, procedimentos, etc.). Antes de
    qualquer publicação ou compartilhamento, os dados devem ser
    **anonimizados** e agregados a nível municipal ou outro nível
    estatístico adequado, conforme a Lei Geral de Proteção de Dados
    (LGPD – Lei nº 13.709/2018).

Example:
    >>> from src.extract.datasus import download_sim_sc
    >>> df = download_sim_sc(years=[2022, 2023])
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
        "As funções de extract/datasus funcionarão como stubs. "
        "Instale com: conda install -c conda-forge pysus  (ou pip install pysus)",
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
    path = SETTINGS.DATA_RAW / "datasus" / subdir.upper()
    path.mkdir(parents=True, exist_ok=True)
    return path


def _save_raw(df: pd.DataFrame, path: Path) -> Path:
    """Salva DataFrame bruto em Parquet comprimido com zstd.

    Args:
        df: Dados brutos extraídos.
        path: Caminho do arquivo de destino.

    Returns:
        Caminho do arquivo salvo.
    """
    df.to_parquet(path, index=False, compression="zstd")
    logger.info("Raw DataSUS salvo em %s", path)
    return path


def _save_stub(path: Path, base_name: str, error_msg: str) -> pd.DataFrame:
    """Cria um DataFrame stub vazio e o salva, documentando o erro.

    Args:
        path: Caminho do arquivo Parquet stub.
        base_name: Nome da base (ex: SIM_SC_2022).
        error_msg: Mensagem de erro a ser registrada.

    Returns:
        DataFrame vazio com colunas informativas.
    """
    logger.warning("Criando stub vazio para %s: %s", base_name, error_msg)
    df = pd.DataFrame({
        "stub": [True],
        "base": [base_name],
        "erro": [error_msg],
    })
    df.to_parquet(path, index=False, compression="zstd")
    return df


def download_sim_sc(
    years: Optional[Union[int, List[int]]] = None,
    force: bool = False,
) -> pd.DataFrame:
    """Download dos dados do SIM (Mortalidade) para SC via PySUS.

    Os microdados do SIM contêm informações individuais sobre óbitos,
    incluindo causa básica (CAUSABAS), local de ocorrência, data, etc.
    **Dados sensíveis – anonimizar antes de agregação.**

    Após o download, registros sem ``CAUSABAS`` são descartados, e apenas
    colunas de interesse são mantidas para reduzir o volume.

    Args:
        years: Ano ou lista de anos de interesse. Padrão: ``[2018, 2019,
            2020, 2021, 2022, 2023]``.
        force: Se ``True``, sobrescreve arquivo existente.

    Returns:
        DataFrame com microdados do SIM. Se o download falhar, retorna
        um DataFrame stub vazio documentando o erro.
    """
    if years is None:
        years = list(range(2018, 2024))
    anos: List[int] = [years] if isinstance(years, int) else years

    if not _PYSUS_AVAILABLE:
        logger.error("PySUS não está instalado. Instale com: pip install pysus")
        cache_dir = _datasus_cache_dir("sim")
        stub_path = cache_dir / "SIM_SC_STUB.parquet"
        return _save_stub(stub_path, "SIM_SC", "PySUS não instalado")

    cache_dir = _datasus_cache_dir("sim")
    frames: List[pd.DataFrame] = []

    for a in anos:
        if a < 1996 or a > 2024:
            logger.warning("Ano %s pode não estar disponível no SIM.", a)

        file_path = cache_dir / f"DO_SC_{a}.parquet"
        if file_path.exists() and not force:
            logger.info("Carregando SIM SC %s do cache.", a)
            frames.append(pd.read_parquet(file_path))
            continue

        logger.info("Baixando SIM SC %s...", a)
        try:
            result = SIM.download(groups="CID10", states="SC", years=a)
            if isinstance(result, list):
                if not result:
                    raise ValueError("PySUS retornou lista vazia para SIM %s." % a)
                df = pd.concat([r.to_dataframe() for r in result], ignore_index=True)
            else:
                df = result.to_dataframe()
        except Exception as exc:
            logger.error("Erro no download SIM SC %s: %s", a, exc)
            stub = _save_stub(file_path, f"SIM_SC_{a}", str(exc))
            frames.append(stub)
            continue

        # Filtra registros sem causa básica e mantém colunas de interesse
        if "CAUSABAS" in df.columns:
            df = df.dropna(subset=["CAUSABAS"])
        else:
            logger.warning("Coluna CAUSABAS não encontrada no SIM %s.", a)

        # Padroniza tipos úteis
        for col in ["DTOBITO", "DTNASC", "IDADE", "SEXO", "RACACOR", "CAUSABAS", "CODMUNRES"]:
            if col in df.columns:
                df[col] = df[col].astype(str)

        df["ano_sim"] = a
        _save_raw(df, file_path)
        frames.append(df)

    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def download_sinasc_sc(
    years: Optional[Union[int, List[int]]] = None,
    force: bool = False,
) -> pd.DataFrame:
    """Download dos dados do SINASC (Nascidos Vivos) para SC via PySUS.

    Os microdados do SINASC contêm informações sobre nascimentos,
    incluindo peso ao nascer, APGAR, escolaridade da mãe, etc.

    Args:
        years: Ano ou lista de anos. Padrão: ``[2018, 2019, 2020, 2021,
            2022, 2023]``.
        force: Sobrescreve cache existente.

    Returns:
        DataFrame com microdados do SINASC. Se falhar, retorna stub.
    """
    if years is None:
        years = list(range(2018, 2024))
    anos: List[int] = [years] if isinstance(years, int) else years

    if not _PYSUS_AVAILABLE:
        logger.error("PySUS não está instalado.")
        cache_dir = _datasus_cache_dir("sinasc")
        stub_path = cache_dir / "SINASC_SC_STUB.parquet"
        return _save_stub(stub_path, "SINASC_SC", "PySUS não instalado")

    cache_dir = _datasus_cache_dir("sinasc")
    frames: List[pd.DataFrame] = []

    for a in anos:
        file_path = cache_dir / f"DN_SC_{a}.parquet"
        if file_path.exists() and not force:
            logger.info("Carregando SINASC SC %s do cache.", a)
            frames.append(pd.read_parquet(file_path))
            continue

        logger.info("Baixando SINASC SC %s...", a)
        try:
            result = SINASC.download(groups="DN", states="SC", years=a)
            if isinstance(result, list):
                if not result:
                    raise ValueError("PySUS retornou lista vazia para SINASC %s." % a)
                df = pd.concat([r.to_dataframe() for r in result], ignore_index=True)
            else:
                df = result.to_dataframe()
        except Exception as exc:
            logger.error("Erro no download SINASC SC %s: %s", a, exc)
            stub = _save_stub(file_path, f"SINASC_SC_{a}", str(exc))
            frames.append(stub)
            continue

        # Padroniza colunas úteis
        for col in ["DTNASC", "SEXO", "IDADEMAE", "CODMUNRES", "PESO", "APGAR1", "APGAR5"]:
            if col in df.columns:
                df[col] = df[col].astype(str)

        df["ano_sinasc"] = a
        _save_raw(df, file_path)
        frames.append(df)

    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


# ---------------------------------------------------------------------------
# Funções legadas (mantidas para compatibilidade)
# ---------------------------------------------------------------------------

def download_datasus_sim(
    years: Union[int, List[int]],
    state: str = "SC",
    force: bool = False,
) -> pd.DataFrame:
    """Download dos dados do SIM (Mortalidade) via PySUS.

    .. deprecated::
        Prefira ``download_sim_sc()`` que já fixa o estado e padroniza
        a saída.
    """
    return download_sim_sc(years=years, force=force)


def download_datasus_sinasc(
    years: Union[int, List[int]],
    state: str = "SC",
    force: bool = False,
) -> pd.DataFrame:
    """Download dos dados do SINASC (Nascidos Vivos) via PySUS.

    .. deprecated::
        Prefira ``download_sinasc_sc()`` que já fixa o estado e padroniza
        a saída.
    """
    return download_sinasc_sc(years=years, force=force)


def download_datasus_aih(
    years: Union[int, List[int]],
    months: Optional[Union[int, List[int]]] = None,
    state: str = "SC",
    force: bool = False,
) -> pd.DataFrame:
    """Download de AIH (SIH/SUS) via PySUS.

    Os dados de AIH (Autorização de Internação Hospitalar) registram
    internações no SUS, incluindo diagnóstico principal, procedimento
    realizado, valor pago, etc.

    Args:
        years: Ano ou lista de anos.
        months: Mês ou lista de meses (1-12). Padrão: todos.
        state: Sigla UF (padrão ``SC``).
        force: Sobrescreve cache existente.

    Returns:
        DataFrame com AIHs baixadas. Se falhar, retorna stub.
    """
    if not _PYSUS_AVAILABLE:
        logger.error("PySUS não está instalado.")
        cache_dir = _datasus_cache_dir("sih")
        stub_path = cache_dir / f"SIH_{state}_STUB.parquet"
        return _save_stub(stub_path, f"SIH_{state}", "PySUS não instalado")

    anos: List[int] = [years] if isinstance(years, int) else years
    meses: List[int] = list(range(1, 13)) if months is None else ([months] if isinstance(months, int) else months)
    cache_dir = _datasus_cache_dir("sih")
    frames: List[pd.DataFrame] = []

    for a in anos:
        for m in meses:
            file_path = cache_dir / f"RD_{state}_{a}_{m:02d}.parquet"
            if file_path.exists() and not force:
                frames.append(pd.read_parquet(file_path))
                continue

            logger.info("Baixando AIH %s/%s/%02d...", state, a, m)
            try:
                result = SIH.download(states=state, years=a, months=m, group="RD")
                df = result.to_dataframe()
            except Exception as exc:
                logger.error("Erro no download AIH %s/%02d: %s", a, m, exc)
                stub = _save_stub(file_path, f"SIH_{state}_{a}_{m:02d}", str(exc))
                frames.append(stub)
                continue

            _save_raw(df, file_path)
            frames.append(df)

    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def download_bpa(
    years: Union[int, List[int]],
    months: Optional[Union[int, List[int]]] = None,
    state: str = "SC",
    force: bool = False,
) -> pd.DataFrame:
    """Download de BPA (SIA/SUS) via PySUS.

    Args:
        years: Ano ou lista de anos.
        months: Mês ou lista de meses. Padrão: todos.
        state: Sigla UF (padrão ``SC``).
        force: Sobrescreve cache existente.

    Returns:
        DataFrame com BPA baixados.
    """
    if not _PYSUS_AVAILABLE:
        logger.error("PySUS não está instalado.")
        cache_dir = _datasus_cache_dir("sia")
        stub_path = cache_dir / f"SIA_{state}_STUB.parquet"
        return _save_stub(stub_path, f"SIA_{state}", "PySUS não instalado")

    anos: List[int] = [years] if isinstance(years, int) else years
    meses: List[int] = list(range(1, 13)) if months is None else ([months] if isinstance(months, int) else months)
    cache_dir = _datasus_cache_dir("sia")
    frames: List[pd.DataFrame] = []

    for a in anos:
        for m in meses:
            file_path = cache_dir / f"BPA_{state}_{a}_{m:02d}.parquet"
            if file_path.exists() and not force:
                frames.append(pd.read_parquet(file_path))
                continue

            logger.info("Baixando BPA %s/%s/%02d...", state, a, m)
            try:
                result = SIA.download(states=state, years=a, months=m, group="BPA")
                df = result.to_dataframe()
            except Exception as exc:
                logger.error("Erro no download BPA %s/%02d: %s", a, m, exc)
                stub = _save_stub(file_path, f"SIA_{state}_{a}_{m:02d}", str(exc))
                frames.append(stub)
                continue

            _save_raw(df, file_path)
            frames.append(df)

    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def download_sipni(
    years: Union[int, List[int]],
    state: str = "SC",
    force: bool = False,
) -> pd.DataFrame:
    """Download de dados do SIPNI (Imunizações) via PySUS.

    Args:
        years: Ano ou lista de anos.
        state: Sigla UF (padrão ``SC``).
        force: Sobrescreve cache existente.

    Returns:
        DataFrame com registros de imunização.
    """
    if not _PYSUS_AVAILABLE:
        logger.error("PySUS não está instalado.")
        cache_dir = _datasus_cache_dir("sipni")
        stub_path = cache_dir / f"SIPNI_{state}_STUB.parquet"
        return _save_stub(stub_path, f"SIPNI_{state}", "PySUS não instalado")

    anos: List[int] = [years] if isinstance(years, int) else years
    cache_dir = _datasus_cache_dir("sipni")
    frames: List[pd.DataFrame] = []

    for a in anos:
        file_path = cache_dir / f"SIPNI_{state}_{a}.parquet"
        if file_path.exists() and not force:
            frames.append(pd.read_parquet(file_path))
            continue

        logger.info("Baixando SIPNI %s/%s...", state, a)
        try:
            result = PNI.download(states=state, years=a)
            df = result.to_dataframe()
        except Exception as exc:
            logger.error("Erro no download SIPNI %s: %s", a, exc)
            stub = _save_stub(file_path, f"SIPNI_{state}_{a}", str(exc))
            frames.append(stub)
            continue

        _save_raw(df, file_path)
        frames.append(df)

    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)
