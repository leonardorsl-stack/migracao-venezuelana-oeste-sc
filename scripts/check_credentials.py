#!/usr/bin/env python3
"""Diagnóstico de credenciais para serviços externos do projeto.

Verifica se as credenciais configuradas no ``.env`` estão funcionando
fazendo chamadas de teste em OSF, Zenodo e Zotero.

Exemplo::

    python scripts/check_credentials.py
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from typing import Optional

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

# Códigos de cor ANSI básicos
_OK = "\033[92m"
_FAIL = "\033[91m"
_WARN = "\033[93m"
_RESET = "\033[0m"
_BOLD = "\033[1m"


def _print_status(name: str, ok: bool, detail: str = "") -> None:
    symbol = f"{_OK}✓{_RESET}" if ok else f"{_FAIL}✗{_RESET}"
    print(f"  {symbol} {_BOLD}{name}{_RESET}", end="")
    if detail:
        print(f" — {detail}")
    else:
        print()


def _get_env(var: str) -> str:
    return os.getenv(var, "").strip()


def check_osf() -> tuple[bool, str]:
    """Testa a credencial OSF fazendo GET no nó configurado.

    Returns:
        (sucesso, mensagem_detalhe)
    """
    token = _get_env("OSF_TOKEN")
    node_id = _get_env("OSF_NODE_ID")
    if not token:
        return False, "OSF_TOKEN não definido no .env"
    if not node_id:
        return False, "OSF_NODE_ID não definido no .env"

    try:
        url = f"https://api.osf.io/v2/nodes/{node_id}/"
        resp = requests.get(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/vnd.api+json",
            },
            timeout=15,
        )
        resp.raise_for_status()
        title = resp.json().get("data", {}).get("attributes", {}).get("title", "?")
        return True, f"nó '{node_id}' — {title}"
    except requests.HTTPError as exc:
        status = exc.response.status_code if exc.response else "?"
        return False, f"HTTP {status} — verifique o token (escopo osf.full_write?) e o node_id"
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)


def check_zenodo() -> tuple[bool, str]:
    """Testa a credencial Zenodo listando depósitos (espera-se lista vazia ou OK).

    Returns:
        (sucesso, mensagem_detalhe)
    """
    token = _get_env("ZENODO_TOKEN")
    if not token:
        return False, "ZENODO_TOKEN não definido no .env"

    try:
        url = "https://zenodo.org/api/deposit/depositions"
        resp = requests.get(
            url,
            headers={"Authorization": f"Bearer {token}"},
            timeout=15,
        )
        resp.raise_for_status()
        count = len(resp.json())
        return True, f"{count} depósito(s) visível(eis)"
    except requests.HTTPError as exc:
        status = exc.response.status_code if exc.response else "?"
        return False, f"HTTP {status} — verifique o token"
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)


def check_zotero() -> tuple[bool, str]:
    """Testa a credencial Zotero obtendo informações do usuário.

    Returns:
        (sucesso, mensagem_detalhe)
    """
    api_key = _get_env("ZOTERO_API_KEY")
    user_id = _get_env("ZOTERO_USER_ID")
    if not api_key:
        return False, "ZOTERO_API_KEY não definido no .env"
    if not user_id:
        return False, "ZOTERO_USER_ID não definido no .env"
    if not user_id.isdigit():
        return (
            False,
            f"ZOTERO_USER_ID ('{user_id}') não parece ser um ID numérico — "
            "o valor correto está em https://www.zotero.org/settings/keys",
        )

    try:
        url = f"https://api.zotero.org/users/{user_id}/items"
        resp = requests.get(
            url,
            headers={
                "Zotero-API-Key": api_key,
                "Zotero-API-Version": "3",
            },
            params={"limit": 1},
            timeout=15,
        )
        resp.raise_for_status()
        # Tenta extrair o nome do usuário pelo header (se presente)
        name = resp.headers.get("Zotero-User-Name", "usuário OK")
        return True, f"{name} (user_id={user_id})"
    except requests.HTTPError as exc:
        status = exc.response.status_code if exc.response else "?"
        return False, f"HTTP {status} — verifique a API key e o user_id"
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)


def main(argv: Optional[list[str]] = None) -> int:
    logging.basicConfig(level=logging.WARNING)

    print(f"\n{_BOLD}=== Verificação de Credenciais ==={_RESET}\n")

    ok_count = 0
    total = 3

    ok, detail = check_osf()
    _print_status("OSF", ok, detail)
    ok_count += int(ok)

    ok, detail = check_zenodo()
    _print_status("Zenodo", ok, detail)
    ok_count += int(ok)

    ok, detail = check_zotero()
    _print_status("Zotero", ok, detail)
    ok_count += int(ok)

    print(f"\n{_BOLD}Resumo:{_RESET} {ok_count}/{total} serviços OK")
    if ok_count < total:
        print(
            f"{_WARN}  Dica:{_RESET} revise o arquivo ``.env`` na raiz do projeto. "
            "Certifique-se de que os tokens estão corretos e possuem os escopos necessários.\n"
        )
        return 1
    print(f"{_OK}Todas as credenciais estão funcionando corretamente.{_RESET}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
