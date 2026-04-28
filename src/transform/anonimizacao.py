"""Funções de anonimização de dados sensíveis para proteção de identidade.

Este módulo implementa técnicas de anonimização aplicáveis a microdados
administrativos (RAIS, CAGED, DataSUS, SED/SC), garantindo conformidade com
a LGPD e boas práticas de pesquisa com dados pessoais.

As técnicas incluem:
    - Hash criptográfico (SHA-256 com salt) de identificadores diretos
    - Remoção/agregação de quasi-identificadores
    - Agregação municipal para supressão de células pequenas

Example:
    >>> from src.transform.anonimizacao import hash_column, anonymize_dataframe
    >>> df["id_hash"] = hash_column(df["cpf"], salt="projeto_migracao_sc")
    >>> df_anon = anonymize_dataframe(df, drop=["cpf", "nome", "endereco"])
"""

from __future__ import annotations

import hashlib
import logging
import secrets
from typing import List, Optional

import pandas as pd

from src.config import SETTINGS

logger = logging.getLogger(__name__)


def hash_column(
    series: pd.Series,
    salt: Optional[str] = None,
    algorithm: str = "sha256",
) -> pd.Series:
    """Aplica hash criptográfico a uma série de identificadores.

    Cada valor é concatenado com um salt fixo e processado pelo algoritmo
    escolhido, produzindo um identificador pseudônimo irreversível.

    Args:
        series: Série pandas com identificadores (CPF, nome, etc.).
        salt: String de salt para dificultar ataques de rainbow table.
            Se ``None``, gera um salt aleatório (aviso: não será
            reprodutível entre execuções).
        algorithm: Algoritmo de hash (``sha256``, ``sha512``, ``blake2b``).

    Returns:
        Série de strings hexadecimais com o hash de cada valor.

    Raises:
        ValueError: Se o algoritmo não for suportado.
    """
    if salt is None:
        salt = secrets.token_hex(16)
        logger.warning(
            "Salt não fornecido. Gerado salt aleatório (não reprodutível): %s",
            salt,
        )

    hasher = getattr(hashlib, algorithm, None)
    if hasher is None:
        raise ValueError(f"Algoritmo de hash não suportado: {algorithm}")

    def _hash(value) -> Optional[str]:
        if pd.isna(value) or str(value).strip() == "":
            return None
        payload = f"{str(value).strip()}:{salt}"
        return hasher(payload.encode("utf-8")).hexdigest()

    return series.apply(_hash)


def anonymize_dataframe(
    df: pd.DataFrame,
    drop: Optional[List[str]] = None,
    hash_map: Optional[dict] = None,
    salt: Optional[str] = None,
    min_group_size: int = 5,
) -> pd.DataFrame:
    """Anonimiza um DataFrame removendo e/ou hasheando colunas sensíveis.

    Args:
        df: DataFrame de entrada com possíveis identificadores diretos.
        drop: Lista de nomes de colunas a serem removidas completamente.
        hash_map: Dicionário ``{coluna_original: nome_novo}`` indicando
            colunas que devem ser substituídas por seu hash.
        salt: Salt para hash. Padrão: ``None`` (gera aleatório).
        min_group_size: Tamanho mínimo de grupo para manter registro.
            Grupos menores são agregados ou removidos (k-anonimato
            básico por supressão de célula).

    Returns:
        DataFrame anonimizado.
    """
    df_out = df.copy()

    if drop:
        missing = [c for c in drop if c not in df_out.columns]
        if missing:
            logger.warning("Colunas para drop não encontradas: %s", missing)
        cols_to_drop = [c for c in drop if c in df_out.columns]
        df_out = df_out.drop(columns=cols_to_drop)
        logger.info("Colunas removidas: %s", cols_to_drop)

    if hash_map:
        for old_col, new_col in hash_map.items():
            if old_col not in df_out.columns:
                logger.warning("Coluna %s não encontrada para hash.", old_col)
                continue
            df_out[new_col] = hash_column(df_out[old_col], salt=salt)
            df_out = df_out.drop(columns=[old_col])
            logger.info("Coluna %s substituída por hash em %s.", old_col, new_col)

    # Supressão básica de células pequenas por município (exemplo)
    if "cod_ibge" in df_out.columns and min_group_size > 1:
        counts = df_out.groupby("cod_ibge").size()
        small = counts[counts < min_group_size].index.tolist()
        if small:
            logger.info(
                "Suprimindo %s municípios com menos de %s registros.",
                len(small),
                min_group_size,
            )
            df_out = df_out[~df_out["cod_ibge"].isin(small)]

    return df_out


def aggregate_municipal(
    df: pd.DataFrame,
    cod_ibge_col: str = "cod_ibge",
    agg_specs: Optional[dict] = None,
) -> pd.DataFrame:
    """Agrega microdados ao nível municipal para anonimização.

    Substitui identificadores individuais por estatísticas agregadas por
    município, eliminando risco de reidentificação.

    Args:
        df: DataFrame com microdados.
        cod_ibge_col: Nome da coluna de código IBGE.
        agg_specs: Dicionário de agregação no formato ``{coluna: funcao}``.
            Se ``None``, utiliza contagens e somas padrão.

    Returns:
        DataFrame agregado por município.
    """
    if cod_ibge_col not in df.columns:
        raise KeyError(f"Coluna {cod_ibge_col} não encontrada no DataFrame.")

    if agg_specs is None:
        # Detecta colunas numéricas automaticamente
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        numeric_cols = [c for c in numeric_cols if c != cod_ibge_col]
        agg_specs = {c: ["sum", "mean", "count"] for c in numeric_cols}
        agg_specs.setdefault("registros", "size")

    logger.info("Agregando dados por %s com specs: %s", cod_ibge_col, agg_specs)
    grouped = df.groupby(cod_ibge_col).agg(agg_specs)
    grouped.columns = [
        "_".join(col).strip("_") if isinstance(col, tuple) else col
        for col in grouped.columns.values
    ]
    grouped = grouped.reset_index()
    return grouped
