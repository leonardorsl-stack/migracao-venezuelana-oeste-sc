"""
Modulo de analise demografica.

Projeto: migracao-venezuelana-oeste-sc
Autores: Leonardo Rafael Santos Leitao e Vicente Neves da Silva Ribeiro (UFFS)
"""

import numpy as np
import pandas as pd


def build_pyramid(df: pd.DataFrame, sexo_col: str, idade_col: str) -> pd.DataFrame:
    """
    Constroi tabela para piramide etaria.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame com dados individuais ou agregados.
    sexo_col : str
        Nome da coluna de sexo (1=Masculino, 2=Feminino).
    idade_col : str
        Nome da coluna de idade.

    Returns
    -------
    pd.DataFrame
        DataFrame com colunas: faixa_etaria, sexo, contagem, pct, pct_plot.
    """
    faixas = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 100]
    labels = ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34",
              "35-39", "40-44", "45-49", "50-54", "55-59", "60-64",
              "65-69", "70-74", "75-79", "80+"]
    df["faixa_etaria"] = pd.cut(df[idade_col], bins=faixas, labels=labels, right=False)
    agg = df.groupby(["faixa_etaria", sexo_col]).size().reset_index(name="contagem")
    total = agg["contagem"].sum()
    agg["pct"] = (agg["contagem"] / total) * 100
    agg["pct_plot"] = agg.apply(lambda r: -r["pct"] if r[sexo_col] == 1 else r["pct"], axis=1)
    return agg


def calc_taxa_dependencia(df: pd.DataFrame, idade_col: str = "idade") -> float:
    """
    Calcula a taxa de dependencia demografica.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame com coluna de idade.
    idade_col : str, default "idade"
        Nome da coluna de idade.

    Returns
    -------
    float
        Taxa de dependencia = ((0-14 + 60+) / (15-59)) * 100.
    """
    jovens = ((df[idade_col] >= 0) & (df[idade_col] <= 14)).sum()
    idosos = (df[idade_col] >= 60).sum()
    ativos = ((df[idade_col] >= 15) & (df[idade_col] <= 59)).sum()
    if ativos == 0:
        return np.nan
    return ((jovens + idosos) / ativos) * 100


def calc_razao_sexos(df: pd.DataFrame, sexo_col: str = "sexo",
                     masculino: int = 1, feminino: int = 2) -> float:
    """
    Calcula a razao de sexos (homens por 100 mulheres).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame com coluna de sexo.
    sexo_col : str, default "sexo"
        Nome da coluna de sexo.
    masculino : int, default 1
        Codigo para masculino.
    feminino : int, default 2
        Codigo para feminino.

    Returns
    -------
    float
        Razao de sexos.
    """
    homens = (df[sexo_col] == masculino).sum()
    mulheres = (df[sexo_col] == feminino).sum()
    if mulheres == 0:
        return np.nan
    return (homens / mulheres) * 100
