#!/usr/bin/env python3
"""Download e processamento do CAGED para SC — filtro Venezuela.

STATUS: Pendente download real.
Fonte: FTP do MTE ou portal Novo CAGED.
"""
import logging
from pathlib import Path

import pandas as pd

from src.config import Settings

logger = logging.getLogger(__name__)
settings = Settings()

CAGED_YEARS = list(range(2018, 2025))

def fetch_caged_admissoes(year: int, month: int, uf: str = "SC") -> pd.DataFrame | None:
    """Stub para download do CAGED."""
    logger.warning("CAGED %d-%02d: download não implementado.", year, month)
    return None


def fetch_caged_desligamentos(year: int, month: int, uf: str = "SC") -> pd.DataFrame | None:
    """Stub para download do CAGED."""
    logger.warning("CAGED %d-%02d: download não implementado.", year, month)
    return None


def process_caged_sc(output_dir: Path = None) -> pd.DataFrame | None:
    """Processa CAGED histórico para SC."""
    if output_dir is None:
        output_dir = settings.DATA_RAW / "caged"
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.warning("CAGED: implementação pendente. Requer download manual.")
    return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    process_caged_sc()
