"""Tests for src/transform/harmonizacao.py and src/transform/anonimizacao.py."""

import hashlib

import pandas as pd
from transform.anonimizacao import aggregate_municipal, hash_column
from transform.harmonizacao import harmonize_geocodes


def test_hash_column_produces_expected_hash():
    """hash_column must return a SHA-256 hex digest for non-null values."""
    salt = "test_salt"
    series = pd.Series(["12345678900", "98765432100", None])
    result = hash_column(series, salt=salt)

    expected_0 = hashlib.sha256(f"12345678900:{salt}".encode()).hexdigest()
    expected_1 = hashlib.sha256(f"98765432100:{salt}".encode()).hexdigest()

    assert result.iloc[0] == expected_0
    assert result.iloc[1] == expected_1
    assert pd.isna(result.iloc[2])


def test_hash_column_preserves_other_columns():
    """hash_column must not alter other columns (it works on Series)."""
    df = pd.DataFrame({"id": [1, 2], "nome": ["Ana", "Bob"]})
    df["nome_hash"] = hash_column(df["nome"], salt="fixed_salt")
    assert list(df["id"]) == [1, 2]
    assert df["nome_hash"].notna().all()


def test_harmonize_geocodes_pads_ibge_codes():
    """harmonize_geocodes should ensure IBGE codes are 7-digit strings by default."""
    series = pd.Series([4205407, "420005", 4201])
    result = harmonize_geocodes(series, target_length=7)

    assert all(isinstance(x, str) or pd.isna(x) for x in result)
    assert result.iloc[0] == "4205407"
    assert result.iloc[1] == "4200050"  # 6-digit code + "0" as DV placeholder
    assert pd.isna(result.iloc[2])  # 4-digit code is invalid (not 6 or 7 digits)


def test_aggregate_municipal_sums_by_municipality():
    """aggregate_municipal should group by municipality and sum numeric columns."""
    df = pd.DataFrame(
        {
            "cod_ibge": ["420005", "420005", "420010"],
            "populacao": [100, 200, 50],
            "casos": [10, 20, 5],
        }
    )
    result = aggregate_municipal(
        df,
        cod_ibge_col="cod_ibge",
        agg_specs={"populacao": "sum", "casos": "sum"},
    )

    assert len(result) == 2
    assert result.set_index("cod_ibge").loc["420005", "populacao"] == 300
    assert result.set_index("cod_ibge").loc["420005", "casos"] == 30
    assert result.set_index("cod_ibge").loc["420010", "populacao"] == 50
