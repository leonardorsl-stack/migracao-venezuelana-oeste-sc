"""
Modulo de analise do mercado de trabalho.

Projeto: migracao-venezuelana-oeste-sc
Autores: Leonardo Rafael Santos Leitao e Vicente Neves da Silva Ribeiro (UFFS)
"""

import pandas as pd


def analise_rotatividade(caged_df: pd.DataFrame,
                         tipo_col: str = "tipo",
                         ano_col: str = "ano") -> pd.DataFrame:
    """
    Calcula taxa de rotatividade (turnover) a partir dos dados CAGED.

    Parameters
    ----------
    caged_df : pd.DataFrame
        DataFrame com movimentacoes do CAGED.
    tipo_col : str, default "tipo"
        Coluna com tipo de movimentacao (Admissao/Desligamento).
    ano_col : str, default "ano"
        Coluna com ano da movimentacao.

    Returns
    -------
    pd.DataFrame
        DataFrame com admissoes, desligamentos, saldo e turnover por ano.
    """
    agg = caged_df.groupby([ano_col, tipo_col]).size().unstack(fill_value=0).reset_index()
    if "Admissao" not in agg.columns or "Desligamento" not in agg.columns:
        raise ValueError("Colunas 'Admissao' e/ou 'Desligamento' nao encontradas.")
    agg["saldo"] = agg["Admissao"] - agg["Desligamento"]
    agg["turnover"] = ((agg["Admissao"] + agg["Desligamento"]) / 2) / (agg["saldo"] + 1) * 100
    return agg


def analise_salarial(rais_df: pd.DataFrame, group_col: str = "setor",
                     salario_col: str = "salario_dezembro") -> pd.DataFrame:
    """
    Analise descritiva salarial por grupo.

    Parameters
    ----------
    rais_df : pd.DataFrame
        DataFrame com dados da RAIS.
    group_col : str, default "setor"
        Coluna de agrupamento.
    salario_col : str, default "salario_dezembro"
        Coluna de salario.

    Returns
    -------
    pd.DataFrame
        Estatisticas descritivas (media, mediana, desvio padrao) por grupo.
    """
    stats = rais_df.groupby(group_col)[salario_col].agg(["mean", "median", "std", "count"]).reset_index()
    stats.columns = [group_col, "media", "mediana", "desvio_padrao", "n"]
    return stats


def survival_analysis(rais_df: pd.DataFrame,
                      tempo_col: str = "tempo_emprego_meses") -> None:
    """
    Placeholder para analise de sobrevivencia no emprego.

    Parameters
    ----------
    rais_df : pd.DataFrame
        DataFrame com dados da RAIS.
    tempo_col : str, default "tempo_emprego_meses"
        Coluna com tempo de emprego em meses.

    Notes
    -----
    Requer instalacao da biblioteca `lifelines`.
    """
    try:
        from lifelines import KaplanMeierFitter
        kmf = KaplanMeierFitter()
        kmf.fit(rais_df[tempo_col])
        kmf.plot_survival_function()
    except ImportError:
        print("[AVISO] lifelines nao instalado. Instale com: pip install lifelines")
