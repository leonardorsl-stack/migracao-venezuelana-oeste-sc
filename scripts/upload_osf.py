#!/usr/bin/env python3
"""Upload de arquivos ao OSF (Open Science Framework) via API v2.

Este script permite enviar arquivos e criar pastas em um projeto OSF
utilizando a API v2 e o WaterButler (v1).

Pré-requisitos:
    - Variável de ambiente ``OSF_TOKEN`` com escopo ``osf.full_write``.
    - Variável de ambiente ``OSF_NODE_ID`` (ex.: ``fna8v``).
    - Pacote ``requests`` instalado.

Exemplos::

    python scripts/upload_osf.py --file data/processados/dados.csv
    python scripts/upload_osf.py --file outputs/figura.png --target-path figuras/
    python scripts/upload_osf.py --file relatorio.pdf --node-id abc12
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Any

import requests

# Garante que src/ esteja no path para importar config, se necessário
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

# Carrega .env (idempotente)
try:
    from dotenv import load_dotenv

    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:  # pragma: no cover
    pass

OSF_API_BASE = "https://api.osf.io/v2"
OSF_FILES_BASE = "https://files.osf.io/v1"

logger = logging.getLogger(__name__)


def _get_token() -> str:
    token = os.getenv("OSF_TOKEN", "")
    if not token:
        raise OSError(
            "OSF_TOKEN não encontrado. Verifique seu arquivo .env."
        )
    return token


def _get_default_node_id() -> str:
    return os.getenv("OSF_NODE_ID", "")


def get_osf_headers() -> dict[str, str]:
    """Retorna headers padrão para autenticação na API OSF.

    Returns:
        Dict com ``Authorization`` (Bearer token) e ``Content-Type``.
    """
    return {
        "Authorization": f"Bearer {_get_token()}",
        "Content-Type": "application/vnd.api+json",
    }


def get_node_info(node_id: str) -> dict[str, Any]:
    """Obtém informações de um nó (projeto/componente) OSF.

    Args:
        node_id: Identificador do nó OSF.

    Returns:
        Dicionário com os dados do nó.

    Raises:
        requests.HTTPError: Se a requisição falhar.
    """
    url = f"{OSF_API_BASE}/nodes/{node_id}/"
    resp = requests.get(url, headers=get_osf_headers(), timeout=30)
    resp.raise_for_status()
    data = resp.json()
    logger.info("Nó '%s' encontrado: %s", node_id, data.get("data", {}).get("attributes", {}).get("title", "<sem título>"))
    return data


def list_osf_files(node_id: str) -> dict[str, Any]:
    """Lista arquivos na raiz do provider ``osfstorage`` do nó.

    Args:
        node_id: Identificador do nó OSF.

    Returns:
        Dicionário com a lista de arquivos/pastas.
    """
    url = f"{OSF_API_BASE}/nodes/{node_id}/files/osfstorage/"
    resp = requests.get(url, headers=get_osf_headers(), timeout=30)
    resp.raise_for_status()
    return resp.json()


def create_osf_folder(node_id: str, folder_name: str, target_path: str = "") -> dict[str, Any]:
    """Cria uma pasta vazia no OSF via WaterButler.

    A criação de pasta no OSF é feita fazendo um PUT para o WaterButler
    com o header ``Content-Type: application/octet-stream`` e
    ``Content-Length: 0``, e o nome da pasta terminando com ``/``.

    Args:
        node_id: Identificador do nó OSF.
        folder_name: Nome da nova pasta (sem barras internas).
        target_path: Caminho relativo dentro do osfstorage (ex.: ``figuras/``).

    Returns:
        Resposta JSON do WaterButler.
    """
    token = _get_token()
    # Normaliza target_path
    target_path = target_path.strip("/")
    folder_name = folder_name.strip("/")

    if target_path:
        full_path = f"{target_path}/{folder_name}/"
    else:
        full_path = f"{folder_name}/"

    url = f"{OSF_FILES_BASE}/resources/{node_id}/providers/osfstorage/{full_path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/octet-stream",
    }
    resp = requests.put(url, headers=headers, data=b"", timeout=30)
    resp.raise_for_status()
    logger.info("Pasta criada: %s", full_path)
    return resp.json()


def _get_upload_link(node_id: str, target_path: str = "") -> str:
    """Obtém o link de upload correto via API v2 do OSF.

    Para a raiz, usa o link base do provider (``/v2/nodes/{id}/files/``).
    Para subpastas, lista a raiz e retorna o ``links.upload`` da pasta.

    Args:
        node_id: Identificador do nó OSF.
        target_path: Caminho de destino relativo no osfstorage.

    Returns:
        URL base do WaterButler para upload.
    """
    headers = get_osf_headers()

    if target_path:
        target_path = target_path.strip("/")
        # Lista a raiz para encontrar a pasta e seu link de upload
        url = f"{OSF_API_BASE}/nodes/{node_id}/files/osfstorage/"
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        for item in resp.json().get("data", []):
            attr = item.get("attributes", {})
            if attr.get("kind") == "folder" and attr.get("name") == target_path:
                upload_link = item.get("links", {}).get("upload", "")
                if upload_link:
                    return upload_link
        raise FileNotFoundError(
            f"Pasta '{target_path}' não encontrada no OSF. "
            "Crie-a primeiro com create_osf_folder()."
        )

    # Link base do provider para a raiz
    url = f"{OSF_API_BASE}/nodes/{node_id}/files/"
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()["data"][0]
    return data["links"]["upload"]


def upload_file_to_osf(
    node_id: str,
    file_path: Path,
    target_path: str = "",
) -> dict[str, Any]:
    """Faz upload de um arquivo local para o OSF.

    Utiliza o endpoint do WaterButler (v1) com método PUT e query params
    ``kind=file&name={filename}`` conforme documentação atual do OSF.

    Args:
        node_id: Identificador do nó OSF.
        file_path: Caminho local do arquivo.
        target_path: Caminho de destino relativo no osfstorage.

    Returns:
        Resposta JSON do WaterButler com metadados do arquivo enviado.
    """
    token = _get_token()
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    target_path = target_path.strip("/")
    file_name = file_path.name

    # Evita duplicar o nome do arquivo no path
    if target_path.endswith(file_name):
        target_path = target_path[: -len(file_name)].strip("/")

    upload_base = _get_upload_link(node_id, target_path)
    upload_url = f"{upload_base}?kind=file&name={file_name}"

    file_size = file_path.stat().st_size
    logger.info("Enviando '%s' (%d bytes) para OSF/%s ...", file_name, file_size, target_path or "raiz")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/octet-stream",
    }

    with file_path.open("rb") as f:
        resp = requests.put(upload_url, headers=headers, data=f, timeout=300)
    resp.raise_for_status()
    logger.info("Upload concluído: %s", resp.json().get("data", {}).get("attributes", {}).get("name", file_name))
    return resp.json()


def _build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Upload de arquivos para o Open Science Framework (OSF).",
    )
    parser.add_argument(
        "--file",
        type=Path,
        required=True,
        help="Caminho local do arquivo a ser enviado.",
    )
    parser.add_argument(
        "--node-id",
        type=str,
        default=_get_default_node_id(),
        help="ID do nó OSF (padrão: valor da env OSF_NODE_ID).",
    )
    parser.add_argument(
        "--target-path",
        type=str,
        default="",
        help="Caminho de destino relativo no osfstorage (ex.: dados/brutos).",
    )
    parser.add_argument(
        "--create-folder",
        type=str,
        default="",
        help="Cria uma pasta vazia no destino especificado antes do upload.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Lista arquivos existentes no nó e sai sem fazer upload.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Ativa saída detalhada (DEBUG).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_argparser().parse_args(argv)

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
    )

    node_id = args.node_id or _get_default_node_id()
    if not node_id:
        logger.error("--node-id é obrigatório quando OSF_NODE_ID não está definido no .env.")
        return 1

    try:
        # Valida credenciais e existência do nó
        get_node_info(node_id)
    except requests.HTTPError as exc:
        logger.error("Falha ao acessar nó OSF '%s': %s", node_id, exc)
        return 1
    except OSError as exc:
        logger.error("%s", exc)
        return 1

    if args.list:
        try:
            files = list_osf_files(node_id)
            for item in files.get("data", []):
                attr = item.get("attributes", {})
                kind = attr.get("kind", "?")
                name = attr.get("name", "?")
                print(f"[{kind}] {name}")
        except requests.HTTPError as exc:
            logger.error("Erro ao listar arquivos: %s", exc)
            return 1
        return 0

    if args.create_folder:
        try:
            create_osf_folder(node_id, args.create_folder, args.target_path)
        except requests.HTTPError as exc:
            logger.error("Erro ao criar pasta: %s", exc)
            return 1

    try:
        upload_file_to_osf(node_id, args.file, args.target_path)
    except requests.HTTPError as exc:
        logger.error("Erro no upload: %s", exc)
        return 1
    except FileNotFoundError as exc:
        logger.error("%s", exc)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
