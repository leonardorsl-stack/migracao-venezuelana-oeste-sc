"""Extrator para microdados da RAIS (Relação Anual de Informações Sociais).

Este módulo implementa o download de microdados da RAIS, mantida pelo Ministério
do Trabalho e Emprego (MTE). A RAIS contém informações sobre vínculos
empregatícios formais no Brasil, incluindo variáveis de nacionalidade, escolaridade,
raça/cor, salário, entre outras.

Acesso e Limitações:
    Os microdados da RAIS **não estão disponíveis para download automático**
    sem credenciais ou sem aceite de termos de uso. As principais formas de
    obtenção são:

    1. **FTP do MTE** (``ftp.mtps.gov.br``): requer credenciais de acesso que
       devem ser solicitadas diretamente ao Ministério do Trabalho e Emprego.
    2. **Portal basedosdados.org**: oferece a RAIS tratada em formato
       amigável (BigQuery), mas também exige cadastro.
    3. **Portal RAIS.gov.br**: permite download manual de arquivos
       estabelecimentos e vínculos, geralmente compactados em ``.7z``.

    Por conta dessas restrições, este módulo documenta a interface esperada
    mas pode falhar em ambientes sem credenciais FTP ou sem os arquivos
    locais prévio download.

Note:
    Este módulo documenta a interface esperada. A implementação completa do
    download via FTP depende de credenciais e da estrutura de diretórios do
    servidor, que podem mudar entre os anos.

Example:
    >>> from src.extract.rais import fetch_rais_vinculos
    >>> df = fetch_rais_vinculos(ano=2022, uf="SC", nacionalidade="VENEZUELA")
"""

from __future__ import annotations

import gzip
import logging
import shutil
from ftplib import FTP, error_perm
from pathlib import Path
from typing import List, Optional, Union

import pandas as pd

from src.config import SETTINGS

logger = logging.getLogger(__name__)

_RAIS_FTP_HOST = "ftp.mtps.gov.br"
_RAIS_FTP_BASE = "/pdet/microdados/RAIS/"

# Nomenclatura de arquivos RAIS (exemplo para 2020+)
_RAIS_FILENAME_PATTERNS = {
    "vinculos": "RAIS_VINC_PUB_{ano}.7z",
    "estabelecimentos": "RAIS_ESTAB_PUB_{ano}.7z",
}


def _rais_cache_dir() -> Path:
    """Retorna o diretório de cache para arquivos da RAIS."""
    path = SETTINGS.DATA_RAW / "rais"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _decompress_7z(src: Path, dest_dir: Path) -> List[Path]:
    """Descompacta arquivo ``.7z`` utilizando o utilitário de linha de comando.

    Args:
        src: Caminho do arquivo ``.7z``.
        dest_dir: Diretório de destino.

    Returns:
        Lista de caminhos dos arquivos extraídos.

    Raises:
        FileNotFoundError: Se o utilitário ``7z`` não estiver disponível.
        RuntimeError: Se a descompactação falhar.
    """
    import subprocess

    if shutil.which("7z") is None:
        raise FileNotFoundError(
            "Utilitário '7z' não encontrado. Instale o p7zip."
        )

    logger.info("Descompactando %s em %s...", src, dest_dir)
    result = subprocess.run(
        ["7z", "x", str(src), f"-o{dest_dir}", "-y"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Falha ao descompactar {src}: {result.stderr}")

    # Retorna arquivos txt/csv extraídos
    return sorted(dest_dir.glob("*.txt"))


def fetch_rais_vinculos(
    ano: int,
    uf: Optional[str] = "SC",
    nacionalidade: Optional[Union[str, List[str]]] = None,
    colunas: Optional[List[str]] = None,
    chunk_size: Optional[int] = 100_000,
    ftp_user: Optional[str] = None,
    ftp_pass: Optional[str] = None,
    force: bool = False,
) -> pd.DataFrame:
    """Download e filtro dos microdados de vínculos da RAIS.

    Realiza o download do arquivo de vínculos do ano especificado, descompacta,
    e aplica filtros de UF e nacionalidade conforme solicitado.

    Args:
        ano: Ano de referência da RAIS (ex: 2022).
        uf: Sigla da UF para filtro. Padrão ``SC``.
        nacionalidade: Nacionalidade ou lista de nacionalidades para filtrar.
            Se ``None``, retorna todos os vínculos.
        colunas: Subconjunto de colunas a serem lidas. ``None`` lê todas.
        chunk_size: Tamanho do chunk para leitura em streaming de arquivos
            grandes. ``None`` carrega tudo em memória.
        ftp_user: Usuário para FTP do MTE (se necessário).
        ftp_pass: Senha para FTP do MTE (se necessário).
        force: Se ``True``, força re-download mesmo que cache exista.

    Returns:
        DataFrame com vínculos empregatícios filtrados.

    Raises:
        ConnectionError: Se não for possível conectar ao FTP.
        FileNotFoundError: Se o arquivo do ano não existir no servidor.
        ValueError: Se o ano for inválido.
    """
    if ano < 1985 or ano > 2025:
        raise ValueError(f"Ano {ano} fora do intervalo suportado pela RAIS.")

    cache_dir = _rais_cache_dir()
    parquet_path = cache_dir / f"RAIS_VINC_{ano}_filtrado.parquet"

    if parquet_path.exists() and not force:
        logger.info("Carregando RAIS %s do cache local.", ano)
        return pd.read_parquet(parquet_path)

    # Define arquivo remoto
    remote_name = _RAIS_FILENAME_PATTERNS["vinculos"].format(ano=ano)
    local_7z = cache_dir / remote_name

    if not local_7z.exists() or force:
        logger.info("Conectando ao FTP %s...", _RAIS_FTP_HOST)
        try:
            ftp = FTP(_RAIS_FTP_HOST, timeout=120)
            if ftp_user:
                ftp.login(user=ftp_user, passwd=ftp_pass or "")
            else:
                ftp.login()  # FTP anônimo ou sem credenciais
        except Exception as exc:
            raise ConnectionError(f"Falha na conexão FTP: {exc}")

        remote_dir = f"{_RAIS_FTP_BASE}{ano}/"
        try:
            ftp.cwd(remote_dir)
        except error_perm as exc:
            raise FileNotFoundError(
                f"Diretório remoto não encontrado: {remote_dir}"
            ) from exc

        logger.info("Baixando %s...", remote_name)
        with open(local_7z, "wb") as f:
            ftp.retrbinary(f"RETR {remote_name}", f.write)
        ftp.quit()
        logger.info("Download concluído: %s", local_7z)

    # Descompacta
    extracted = _decompress_7z(local_7z, cache_dir / f"RAIS_{ano}")
    if not extracted:
        raise FileNotFoundError("Nenhum arquivo extraído do 7z.")

    txt_file = extracted[0]
    logger.info("Lendo %s...", txt_file)

    # Leitura com chunking opcional
    if chunk_size:
        chunks = []
        reader = pd.read_csv(
            txt_file,
            sep=";",
            encoding="latin1",
            low_memory=False,
            chunksize=chunk_size,
            usecols=colunas,
            dtype=str,
        )
        for chunk in reader:
            if uf:
                chunk = chunk[chunk.get("Sigla da UF", chunk.get("UF", "")) == uf]
            if nacionalidade:
                nacs = [nacionalidade] if isinstance(nacionalidade, str) else nacionalidade
                col_nac = "Nacionalidade" if "Nacionalidade" in chunk.columns else "Nacionalidade Vinculo"
                if col_nac in chunk.columns:
                    chunk = chunk[chunk[col_nac].isin(nacs)]
            if not chunk.empty:
                chunks.append(chunk)
        df = pd.concat(chunks, ignore_index=True) if chunks else pd.DataFrame()
    else:
        df = pd.read_csv(
            txt_file,
            sep=";",
            encoding="latin1",
            low_memory=False,
            usecols=colunas,
            dtype=str,
        )
        if uf:
            df = df[df.get("Sigla da UF", df.get("UF", "")) == uf]
        if nacionalidade:
            nacs = [nacionalidade] if isinstance(nacionalidade, str) else nacionalidade
            col_nac = "Nacionalidade" if "Nacionalidade" in df.columns else "Nacionalidade Vinculo"
            if col_nac in df.columns:
                df = df[df[col_nac].isin(nacs)]

    # Persiste resultado filtrado
    if not df.empty:
        df.to_parquet(parquet_path, index=False, compression="gzip")
        logger.info("RAIS filtrada salva em %s (%s registros)", parquet_path, len(df))
    else:
        logger.warning("Nenhum registro encontrado após filtros.")

    return df
