"""Extração de dados do DataSUS via PySUS."""

from pathlib import Path

import pandas as pd


def _download_sih(uf: str, year: int, month: int) -> str:
    """Chamada interna ao PySUS para SIH."""
    # Placeholder: substituir por pysus.download_sih quando disponível
    raise NotImplementedError("PySUS integration not yet implemented.")


def _download_sim(uf: str, year: int) -> pd.DataFrame:
    """Chamada interna ao PySUS para SIM."""
    # Placeholder: substituir por pysus.download_sim quando disponível
    raise NotImplementedError("PySUS integration not yet implemented.")


def extract_sih(uf: str, year: int, month: int) -> str | Path:
    """Extrai dados do SIH (Sistema de Informações Hospitalares)."""
    return _download_sih(uf, year, month)


def extract_sim(uf: str, year: int) -> pd.DataFrame:
    """Extrai dados do SIM (Sistema de Informação sobre Mortalidade)."""
    return _download_sim(uf, year)
