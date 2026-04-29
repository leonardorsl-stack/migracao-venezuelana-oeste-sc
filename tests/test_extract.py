"""Mocked tests for src/extract/ modules."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
from extract.pysus_extractor import extract_sih, extract_sim


@patch("extract.pysus_extractor._download_sih")
def test_extract_sih_returns_path(mock_download: MagicMock, tmp_path: Path) -> None:
    """Mocked extraction of SIH (Sistema de Informações Hospitalares) via PySUS."""
    fake_parquet = tmp_path / "sih_2023.parquet"
    fake_parquet.write_text("fake parquet data")
    mock_download.return_value = str(fake_parquet)

    result = extract_sih(uf="SC", year=2023, month=1)

    assert isinstance(result, str | Path)
    mock_download.assert_called_once()


@patch("extract.pysus_extractor._download_sim")
def test_extract_sim_returns_dataframe(mock_download: MagicMock) -> None:
    """Mocked extraction of SIM (Mortality) via PySUS."""
    df = pd.DataFrame({"CAUSABAS": ["I10", "I11"], "DTOBITO": ["01012023", "02012023"]})
    mock_download.return_value = df

    result = extract_sim(uf="SC", year=2023)

    assert isinstance(result, pd.DataFrame)
    assert "CAUSABAS" in result.columns
    mock_download.assert_called_once()
