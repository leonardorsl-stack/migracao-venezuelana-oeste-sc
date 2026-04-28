"""Mocked tests for src/extract/ modules."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from extract.ibge import fetch_municipalities, fetch_population


@patch("extract.ibge.requests.get")
def test_fetch_municipalities_returns_dataframe(mock_get: MagicMock) -> None:
    """fetch_municipalities should return a DataFrame when IBGE API responds."""
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {
            "id": 420005,
            "nome": "Abdon Batista",
            "microrregiao": {
                "mesorregiao": {"UF": {"sigla": "SC"}},
            },
        },
        {
            "id": 420010,
            "nome": "Abelardo Luz",
            "microrregiao": {
                "mesorregiao": {"UF": {"sigla": "SC"}},
            },
        },
    ]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    df = fetch_municipalities(uf="SC")

    assert isinstance(df, pd.DataFrame)
    assert "id" in df.columns
    assert "nome" in df.columns
    assert len(df) == 2
    mock_get.assert_called_once()


@patch("extract.ibge.requests.get")
def test_fetch_municipalities_raises_on_http_error(mock_get: MagicMock) -> None:
    """fetch_municipalities should propagate HTTP errors."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("HTTP 500")
    mock_get.return_value = mock_response

    with pytest.raises(Exception, match="HTTP 500"):
        fetch_municipalities(uf="SC")


@patch("extract.ibge.requests.get")
def test_fetch_population_returns_dataframe(mock_get: MagicMock) -> None:
    """fetch_population should return a DataFrame with population data."""
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {
            "localidade": "420005",
            "res": [{"v": "12345"}],
        }
    ]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    df = fetch_population(codes=["420005"])

    assert isinstance(df, pd.DataFrame)
    assert "localidade" in df.columns
    mock_get.assert_called_once()


@patch("extract.pysus_extractor._download_sih")
def test_extract_sih_returns_path(mock_download: MagicMock, tmp_path: Path) -> None:
    """Mocked extraction of SIH (Sistema de Informações Hospitalares) via PySUS."""
    from extract.pysus_extractor import extract_sih

    fake_parquet = tmp_path / "sih_2023.parquet"
    fake_parquet.write_text("fake parquet data")
    mock_download.return_value = str(fake_parquet)

    result = extract_sih(uf="SC", year=2023, month=1)

    assert isinstance(result, (str, Path))
    mock_download.assert_called_once()


@patch("extract.pysus_extractor._download_sim")
def test_extract_sim_returns_dataframe(mock_download: MagicMock) -> None:
    """Mocked extraction of SIM (Mortality) via PySUS."""
    from extract.pysus_extractor import extract_sim

    df = pd.DataFrame({"CAUSABAS": ["I10", "I11"], "DTOBITO": ["01012023", "02012023"]})
    mock_download.return_value = df

    result = extract_sim(uf="SC", year=2023)

    assert isinstance(result, pd.DataFrame)
    assert "CAUSABAS" in result.columns
    mock_download.assert_called_once()
