"""Funções de cálculo de indicadores demográficos e de saúde.

Este módulo implementa as fórmulas padronizadas para taxas brutas de
mortalidade/natalidade, razão de sexos, média de idade da mãe,
percentual de cesáreas e óbitos por causas externas.

Todas as funções aceitam tanto escalares (int/float) quanto
`pd.Series`, retornando o mesmo tipo da entrada.

Example:
    >>> from src.analysis.indicadores import calc_taxa_mortalidade
    >>> calc_taxa_mortalidade(150, 10000)
    15.0
"""

from __future__ import annotations

import logging
from typing import Union

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

NumericOrSeries = Union[int, float, pd.Series]


def _safe_divide(numerator: NumericOrSeries, denominator: NumericOrSeries) -> NumericOrSeries:
    """Divisão segura que retorna 0 quando denominador é 0 ou NaN."""
    if isinstance(numerator, pd.Series) or isinstance(denominator, pd.Series):
        num = pd.Series(numerator)
        den = pd.Series(denominator)
        return np.where(den > 0, num / den, 0.0)
    return numerator / denominator if denominator > 0 else 0.0


def calc_taxa_mortalidade(obitos: NumericOrSeries, populacao: NumericOrSeries) -> NumericOrSeries:
    """Calcula a taxa bruta de mortalidade (‰).

    Fórmula: (óbitos / população) * 1000

    Args:
        obitos: Número de óbitos.
        populacao: População residente.

    Returns:
        Taxa bruta de mortalidade por mil habitantes.
    """
    return _safe_divide(obitos, populacao) * 1000


def calc_taxa_natalidade(nascimentos: NumericOrSeries, populacao: NumericOrSeries) -> NumericOrSeries:
    """Calcula a taxa bruta de natalidade (‰).

    Fórmula: (nascimentos vivos / população) * 1000

    Args:
        nascimentos: Número de nascimentos vivos.
        populacao: População residente.

    Returns:
        Taxa bruta de natalidade por mil habitantes.
    """
    return _safe_divide(nascimentos, populacao) * 1000


def calc_razao_sexos(sinasc_df: pd.DataFrame) -> NumericOrSeries:
    """Calcula a razão de sexos ao nascer (homens por 100 mulheres).

    A função aceita tanto microdados (com coluna ``SEXO`` ou ``sexo``)
    quanto dados agregados (com colunas ``nascimentos_masculino`` e
    ``nascimentos_feminino``).

    Args:
        sinasc_df: DataFrame com dados do SINASC.

    Returns:
        Razão de sexos (homens / mulheres * 100). Retorna ``NaN`` quando
        não há mulheres ou quando as colunas necessárias não existem.
    """
    if "nascimentos_masculino" in sinasc_df.columns and "nascimentos_feminino" in sinasc_df.columns:
        homens = sinasc_df["nascimentos_masculino"]
        mulheres = sinasc_df["nascimentos_feminino"]
        return np.where(mulheres > 0, homens / mulheres * 100, np.nan)

    # Fallback para microdados
    sexo_col = "SEXO" if "SEXO" in sinasc_df.columns else "sexo" if "sexo" in sinasc_df.columns else None
    if sexo_col is None:
        logger.warning("Coluna de sexo não encontrada em sinasc_df.")
        return np.nan

    homens = (sinasc_df[sexo_col] == 1).sum() if isinstance(sinasc_df, pd.DataFrame) else np.nan
    mulheres = (sinasc_df[sexo_col] == 2).sum() if isinstance(sinasc_df, pd.DataFrame) else np.nan
    if isinstance(sinasc_df, pd.DataFrame) and mulheres == 0:
        return np.nan
    return homens / mulheres * 100


def calc_media_idade_mae(sinasc_df: pd.DataFrame) -> float:
    """Calcula a média de idade da mãe.

    Args:
        sinasc_df: DataFrame com dados do SINASC. Deve conter a coluna
            ``IDADEMAE`` ou ``idademae``.

    Returns:
        Média de idade da mãe. Retorna ``np.nan`` quando a coluna não
        existe ou não há registros válidos.
    """
    idade_col = "IDADEMAE" if "IDADEMAE" in sinasc_df.columns else "idademae" if "idademae" in sinasc_df.columns else None
    if idade_col is None:
        logger.warning("Coluna de idade da mãe não encontrada em sinasc_df.")
        return np.nan

    idades = pd.to_numeric(sinasc_df[idade_col], errors="coerce")
    idades = idades[(idades >= 10) & (idades <= 60)]  # filtro biológico
    if idades.empty:
        return np.nan
    return float(idades.mean())


def calc_percentual_cesareas(sinasc_df: pd.DataFrame) -> NumericOrSeries:
    """Calcula o percentual de partos cesáreos.

    Aceita dados agregados (colunas ``partos_cesarea`` e ``partos_normal``)
    ou microdados (coluna ``PARTO`` / ``parto``).

    Args:
        sinasc_df: DataFrame com dados do SINASC.

    Returns:
        Percentual de cesáreas (0–100). Retorna ``NaN`` quando não há
        partos válidos ou colunas ausentes.
    """
    if "partos_cesarea" in sinasc_df.columns and "partos_normal" in sinasc_df.columns:
        total = sinasc_df["partos_cesarea"] + sinasc_df["partos_normal"]
        return np.where(total > 0, sinasc_df["partos_cesarea"] / total * 100, np.nan)

    parto_col = "PARTO" if "PARTO" in sinasc_df.columns else "parto" if "parto" in sinasc_df.columns else None
    if parto_col is None:
        logger.warning("Coluna de tipo de parto não encontrada em sinasc_df.")
        return np.nan

    total = sinasc_df[parto_col].notna().sum()
    cesareas = (sinasc_df[parto_col] == 2).sum()
    return cesareas / total * 100 if total > 0 else np.nan


def calc_obitos_causas_externas(sim_df: pd.DataFrame, total_obitos: NumericOrSeries) -> NumericOrSeries:
    """Calcula o percentual de óbitos por causas externas (acidentes/violência).

    No DataSUS, causas externas correspondem ao capítulo CID-10 **V01-Y98**.
    A função tenta extrair a contagem a partir das colunas agregadas
    ``top3_causas`` / ``top3_causas_n`` ou, em microdados, da coluna
    ``CAUSABAS``.

    Args:
        sim_df: DataFrame com dados do SIM (agregado ou microdados).
        total_obitos: Total de óbitos (escalar ou série). Usado como
            denominador para o percentual.

    Returns:
        Percentual de óbitos por causas externas (0–100). Retorna ``NaN``
        quando não é possível identificar as causas externas.
    """
    # Caso 1: dados agregados com top3_causas e top3_causas_n
    if "top3_causas" in sim_df.columns and "top3_causas_n" in sim_df.columns:
        causas_externas: list = []
        for idx, row in sim_df.iterrows():
            causas = row["top3_causas"]
            contagens = row["top3_causas_n"]
            if causas is None or contagens is None:
                causas_externas.append(np.nan)
                continue
            # Converte para lista caso seja ndarray ou similar
            causas = list(causas)
            contagens = list(contagens)
            count = sum(
                int(contagens[i])
                for i, c in enumerate(causas)
                if isinstance(c, str) and c.startswith("V")
            )
            causas_externas.append(count)
        resultado = pd.Series(causas_externas, index=sim_df.index)
        return np.where(pd.Series(total_obitos) > 0, resultado / pd.Series(total_obitos) * 100, np.nan)

    # Caso 2: microdados com CAUSABAS
    causabas_col = "CAUSABAS" if "CAUSABAS" in sim_df.columns else "causabas" if "causabas" in sim_df.columns else None
    if causabas_col is None:
        logger.warning("Nenhuma coluna de causa básica encontrada em sim_df.")
        return np.nan

    causas_ext = sim_df[causabas_col].astype(str).str.upper().str.match(r"^[V-WXY]")
    count = causas_ext.sum()
    if isinstance(total_obitos, (int, float)):
        return count / total_obitos * 100 if total_obitos > 0 else np.nan
    return np.where(total_obitos > 0, count / total_obitos * 100, np.nan)
