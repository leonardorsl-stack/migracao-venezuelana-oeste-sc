"""Extrator para dados do CAGED (Cadastro Geral de Empregados e Desempregados).

Este módulo implementa o download dos microdados do Novo CAGED, mantido pelo
Ministério do Trabalho e Emprego (MTE). O CAGED registra admissões e
desligamentos formais do mercado de trabalho brasileiro.

A partir de 2020, o Novo CAGED apresenta layout diferente do legado, com
arquivos mensais em formato ``.txt`` compactados em ``.7z``. Este módulo
implementa download via FTP, descompactação e concatenação histórica.

Referência:
    - https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/caged

Example:
    >>> from src.extract.caged import fetch_caged_admissoes, concatena_historica
    >>> df_2022 = fetch_caged_admissoes(ano=2022, mes=3, uf="SC")
    >>> df_hist = concatena_historica(anos=range(2020, 2024), tipo="admissao", uf="SC")
"""

from __future__ import annotations

import logging
import shutil
import subprocess
from ftplib import FTP, error_perm
from pathlib import Path
from typing import List, Literal, Optional, Union

import pandas as pd

from src.config import SETTINGS

logger = logging.getLogger(__name__)

_CAGED_FTP_HOST = "ftp.mtps.gov.br"
_CAGED_FTP_BASE = "/pdet/microdados/NOVO%20CAGED/"

# Layout do arquivo muda conforme o ano
_CAGED_LAYOUTS = {
    "2020": {
        "sep": ";",
        "encoding": "utf-8",
        "admissao": "CAGEDMOV{ano}{mes:02d}.txt",
        "desligamento": "CAGEDMOV{ano}{mes:02d}.txt",
    },
    "2021": {
        "sep": ";",
        "encoding": "utf-8",
        "admissao": "CAGEDMOV{ano}{mes:02d}.txt",
        "desligamento": "CAGEDMOV{ano}{mes:02d}.txt",
    },
    "2022": {
        "sep": ";",
        "encoding": "utf-8",
        "admissao": "CAGEDMOV{ano}{mes:02d}.txt",
        "desligamento": "CAGEDMOV{ano}{mes:02d}.txt",
    },
    "2023": {
        "sep": ";",
        "encoding": "utf-8",
        "admissao": "CAGEDMOV{ano}{mes:02d}.txt",
        "desligamento": "CAGEDMOV{ano}{mes:02d}.txt",
    },
    "2024": {
        "sep": ";",
        "encoding": "utf-8",
        "admissao": "CAGEDMOV{ano}{mes:02d}.txt",
        "desligamento": "CAGEDMOV{ano}{mes:02d}.txt",
    },
}


def _caged_cache_dir() -> Path:
    """Retorna o diretório de cache para arquivos do CAGED."""
    path = SETTINGS.DATA_RAW / "caged"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _decompress_7z(src: Path, dest_dir: Path) -> List[Path]:
    """Descompacta arquivo ``.7z`` para o diretório de destino.

    Args:
        src: Arquivo ``.7z``.
        dest_dir: Diretório de saída.

    Returns:
        Lista de arquivos extraídos.

    Raises:
        FileNotFoundError: Se ``7z`` não estiver instalado.
        RuntimeError: Se a descompactação falhar.
    """
    if shutil.which("7z") is None:
        raise FileNotFoundError(
            "Utilitário '7z' não encontrado. Instale o p7zip."
        )

    logger.info("Descompactando %s...", src)
    result = subprocess.run(
        ["7z", "x", str(src), f"-o{dest_dir}", "-y"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Falha ao descompactar {src}: {result.stderr}")

    return sorted(dest_dir.glob("*.txt"))


def _download_caged_file(
    ano: int,
    mes: int,
    tipo: Literal["admissao", "desligamento"],
    ftp_user: Optional[str] = None,
    ftp_pass: Optional[str] = None,
    force: bool = False,
) -> Path:
    """Baixa o arquivo mensal do CAGED via FTP.

    Args:
        ano: Ano do movimento.
        mes: Mês do movimento.
        tipo: ``admissao`` ou ``desligamento``.
        ftp_user: Usuário FTP (se necessário).
        ftp_pass: Senha FTP (se necessário).
        force: Força re-download.

    Returns:
        Caminho do arquivo de texto descompactado.
    """
    cache_dir = _caged_cache_dir()
    layout = _CAGED_LAYOUTS.get(str(ano), _CAGED_LAYOUTS["2024"])
    base_name = layout[tipo].format(ano=ano, mes=mes)
    remote_7z = f"{base_name}.7z"
    local_7z = cache_dir / remote_7z
    extract_dir = cache_dir / f"{ano}{mes:02d}"
    txt_path = extract_dir / base_name

    if txt_path.exists() and not force:
        logger.info("Arquivo CAGED %s/%s já existe em cache.", ano, mes)
        return txt_path

    if not local_7z.exists() or force:
        logger.info("Conectando ao FTP %s para CAGED...", _CAGED_FTP_HOST)
        try:
            ftp = FTP(_CAGED_FTP_HOST, timeout=120)
            if ftp_user:
                ftp.login(user=ftp_user, passwd=ftp_pass or "")
            else:
                ftp.login()
        except Exception as exc:
            raise ConnectionError(f"Falha na conexão FTP: {exc}")

        remote_dir = f"{_CAGED_FTP_BASE}{ano}/"
        try:
            ftp.cwd(remote_dir)
        except error_perm as exc:
            raise FileNotFoundError(
                f"Diretório remoto não encontrado: {remote_dir}"
            ) from exc

        logger.info("Baixando %s...", remote_7z)
        with open(local_7z, "wb") as f:
            ftp.retrbinary(f"RETR {remote_7z}", f.write)
        ftp.quit()
        logger.info("Download concluído: %s", local_7z)

    extract_dir.mkdir(parents=True, exist_ok=True)
    _decompress_7z(local_7z, extract_dir)

    if not txt_path.exists():
        raise FileNotFoundError(f"Arquivo esperado não encontrado após extração: {txt_path}")

    return txt_path


def fetch_caged_admissoes(
    ano: int,
    mes: Union[int, List[int]],
    uf: Optional[str] = "SC",
    nacionalidade: Optional[Union[str, List[str]]] = None,
    force: bool = False,
) -> pd.DataFrame:
    """Obtém dados de admissões do CAGED.

    Args:
        ano: Ano do movimento.
        mes: Mês ou lista de meses.
        uf: Sigla da UF para filtro. Padrão ``SC``.
        nacionalidade: Nacionalidade(es) para filtrar. Padrão: todas.
        force: Força re-download.

    Returns:
        DataFrame com admissões filtradas.
    """
    meses: List[int] = [mes] if isinstance(mes, int) else mes
    frames: List[pd.DataFrame] = []

    for m in meses:
        txt_path = _download_caged_file(ano, m, "admissao", force=force)
        layout = _CAGED_LAYOUTS.get(str(ano), _CAGED_LAYOUTS["2024"])

        df = pd.read_csv(
            txt_path,
            sep=layout["sep"],
            encoding=layout["encoding"],
            low_memory=False,
            dtype=str,
        )

        # Filtro UF
        col_uf = "uf" if "uf" in df.columns else "Sigla da UF"
        if col_uf in df.columns and uf:
            df = df[df[col_uf] == uf]

        # Filtro nacionalidade
        if nacionalidade is not None:
            nacs = [nacionalidade] if isinstance(nacionalidade, str) else nacionalidade
            col_nac = "nacionalidade" if "nacionalidade" in df.columns else "Nacionalidade"
            if col_nac in df.columns:
                df = df[df[col_nac].isin(nacs)]

        if not df.empty:
            df["ano"] = ano
            df["mes"] = m
            frames.append(df)

    if not frames:
        logger.warning("Nenhuma admissão encontrada para os critérios.")
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)


def fetch_caged_desligamentos(
    ano: int,
    mes: Union[int, List[int]],
    uf: Optional[str] = "SC",
    nacionalidade: Optional[Union[str, List[str]]] = None,
    force: bool = False,
) -> pd.DataFrame:
    """Obtém dados de desligamentos do CAGED.

    Args:
        ano: Ano do movimento.
        mes: Mês ou lista de meses.
        uf: Sigla da UF para filtro. Padrão ``SC``.
        nacionalidade: Nacionalidade(es) para filtrar. Padrão: todas.
        force: Força re-download.

    Returns:
        DataFrame com desligamentos filtrados.
    """
    meses: List[int] = [mes] if isinstance(mes, int) else mes
    frames: List[pd.DataFrame] = []

    for m in meses:
        txt_path = _download_caged_file(ano, m, "desligamento", force=force)
        layout = _CAGED_LAYOUTS.get(str(ano), _CAGED_LAYOUTS["2024"])

        df = pd.read_csv(
            txt_path,
            sep=layout["sep"],
            encoding=layout["encoding"],
            low_memory=False,
            dtype=str,
        )

        col_uf = "uf" if "uf" in df.columns else "Sigla da UF"
        if col_uf in df.columns and uf:
            df = df[df[col_uf] == uf]

        if nacionalidade is not None:
            nacs = [nacionalidade] if isinstance(nacionalidade, str) else nacionalidade
            col_nac = "nacionalidade" if "nacionalidade" in df.columns else "Nacionalidade"
            if col_nac in df.columns:
                df = df[df[col_nac].isin(nacs)]

        if not df.empty:
            df["ano"] = ano
            df["mes"] = m
            frames.append(df)

    if not frames:
        logger.warning("Nenhum desligamento encontrado para os critérios.")
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)


def concatena_historica(
    anos: Union[range, List[int]],
    tipo: Literal["admissao", "desligamento"],
    uf: Optional[str] = "SC",
    nacionalidade: Optional[Union[str, List[str]]] = None,
    force: bool = False,
) -> pd.DataFrame:
    """Concatena séries históricas do CAGED em um único DataFrame.

    Args:
        anos: Iterável de anos para download.
        tipo: ``admissao`` ou ``desligamento``.
        uf: Sigla da UF.
        nacionalidade: Nacionalidade(es) para filtrar.
        force: Força re-download de todos os arquivos.

    Returns:
        DataFrame concatenado com todos os anos/meses solicitados.
    """
    anos_list: List[int] = list(anos)
    frames: List[pd.DataFrame] = []

    fetch_fn = (
        fetch_caged_admissoes if tipo == "admissao" else fetch_caged_desligamentos
    )

    for ano in anos_list:
        logger.info("Processando CAGED %s %s...", tipo, ano)
        try:
            df = fetch_fn(
                ano=ano,
                mes=list(range(1, 13)),
                uf=uf,
                nacionalidade=nacionalidade,
                force=force,
            )
            if not df.empty:
                frames.append(df)
        except Exception as exc:
            logger.error("Falha ao processar CAGED %s %s: %s", tipo, ano, exc)

    if not frames:
        raise RuntimeError(f"Nenhum dado de {tipo} foi concatenado.")

    result = pd.concat(frames, ignore_index=True)
    logger.info("Concatenação histórica concluída: %s registros.", len(result))
    return result
