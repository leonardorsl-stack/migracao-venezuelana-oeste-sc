#!/usr/bin/env python3
"""
Sincronização de bibliografia BibTeX com Zotero (API v3).

Uso:
    python scripts/sync_zotero.py
    python scripts/sync_zotero.py --bib-file references.bib --collection "Migracao Venezuelana SC"
    python scripts/sync_zotero.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any

import bibtexparser
import requests
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuração de logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("zotero_sync")

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------
ZOTERO_API_BASE = "https://api.zotero.org"
DEFAULT_BIB_FILE = Path("references.bib")
DEFAULT_COLLECTION = "Migracao Venezuelana SC"
WRITE_DELAY_SECONDS = 1.0  # Zotero limita writes a ~1 req/s

# Mapeamento simplificado BibTeX -> Zotero itemType
BIBTEX_TO_ZOTERO_TYPE = {
    "article": "journalArticle",
    "book": "book",
    "inbook": "bookSection",
    "incollection": "bookSection",
    "inproceedings": "conferencePaper",
    "conference": "conferencePaper",
    "techreport": "report",
    "report": "report",
    "mastersthesis": "thesis",
    "phdthesis": "thesis",
    "thesis": "thesis",
    "unpublished": "manuscript",
    "misc": "document",
    "booklet": "document",
    "manual": "document",
    "proceedings": "conferencePaper",
}


def _zotero_headers(api_key: str) -> dict[str, str]:
    return {
        "Zotero-API-Key": api_key,
        "Content-Type": "application/json",
    }


# ---------------------------------------------------------------------------
# Credenciais
# ---------------------------------------------------------------------------
def get_zotero_credentials() -> tuple[str, str | None]:
    """
    Lê credenciais do Zotero do arquivo .env.

    Returns:
        (api_key, user_id_or_username)
    """
    load_dotenv()
    api_key = os.getenv("ZOTERO_API_KEY", "").strip()
    user_id = os.getenv("ZOTERO_USER_ID", "").strip() or None
    if not api_key:
        raise RuntimeError("ZOTERO_API_KEY não encontrada no .env")
    return api_key, user_id


def get_user_id(api_key: str, fallback: str | None = None) -> str:
    """
    Descobre o userID numérico via endpoint /keys/current da API Zotero.

    Se a requisição falhar, retorna *fallback* ou levanta erro.
    """
    url = f"{ZOTERO_API_BASE}/keys/current"
    try:
        resp = requests.get(url, headers={"Zotero-API-Key": api_key}, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as exc:
        logger.warning("Não foi possível consultar /keys/current: %s", exc)
        if fallback:
            logger.info("Usando ZOTERO_USER_ID do .env: %s", fallback)
            return fallback
        raise RuntimeError("Não foi possível obter userID e não há fallback no .env") from exc

    # O endpoint retorna JSON
    try:
        data = resp.json()
        user_id = data.get("userID")
        if user_id is not None:
            user_id_str = str(user_id).strip()
            logger.info("UserID descoberto via API: %s", user_id_str)
            return user_id_str
    except json.JSONDecodeError as exc:
        logger.warning("Falha ao parsear JSON de /keys/current: %s", exc)

    if fallback:
        logger.info("Usando ZOTERO_USER_ID do .env: %s", fallback)
        return fallback
    raise RuntimeError("Não foi possível obter userID e não há fallback no .env")


# ---------------------------------------------------------------------------
# Parsing BibTeX
# ---------------------------------------------------------------------------
def parse_bibtex(file_path: Path) -> list[dict[str, Any]]:
    """
    Lê um arquivo .bib e retorna lista de entradas BibTeX como dicts.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    with file_path.open("r", encoding="utf-8") as fh:
        db = bibtexparser.load(fh)

    entries = []
    for entry in db.entries:
        # bibtexparser normaliza chaves para minúsculas
        entries.append(dict(entry))
    logger.info("%d entradas lidas de %s", len(entries), file_path)
    return entries


# ---------------------------------------------------------------------------
# Conversão BibTeX -> Zotero JSON
# ---------------------------------------------------------------------------
def _parse_author_field(author_str: str) -> list[dict[str, str]]:
    """
    Converte campo 'author' BibTeX em lista de creators Zotero.
    """
    creators: list[dict[str, str]] = []
    if not author_str:
        return creators

    # Separa por ' and ' (padrão BibTeX)
    raw_names = [n.strip() for n in author_str.replace("\n", " ").split(" and ")]
    for name in raw_names:
        if not name:
            continue
        # Formato BibTeX: "Sobrenome, Nome" ou "Nome Sobrenome"
        if "," in name:
            parts = [p.strip() for p in name.split(",", 1)]
            creators.append({"creatorType": "author", "lastName": parts[0], "firstName": parts[1]})
        else:
            # Heurística simples: última palavra = sobrenome
            parts = name.split()
            if len(parts) == 1:
                creators.append({"creatorType": "author", "lastName": parts[0], "firstName": ""})
            else:
                creators.append(
                    {
                        "creatorType": "author",
                        "lastName": parts[-1],
                        "firstName": " ".join(parts[:-1]),
                    }
                )
    return creators


def item_to_zotero_json(bib_entry: dict[str, Any]) -> dict[str, Any]:
    """
    Converte uma entrada BibTeX para o formato JSON esperado pela API Zotero.
    """
    bib_type = bib_entry.get("ENTRYTYPE", "misc").lower()
    item_type = BIBTEX_TO_ZOTERO_TYPE.get(bib_type, "document")

    data: dict[str, Any] = {
        "itemType": item_type,
        "title": bib_entry.get("title", ""),
        "abstractNote": bib_entry.get("abstract", ""),
        "date": bib_entry.get("year", ""),
        "url": bib_entry.get("url", ""),
        "DOI": bib_entry.get("doi", ""),
        "language": bib_entry.get("language", "pt-BR"),
        "extra": "",
    }

    # Autores
    authors = _parse_author_field(bib_entry.get("author", ""))
    if authors:
        data["creators"] = authors

    # Campos específicos por tipo
    if item_type == "journalArticle":
        data["publicationTitle"] = bib_entry.get("journal", "")
        data["volume"] = bib_entry.get("volume", "")
        data["issue"] = bib_entry.get("number", "")
        data["pages"] = bib_entry.get("pages", "")
        data["ISSN"] = bib_entry.get("issn", "")
    elif item_type == "book":
        data["publisher"] = bib_entry.get("publisher", "")
        data["place"] = bib_entry.get("address", "")
        data["ISBN"] = bib_entry.get("isbn", "")
        data["edition"] = bib_entry.get("edition", "")
        # Tradutor
        if bib_entry.get("translator"):
            translators = _parse_author_field(bib_entry["translator"])
            for t in translators:
                t["creatorType"] = "translator"
            data.setdefault("creators", []).extend(translators)
    elif item_type == "report":
        data["institution"] = bib_entry.get("institution", "")
        data["place"] = bib_entry.get("address", "")
        data["reportType"] = bib_entry.get("type", "")
        data["reportNumber"] = bib_entry.get("number", "")
    elif item_type == "thesis":
        data["university"] = bib_entry.get("school", "")
        data["place"] = bib_entry.get("address", "")
        data["thesisType"] = bib_entry.get("type", "")

    # Keywords -> tags
    keywords = bib_entry.get("keywords", "")
    if keywords:
        data["tags"] = [{"tag": k.strip()} for k in keywords.split(",") if k.strip()]

    # Notas extras
    extra_parts: list[str] = []
    if bib_entry.get("note"):
        extra_parts.append(bib_entry["note"])
    if bib_entry.get("originaltitle"):
        extra_parts.append(f"Título original: {bib_entry['originaltitle']}")
    if bib_entry.get("originalyear"):
        extra_parts.append(f"Ano original: {bib_entry['originalyear']}")
    if extra_parts:
        data["extra"] = "\n".join(extra_parts)

    return {"itemType": item_type, **data}


# ---------------------------------------------------------------------------
# Operações na API Zotero
# ---------------------------------------------------------------------------
def get_collections(api_key: str, user_id: str) -> list[dict[str, Any]]:
    """
    Retorna todas as coleções do usuário.
    """
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


def create_collection(
    api_key: str, user_id: str, name: str, parent_key: str | None = None
) -> dict[str, Any]:
    """
    Cria uma nova coleção no Zotero e retorna o objeto criado.
    """
    url = f"{ZOTERO_API_BASE}/users/{user_id}/collections"
    payload: list[dict[str, Any]] = [{"name": name, "parentCollection": parent_key or False}]
    resp = requests.post(url, headers=_zotero_headers(api_key), json=payload, timeout=30)
    resp.raise_for_status()
    result = resp.json()
    # A resposta vem com successful -> {"0": {"key": "...", ...}}
    success_data = result.get("successful", {})
    first = success_data.get("0", {})
    collection_key = first.get("key")
    logger.info("Coleção '%s' criada (key=%s)", name, collection_key)
    time.sleep(WRITE_DELAY_SECONDS)
    return {"name": name, "key": collection_key, "data": first}


def get_collection_items(
    api_key: str, user_id: str, collection_key: str
) -> list[dict[str, Any]]:
    """
    Retorna todos os itens de uma coleção.
    """
    url = f"{ZOTERO_API_BASE}/users/{user_id}/collections/{collection_key}/items"
    headers = _zotero_headers(api_key)
    items: list[dict[str, Any]] = []
    start = 0
    limit = 100

    while True:
        resp = requests.get(url, headers=headers, params={"start": start, "limit": limit}, timeout=30)
        resp.raise_for_status()
        page = resp.json()
        if not page:
            break
        items.extend(page)
        if len(page) < limit:
            break
        start += limit

    return items


def create_or_update_item(
    api_key: str,
    user_id: str,
    item_json: dict[str, Any],
    collection_key: str | None = None,
) -> dict[str, Any]:
    """
    Cria um novo item no Zotero.

    Se *collection_key* for fornecido, o item será associado àquela coleção.
    """
    url = f"{ZOTERO_API_BASE}/users/{user_id}/items"
    payload = [item_json]
    if collection_key:
        item_json.setdefault("collections", []).append(collection_key)

    resp = requests.post(url, headers=_zotero_headers(api_key), json=payload, timeout=30)
    resp.raise_for_status()
    time.sleep(WRITE_DELAY_SECONDS)
    return {"status": resp.status_code, "headers": dict(resp.headers), "body": resp.text}


# ---------------------------------------------------------------------------
# Fluxo completo de sincronização
# ---------------------------------------------------------------------------
def sync_bibtex_to_zotero(
    bib_path: Path,
    collection_name: str = DEFAULT_COLLECTION,
    dry_run: bool = False,
) -> dict[str, Any]:
    """
    Fluxo completo:
      1. Descobre credenciais e userID.
      2. Lê o .bib.
      3. Cria coleção se não existir.
      4. Converte entradas e envia para Zotero (evitando duplicatas por título).
    """
    api_key, fallback_user_id = get_zotero_credentials()
    user_id = get_user_id(api_key, fallback=fallback_user_id)

    entries = parse_bibtex(bib_path)
    if not entries:
        logger.warning("Nenhuma entrada encontrada em %s", bib_path)
        return {"created": 0, "skipped": 0, "errors": 0, "collection_key": None}

    # --- Coleção ---
    collections = get_collections(api_key, user_id)
    collection = next((c for c in collections if c.get("data", {}).get("name") == collection_name), None)
    collection_key: str | None = None

    if collection:
        collection_key = collection["key"]
        logger.info("Coleção '%s' já existe (key=%s)", collection_name, collection_key)
    else:
        if dry_run:
            logger.info("[DRY-RUN] Criaria coleção '%s'", collection_name)
        else:
            new_col = create_collection(api_key, user_id, collection_name)
            collection_key = new_col.get("key")
            if not collection_key:
                # Fallback: buscar novamente após criação
                collections = get_collections(api_key, user_id)
                new_col_obj = next(
                    (c for c in collections if c.get("data", {}).get("name") == collection_name),
                    None,
                )
                if new_col_obj:
                    collection_key = new_col_obj["key"]
            logger.info("Coleção '%s' criada (key=%s)", collection_name, collection_key)

    # --- Duplicatas ---
    existing_titles: set[str] = set()
    if collection_key and not dry_run:
        existing_items = get_collection_items(api_key, user_id, collection_key)
        for it in existing_items:
            title = it.get("data", {}).get("title", "").strip().lower()
            if title:
                existing_titles.add(title)
        logger.info("%d itens já existentes na coleção", len(existing_titles))

    created = 0
    skipped = 0
    errors = 0

    for entry in entries:
        item_json = item_to_zotero_json(entry)
        title = item_json.get("title", "").strip()
        title_lower = title.lower()

        if title_lower in existing_titles:
            logger.info("[SKIP] Item já existe na coleção: %s", title)
            skipped += 1
            continue

        if dry_run:
            logger.info("[DRY-RUN] Criaria item: %s", title)
            created += 1
            continue

        try:
            create_or_update_item(api_key, user_id, item_json, collection_key=collection_key)
            if title_lower:
                existing_titles.add(title_lower)
            logger.info("[OK] Item criado: %s", title)
            created += 1
        except requests.HTTPError as exc:
            logger.error("[ERRO] Falha ao criar '%s': %s", title, exc)
            errors += 1
        except Exception as exc:
            logger.error("[ERRO] Exceção inesperada para '%s': %s", title, exc)
            errors += 1

    summary = {
        "created": created,
        "skipped": skipped,
        "errors": errors,
        "collection_key": collection_key,
    }
    logger.info("Resumo da sincronização: %s", summary)
    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sincroniza references.bib com Zotero")
    parser.add_argument(
        "--bib-file",
        type=Path,
        default=DEFAULT_BIB_FILE,
        help=f"Caminho para o arquivo .bib (padrão: {DEFAULT_BIB_FILE})",
    )
    parser.add_argument(
        "--collection",
        default=DEFAULT_COLLECTION,
        help=f"Nome da coleção Zotero (padrão: '{DEFAULT_COLLECTION}')",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula a execução sem enviar dados para o Zotero",
    )
    args = parser.parse_args(argv)

    sync_bibtex_to_zotero(
        bib_path=args.bib_file,
        collection_name=args.collection,
        dry_run=args.dry_run,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
