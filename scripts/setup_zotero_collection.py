#!/usr/bin/env python3
"""
Script simples para criar a coleção "Migracao Venezuelana SC" no Zotero pessoal.

Uso:
    python scripts/setup_zotero_collection.py
    python scripts/setup_zotero_collection.py --name "Outra Coleção"

Retorna a collection key no stdout (útil para pipelines).
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("setup_zotero_collection")

ZOTERO_API_BASE = "https://api.zotero.org"
DEFAULT_COLLECTION_NAME = "Migracao Venezuelana SC"


def _zotero_headers(api_key: str) -> dict[str, str]:
    return {
        "Zotero-API-Key": api_key,
        "Content-Type": "application/json",
    }


def get_zotero_credentials() -> tuple[str, str | None]:
    """Lê ZOTERO_API_KEY e ZOTERO_USER_ID do .env."""
    load_dotenv()
    api_key = os.getenv("ZOTERO_API_KEY", "").strip()
    user_id = os.getenv("ZOTERO_USER_ID", "").strip() or None
    if not api_key:
        raise RuntimeError("ZOTERO_API_KEY não encontrada no .env")
    return api_key, user_id


def get_user_id(api_key: str, fallback: str | None = None) -> str:
    """
    Descobre o userID numérico via endpoint /keys/current.
    Em caso de falha, usa o fallback.
    """
    url = f"{ZOTERO_API_BASE}/keys/current"
    try:
        resp = requests.get(url, headers={"Zotero-API-Key": api_key}, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        user_id = data.get("userID")
        if user_id is not None:
            user_id_str = str(user_id).strip()
            logger.info("UserID descoberto via API: %s", user_id_str)
            return user_id_str
    except Exception as exc:
        logger.warning("Não foi possível descobrir userID via API: %s", exc)

    if fallback:
        logger.info("Usando ZOTERO_USER_ID do .env: %s", fallback)
        return fallback
    raise RuntimeError("Não foi possível obter userID e não há fallback no .env")


def get_collections(api_key: str, user_id: str) -> list[dict[str, Any]]:
    """Lista todas as coleções do usuário."""
    url = f"{ZOTERO_API_BASE}/users/{user_id}/collections"
    headers = _zotero_headers(api_key)
    collections: list[dict[str, Any]] = []
    start = 0
    limit = 100

    while True:
        resp = requests.get(url, headers=headers, params={"start": start, "limit": limit}, timeout=30)
        resp.raise_for_status()
        page = resp.json()
        if not page:
            break
        collections.extend(page)
        if len(page) < limit:
            break
        start += limit

    return collections


def create_collection(api_key: str, user_id: str, name: str) -> dict[str, Any]:
    """Cria uma coleção no Zotero e retorna os dados da resposta."""
    url = f"{ZOTERO_API_BASE}/users/{user_id}/collections"
    payload = [{"name": name, "parentCollection": False}]
    resp = requests.post(url, headers=_zotero_headers(api_key), json=payload, timeout=30)
    resp.raise_for_status()

    result = resp.json()
    success_data = result.get("successful", {})
    first = success_data.get("0", {})
    collection_key = first.get("key")

    logger.info("Coleção '%s' criada com sucesso (key=%s)", name, collection_key)
    return {"name": name, "key": collection_key, "data": first}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Cria coleção Zotero para o projeto")
    parser.add_argument(
        "--name",
        default=DEFAULT_COLLECTION_NAME,
        help=f"Nome da coleção (padrão: '{DEFAULT_COLLECTION_NAME}')",
    )
    args = parser.parse_args(argv)

    api_key, fallback_user_id = get_zotero_credentials()
    user_id = get_user_id(api_key, fallback=fallback_user_id)

    # Verifica se já existe
    collections = get_collections(api_key, user_id)
    existing = next((c for c in collections if c.get("data", {}).get("name") == args.name), None)
    if existing:
        collection_key = existing["key"]
        logger.info("Coleção '%s' já existe (key=%s)", args.name, collection_key)
        print(collection_key)
        return 0

    result = create_collection(api_key, user_id, args.name)
    collection_key = result.get("key")
    if collection_key:
        print(collection_key)
    else:
        # Fallback: lista coleções novamente para pegar a key
        collections = get_collections(api_key, user_id)
        new_col = next(
            (c for c in collections if c.get("data", {}).get("name") == args.name), None
        )
        if new_col:
            print(new_col["key"])
        else:
            logger.error("Não foi possível determinar a key da nova coleção")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
