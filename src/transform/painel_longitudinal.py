"""Construção do painel longitudinal municipal (2018–2023).

Este módulo consolida dados de população (IBGE), óbitos (DataSUS/SIM) e
nascimentos (DataSUS/SINASC) em um painel balanceado por município e ano,
preenchendo combinações ausentes com ``NA`` e calculando indicadores
derivados padronizados.

Example:
    >>> from src.transform.painel_longitudinal import construir_painel_municipal_ano
    >>> painel = construir_painel_municipal_ano()
    >>> painel.head()
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
import pandas as pd

from src.analysis.indicadores import (
    calc_obitos_causas_externas,
    calc_percentual_cesareas,
    calc_razao_sexos,
    calc_taxa_mortalidade,
    calc_taxa_natalidade,
)
from src.config import SETTINGS

logger = logging.getLogger(__name__)

# Colunas-chave para o painel
_CHAVE_MUNICIPIO = "codigo_ibge_7d"
_CHAVE_ANO = "ano"
_COL_POPULACAO = "populacao"
_COL_OBITOS = "total_obitos"
_COL_NASCIMENTOS = "total_nascimentos"


def _ler_ibge(path: Path | None = None) -> pd.DataFrame:
    """Lê e padroniza os dados de população estimada do IBGE."""
    if path is None:
        path = SETTINGS.DATA_PROCESSED / "ibge_populacao_estimada_oeste_sc.parquet"

    logger.info("Lendo população IBGE de %s", path)
    df = pd.read_parquet(path)

    # Garante tipos
    df[_CHAVE_MUNICIPIO] = df[_CHAVE_MUNICIPIO].astype(str).str.strip()
    df[_CHAVE_ANO] = pd.to_numeric(df[_CHAVE_ANO], errors="coerce").astype("Int32")

    # Seleciona e renomeia colunas essenciais
    colunas = {c: c for c in df.columns}
    df = df.rename(columns=colunas)

    if _COL_POPULACAO not in df.columns:
        raise KeyError(f"Coluna '{_COL_POPULACAO}' não encontrada no arquivo IBGE.")

    df[_COL_POPULACAO] = pd.to_numeric(df[_COL_POPULACAO], errors="coerce")
    return df


def _ler_sim(path: Path | None = None) -> pd.DataFrame:
    """Lê e padroniza os dados de óbitos do SIM (DataSUS)."""
    if path is None:
        path = SETTINGS.DATA_PROCESSED / "datasus_sim_oeste_sc.parquet"

    logger.info("Lendo óbitos SIM de %s", path)
    df = pd.read_parquet(path)

    # Garante codigo_ibge_7d
    if _CHAVE_MUNICIPIO not in df.columns:
        if "codigo_ibge_7d" in df.columns:
            pass
        elif "CODMUNRES_6" in df.columns:
            df[_CHAVE_MUNICIPIO] = df["CODMUNRES_6"].astype(str).str.zfill(7)
        else:
            raise KeyError("Nenhuma coluna de código IBGE encontrada no SIM.")

    df[_CHAVE_MUNICIPIO] = df[_CHAVE_MUNICIPIO].astype(str).str.strip()
    df[_CHAVE_ANO] = pd.to_numeric(df[_CHAVE_ANO], errors="coerce").astype("Int32")

    if _COL_OBITOS not in df.columns:
        raise KeyError(f"Coluna '{_COL_OBITOS}' não encontrada no arquivo SIM.")

    df[_COL_OBITOS] = pd.to_numeric(df[_COL_OBITOS], errors="coerce").fillna(0)
    return df


def _ler_sinasc(path: Path | None = None) -> pd.DataFrame:
    """Lê e padroniza os dados de nascimentos do SINASC (DataSUS)."""
    if path is None:
        path = SETTINGS.DATA_PROCESSED / "datasus_sinasc_oeste_sc.parquet"

    logger.info("Lendo nascimentos SINASC de %s", path)
    df = pd.read_parquet(path)

    # Garante codigo_ibge_7d
    if _CHAVE_MUNICIPIO not in df.columns:
        if "codigo_ibge_7d" in df.columns:
            pass
        elif "CODMUNRES_6" in df.columns:
            df[_CHAVE_MUNICIPIO] = df["CODMUNRES_6"].astype(str).str.zfill(7)
        else:
            raise KeyError("Nenhuma coluna de código IBGE encontrada no SINASC.")

    df[_CHAVE_MUNICIPIO] = df[_CHAVE_MUNICIPIO].astype(str).str.strip()
    df[_CHAVE_ANO] = pd.to_numeric(df[_CHAVE_ANO], errors="coerce").astype("Int32")

    if _COL_NASCIMENTOS not in df.columns:
        raise KeyError(f"Coluna '{_COL_NASCIMENTOS}' não encontrada no arquivo SINASC.")

    df[_COL_NASCIMENTOS] = pd.to_numeric(df[_COL_NASCIMENTOS], errors="coerce").fillna(0)
    return df


def _criar_grid_completo(
    codigos_municipios: list,
    anos: range,
) -> pd.DataFrame:
    """Cria DataFrame com todas as combinações município × ano."""
    grid = pd.MultiIndex.from_product(
        [codigos_municipios, list(anos)],
        names=[_CHAVE_MUNICIPIO, _CHAVE_ANO],
    ).to_frame(index=False)
    grid[_CHAVE_ANO] = grid[_CHAVE_ANO].astype("Int32")
    return grid


def _calcular_indicadores(painel: pd.DataFrame) -> pd.DataFrame:
    """Calcula indicadores derivados no painel longitudinal."""
    df = painel.copy()

    # Taxa bruta de mortalidade (‰)
    df["taxa_bruta_mortalidade"] = calc_taxa_mortalidade(
        df[_COL_OBITOS], df[_COL_POPULACAO]
    ).round(3)

    # Taxa bruta de natalidade (‰)
    df["taxa_bruta_natalidade"] = calc_taxa_natalidade(
        df[_COL_NASCIMENTOS], df[_COL_POPULACAO]
    ).round(3)

    # Taxa de mortalidade infantil (óbitos 0-1 / nascimentos * 1000)
    if "obitos_faixa_0-1" in df.columns and _COL_NASCIMENTOS in df.columns:
        df["taxa_mortalidade_infantil"] = np.where(
            df[_COL_NASCIMENTOS] > 0,
            df["obitos_faixa_0-1"] / df[_COL_NASCIMENTOS] * 1000,
            np.nan,
        ).round(3)

    # Taxa de fecundidade — necessitaria de população feminina 15-49 anos,
    # dado que não está disponível no painel atual.
    if "pop_feminina_15_49" in df.columns:
        df["taxa_fecundidade"] = np.where(
            df["pop_feminina_15_49"] > 0,
            df[_COL_NASCIMENTOS] / df["pop_feminina_15_49"] * 1000,
            np.nan,
        ).round(3)
    else:
        logger.info(
            "Taxa de fecundidade não calculada: população feminina 15-49 "
            "não disponível no painel."
        )
        df["taxa_fecundidade"] = np.nan

    # Percentual de óbitos por causas externas
    if "top3_causas" in df.columns:
        df["pct_obitos_causas_externas"] = calc_obitos_causas_externas(
            df, df[_COL_OBITOS]
        ).round(2)

    # Razão de sexos ao nascer (se dados agregados disponíveis)
    if "nascimentos_masculino" in df.columns and "nascimentos_feminino" in df.columns:
        df["razao_sexos_nascimento"] = calc_razao_sexos(df).round(2)

    # Percentual de cesáreas
    if "partos_cesarea" in df.columns:
        df["pct_cesareas"] = calc_percentual_cesareas(df).round(2)

    return df


def construir_painel_municipal_ano(
    ibge_path: Path | None = None,
    sim_path: Path | None = None,
    sinasc_path: Path | None = None,
    output_parquet: Path | None = None,
    output_csv: Path | None = None,
) -> pd.DataFrame:
    """Constrói o painel longitudinal municipal consolidado.

    O painel é balanceado para todas as combinações de município (Oeste de SC)
    e ano (2018–2023). Combinações sem dados são preenchidas com ``NA``.

    Args:
        ibge_path: Caminho para população estimada do IBGE.
        sim_path: Caminho para óbitos agregados do SIM.
        sinasc_path: Caminho para nascimentos agregados do SINASC.
        output_parquet: Caminho de saída em Parquet.
        output_csv: Caminho de saída em CSV.

    Returns:
        DataFrame do painel longitudinal.
    """
    if output_parquet is None:
        output_parquet = SETTINGS.DATA_PROCESSED / "painel_oeste_sc_2018_2023.parquet"
    if output_csv is None:
        output_csv = SETTINGS.DATA_PROCESSED / "painel_oeste_sc_2018_2023.csv"

    # 1. Leitura
    df_ibge = _ler_ibge(ibge_path)
    df_sim = _ler_sim(sim_path)
    df_sin = _ler_sinasc(sinasc_path)

    # 2. Grid completo
    codigos = [str(c) for c in SETTINGS.REGIAO_OESTE_SC]
    anos = range(2018, 2024)
    grid = _criar_grid_completo(codigos, anos)
    logger.info("Grid completo: %d combinações município-ano", len(grid))

    # 3. Merge
    painel = grid.merge(df_ibge, on=[_CHAVE_MUNICIPIO, _CHAVE_ANO], how="left")
    painel = painel.merge(df_sim, on=[_CHAVE_MUNICIPIO, _CHAVE_ANO], how="left")
    painel = painel.merge(df_sin, on=[_CHAVE_MUNICIPIO, _CHAVE_ANO], how="left")

    # Remove colunas duplicadas de merge (ex: municipio_y, municipio_x)
    duplicatas = [c for c in painel.columns if c.endswith("_x") or c.endswith("_y")]
    if duplicatas:
        painel = painel.drop(columns=duplicatas)

    # 4. Preenche zeros para contagens ausentes (óbitos/nascimentos = 0 quando não há registro)
    colunas_contagem = [
        _COL_OBITOS,
        _COL_NASCIMENTOS,
        "obitos_masculino",
        "obitos_feminino",
        "obitos_sexo_ignorado",
        "obitos_faixa_60+",
        "obitos_faixa_0-1",
        "obitos_faixa_15-29",
        "obitos_faixa_40-59",
        "obitos_faixa_5-14",
        "obitos_faixa_30-39",
        "obitos_faixa_1-4",
        "nascimentos_masculino",
        "nascimentos_feminino",
        "nascimentos_sexo_ignorado",
        "nascimentos_peso_baixo",
        "nascimentos_peso_normal",
        "nascimentos_mae_adolescente",
        "partos_cesarea",
        "partos_normal",
        "partos_ignorado",
    ]
    for col in colunas_contagem:
        if col in painel.columns:
            painel[col] = pd.to_numeric(painel[col], errors="coerce").fillna(0)

    # 5. Indicadores derivados
    painel = _calcular_indicadores(painel)

    # 6. Ordenação
    painel = painel.sort_values([_CHAVE_MUNICIPIO, _CHAVE_ANO]).reset_index(drop=True)

    # 7. Persistência
    output_parquet.parent.mkdir(parents=True, exist_ok=True)
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    painel.to_parquet(output_parquet, index=False)
    logger.info("Painel salvo em Parquet: %s (%s linhas)", output_parquet, len(painel))

    painel.to_csv(output_csv, index=False)
    logger.info("Painel salvo em CSV: %s", output_csv)

    return painel


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    construir_painel_municipal_ano()
