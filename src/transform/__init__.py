"""Módulo de transformação de dados do pipeline ETL.

Este pacote agrupa funções de limpeza, harmonização, anonimização e
enriquecimento dos dados extraídos, preparando-os para análise.

Funções exportadas:
    - Harmonização geográfica e temporal
    - Anonimização de identificadores sensíveis
    - Enriquecimento com classificações setoriais, faixas etárias e índices
"""

from src.transform.harmonizacao import (
    harmonize_geocodes,
    merge_datasets,
    standardize_dates,
)
from src.transform.anonimizacao import (
    aggregate_municipal,
    anonymize_dataframe,
    hash_column,
)
from src.transform.enriquecimento import (
    cnae_to_sector,
    classify_microregion,
    compute_indices,
    cut_age_bins,
)

__all__ = [
    "harmonize_geocodes",
    "standardize_dates",
    "merge_datasets",
    "hash_column",
    "anonymize_dataframe",
    "aggregate_municipal",
    "classify_microregion",
    "cnae_to_sector",
    "cut_age_bins",
    "compute_indices",
]
