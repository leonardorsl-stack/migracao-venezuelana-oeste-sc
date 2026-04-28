"""Tests for src/transform/harmonizacao.py and src/transform/anonimizacao.py."""

import hashlib

import pandas as pd
import pytest

from transform.anonimizacao import hash_column
from transform.harmonizacao import aggregate_municipal, harmonize_geocodes


def test_hash_column_produces_expected_hash():
    """hash_column must return a SHA-256 hex digest for non-null values."""
    df = pd.DataFrame({"cpf": ["12345678900", "98765432100", None]})
    result = hash_column(df, "cpf")

    expected_0 = hashlib.sha256("12345678900".encode("utf-8")).hexdigest()
    expected_1 = hashlib.sha256("98765432100".encode("utf-8")).hexdigest()

    assert result.loc[0, "cpf"] == expected_0
    assert result.loc[1, "cpf"] == expected_1
    assert pd.isna(result.loc[2, "cpf"])


def test_hash_column_preserves_other_columns():
    """hash_column must not alter other columns."""
    df = pd.DataFrame({"id": [1, 2], "nome": ["Ana", "Bob"]})
    result = hash_column(df, "nome")
    assert list(result["id"]) == [1, 2]


def test_harmonize_geocodes_pads_ibge_codes():
    """harmonize_geocodes should ensure IBGE codes are 6-digit strings."""
    df = pd.DataFrame(
        {
            "codigo_municipio": [4201, 4205407, "420005"],
            "nome": ["A", "B", "C"],
        }
    )
    result = harmonize_geocodes(df, col="codigo_municipio")

    assert all(isinstance(x, str) for x in result["codigo_municipio"])
    assert result.loc[0, "codigo_municipio"] == "004201"
    assert result.loc[1, "codigo_municipio"] == "4205407"[:6]
    assert result.loc[2, "codigo_municipio"] == "420005"


def test_aggregate_municipal_sums_by_municipality():
    """aggregate_municipal should group by municipality and sum numeric columns."""
    df = pd.DataFrame(
        {
            "codigo_municipio": ["420005", "420005", "420010"],
            "populacao": [100, 200, 50],
            "casos": [10, 20, 5],
        }
    )
    result = aggregate_municipal(df, by="codigo_municipio", cols=["populacao", "casos"])

    assert len(result) == 2
    assert result.set_index("codigo_municipio").loc["420005", "populacao"] == 300
    assert result.set_index("codigo_municipio").loc["420005", "casos"] == 30
    assert result.set_index("codigo_municipio").loc["420010", "populacao"] == 50
