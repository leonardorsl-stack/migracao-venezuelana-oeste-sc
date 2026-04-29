"""Tests for src/config.py."""

from pathlib import Path

from config import SETTINGS


def test_data_raw_path_exists():
    """Verify that the configured raw data path exists or is a valid Path."""
    assert isinstance(SETTINGS.DATA_RAW, Path)


def test_data_processed_path_exists():
    """Verify that the processed data path exists or is a valid Path."""
    assert isinstance(SETTINGS.DATA_PROCESSED, Path)


def test_regiao_oeste_sc_codes_are_seven_digit_integers():
    """All IBGE municipality codes must be 7-digit integers (109 municipalities)."""
    codes = SETTINGS.REGIAO_OESTE_SC
    assert isinstance(codes, list)
    assert len(codes) == 109, f"Expected 109 municipalities, got {len(codes)}"
    for code in codes:
        assert isinstance(code, int), f"Code {code} is not an integer"
        assert 1000000 <= code <= 9999999, f"Code {code} is not a 7-digit IBGE code"


def test_periodo_analise_is_valid():
    """PERIODO_ANALISE must be a range covering 2018-2026."""
    periodo = SETTINGS.PERIODO_ANALISE
    assert isinstance(periodo, range)
    assert periodo.start == 2018
    assert periodo.stop == 2027
    assert list(periodo) == list(range(2018, 2027))
