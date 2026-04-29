#!/usr/bin/env python3
"""Criação de depósitos e upload de arquivos no Zenodo.

Suporta tanto o Zenodo de produção quanto o *sandbox*.
Ao publicar, o DOI e o link de acesso são impressos no terminal.

Pré-requisitos:
    - Variável de ambiente ``ZENODO_TOKEN``.
    - Pacote ``requests`` instalado.

Exemplos::

    python scripts/upload_zenodo.py \
        --title "Dados da migração venezuelana em SC" \
        --description "Conjunto de dados processados referentes à migração..." \
        --file outputs/dados.csv

    python scripts/upload_zenodo.py \
        --title "Teste sandbox" \
        --description "Descrição de teste" \
        --file data/amostra.parquet \
        --sandbox \
        --publish
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

try:
    from dotenv import load_dotenv

    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:  # pragma: no cover
    pass

logger = logging.getLogger(__name__)


def _get_token() -> str:
    token = os.getenv("ZENODO_TOKEN", "")
    if not token:
        raise OSError(
            "ZENODO_TOKEN não encontrado. Verifique seu arquivo .env."
        )
    return token


def get_zenodo_api_url(sandbox: bool = False) -> str:
    """Retorna a URL base da API do Zenodo.

    Args:
        sandbox: Se ``True``, usa o ambiente de testes (sandbox.zenodo.org).

    Returns:
        URL base da API (v1).
    """
    return (
        "https://sandbox.zenodo.org/api"
        if sandbox
        else "https://zenodo.org/api"
    )


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {_get_token()}",
        "Content-Type": "application/json",
    }


def create_deposition(
    title: str,
    description: str,
    creators: list[dict[str, Any]],
    sandbox: bool = False,
    metadata_extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Cria um novo depósito (rascunho) no Zenodo.

    Args:
        title: Título do depósito.
        description: Resumo / descrição do conteúdo.
        creators: Lista de dicionários com chaves ``name``, ``affiliation`` e,
            opcionalmente, ``orcid``.
        sandbox: Usa o ambiente sandbox.
        metadata_extra: Campos adicionais de metadados (upload_type, keywords, etc.).

    Returns:
        Dicionário com os dados do depósito criado.
    """
    url = f"{get_zenodo_api_url(sandbox)}/deposit/depositions"
    payload: dict[str, Any] = {
        "metadata": {
            "title": title,
            "description": description,
            "upload_type": (metadata_extra or {}).get("upload_type", "dataset"),
            "creators": creators,
        }
    }
    if metadata_extra:
        for key, value in metadata_extra.items():
            if key not in payload["metadata"]:
                payload["metadata"][key] = value

    resp = requests.post(url, headers=_headers(), data=json.dumps(payload), timeout=30)
    resp.raise_for_status()
    data = resp.json()
    dep_id = data.get("id")
    logger.info("Depósito criado (id=%s, sandbox=%s)", dep_id, sandbox)
    return data


def get_deposition(deposition_id: int | str, sandbox: bool = False) -> dict[str, Any]:
    """Recupera informações de um depósito existente.

    Args:
        deposition_id: ID numérico do depósito.
        sandbox: Usa o ambiente sandbox.

    Returns:
        Dados do depósito.
    """
    url = f"{get_zenodo_api_url(sandbox)}/deposit/depositions/{deposition_id}"
    resp = requests.get(url, headers=_headers(), timeout=30)
    resp.raise_for_status()
    return resp.json()


def upload_file_to_zenodo(
    deposition_id: int | str,
    file_path: Path,
    sandbox: bool = False,
) -> dict[str, Any]:
    """Faz upload de um arquivo para um depósito Zenodo existente.

    Args:
        deposition_id: ID do depósito.
        file_path: Caminho local do arquivo.
        sandbox: Usa o ambiente sandbox.

    Returns:
        Metadados do arquivo enviado.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    # Obtém o bucket de upload
    dep = get_deposition(deposition_id, sandbox=sandbox)
    bucket_url = dep.get("links", {}).get("bucket")
    if not bucket_url:
        raise RuntimeError("Não foi possível obter o 'bucket' do depósito.")

    file_name = file_path.name
    file_size = file_path.stat().st_size
    logger.info("Enviando '%s' (%d bytes) para depósito %s ...", file_name, file_size, deposition_id)

    upload_url = f"{bucket_url}/{file_name}"
    token = _get_token()
    headers = {"Authorization": f"Bearer {token}"}

    with file_path.open("rb") as f:
        resp = requests.put(upload_url, headers=headers, data=f, timeout=300)
    resp.raise_for_status()
    logger.info("Upload concluído: %s", file_name)
    return resp.json()


def publish_deposition(deposition_id: int | str, sandbox: bool = False) -> dict[str, Any]:
    """Publica um depósito, gerando DOI permanente.

    Args:
        deposition_id: ID do depósito.
        sandbox: Usa o ambiente sandbox.

    Returns:
        Dados do depósito publicado.
    """
    url = f"{get_zenodo_api_url(sandbox)}/deposit/depositions/{deposition_id}/actions/publish"
    resp = requests.post(url, headers=_headers(), timeout=30)
    resp.raise_for_status()
    data = resp.json()
    doi = data.get("metadata", {}).get("prereserve_doi", {}).get("doi") or data.get("doi")
    record_url = data.get("links", {}).get("record_html", data.get("links", {}).get("html"))
    logger.info("Depósito publicado!")
    print(f"\n{'='*60}")
    print(f"DOI:  {doi}")
    print(f"Link: {record_url}")
    print(f"{'='*60}\n")
    return data


def _build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Cria depósitos e faz upload de arquivos no Zenodo.",
    )
    parser.add_argument(
        "--title",
        type=str,
        required=True,
        help="Título do depósito.",
    )
    parser.add_argument(
        "--description",
        type=str,
        required=True,
        help="Descrição / resumo do conteúdo.",
    )
    parser.add_argument(
        "--file",
        type=Path,
        required=True,
        help="Caminho local do arquivo a ser arquivado.",
    )
    parser.add_argument(
        "--creators",
        type=str,
        default='[{"name": "Projeto Migracao Venezuelana Oeste SC", "affiliation": "UFSC / Observatorio das Migracoes"}]',
        help='JSON string com lista de creators (padrão: projeto genérico).',
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Publica o depósito imediatamente após o upload (irreversível).",
    )
    parser.add_argument(
        "--sandbox",
        action="store_true",
        help="Usa o ambiente sandbox do Zenodo (recomendado para testes).",
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

    try:
        creators: list[dict[str, Any]] = json.loads(args.creators)
    except json.JSONDecodeError as exc:
        logger.error("--creators não é um JSON válido: %s", exc)
        return 1

    try:
        dep = create_deposition(
            title=args.title,
            description=args.description,
            creators=creators,
            sandbox=args.sandbox,
        )
        deposition_id = dep["id"]
        upload_file_to_zenodo(deposition_id, args.file, sandbox=args.sandbox)
        if args.publish:
            publish_deposition(deposition_id, sandbox=args.sandbox)
        else:
            print(f"\nDepósito salvo como RASCUNHO (id={deposition_id}).")
            print(f"Acesse: {dep['links']['html']}")
            print("Use --publish para torná-lo permanente.\n")
    except requests.HTTPError as exc:
        logger.error("Erro na API Zenodo: %s", exc)
        return 1
    except (OSError, FileNotFoundError, RuntimeError) as exc:
        logger.error("%s", exc)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
