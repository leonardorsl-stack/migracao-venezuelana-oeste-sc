"""Tests for src/config.py."""

from pathlib import Path

import pytest

from config import (
    PERIODO_ANALISE,
    REGIAO_OESTE_SC,
)


def test_data_raw_path_exists():
    """Verify that the configured raw data path exists or is a valid Path."""
    from config import DATA_RAW

    assert isinstance(DATA_RAW, Path)


def test_data_processed_path_exists():
    """Verify that the configured processed data path exists or is a valid Path."""
    from config import DATA_PROCESSED

    assert isinstance(DATA_PROCESSED, Path)


def test_regiao_oeste_sc_codes_are_six_digits():
    """All IBGE municipality codes must be exactly 6 digits."""
    assert isinstance(REGIAO_OESTE_SC, list)
    assert len(REGIAO_OESTE_SC) > 0
    for code in REGIAO_OESTE_SC:
        assert isinstance(code, str), f"Code {code} is not a string"
        assert code.isdigit(), f"Code {code} is not numeric"
        assert len(code) == 6, f"Code {code} does not have 6 digits"


def test_periodo_analise_is_valid():
    """PERIODO_ANALISE must be a tuple of two integers (start, end) with start <= end."""
    assert isinstance(PERIODO_ANALISE, tuple)
    assert len(PERIODO_ANALISE) == 2
    start, end = PERIODO_ANALISE
    assert isinstance(start, int)
    assert isinstance(end, int)
    assert start <= end
