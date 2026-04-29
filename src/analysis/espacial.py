"""
Modulo de analise espacial.

Projeto: migracao-venezuelana-oeste-sc
Autores: Leonardo Rafael Santos Leitao e Vicente Neves da Silva Ribeiro (UFFS)
"""

import pandas as pd


def calc_morani(df: pd.DataFrame, var: str, w) -> dict:
    """
    Calcula o Indice de Moran I para autocorrelacao espacial.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame com dados e geometria (GeoDataFrame).
    var : str
        Nome da variavel a ser analisada.
    w : pysal.lib.weights.W
        Matriz de pesos espaciais.

    Returns
    -------
    dict
        Dicionario com I, z_score, p_value.
    """
    try:
        from pysal.explore import esda
        moran = esda.Moran(df[var], w)
        return {"moran_i": moran.I, "z_score": moran.z_sim, "p_value": moran.p_sim}
    except ImportError:
        print("[AVISO] pysal nao instalado. Instale com: pip install pysal")
        return {}


def calc_lisa(df: pd.DataFrame, var: str, w) -> pd.DataFrame:
    """
    Calcula LISA (Local Indicators of Spatial Association).

    Parameters
    ----------
    df : pd.DataFrame
        GeoDataFrame com dados.
    var : str
        Variavel de interesse.
    w : pysal.lib.weights.W
        Matriz de pesos espaciais.

    Returns
    -------
    pd.DataFrame
        DataFrame original com colunas de cluster LISA e significancia.
    """
    try:
        from pysal.explore import esda
        lisa = esda.Moran_Local(df[var], w)
        df = df.copy()
        df["lisa_cluster"] = lisa.q
        df["lisa_pvalue"] = lisa.p_sim
        return df
    except ImportError:
        print("[AVISO] pysal nao instalado.")
        return df


def plot_mapa(df, var: str, ax=None):
    """
    Placeholder para plotagem de mapa.

    Parameters
    ----------
    df : GeoDataFrame
        Dados espaciais.
    var : str
        Variavel a ser mapeada.
    ax : matplotlib.axes.Axes, optional
        Eixo para plotagem.
    """
    try:
        import matplotlib.pyplot as plt
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 10))
        df.plot(column=var, cmap="YlOrRd", legend=True, ax=ax, edgecolor="black")
        ax.set_title(f"Mapa: {var}")
    except Exception as e:
        print(f"[ERRO] Falha ao plotar mapa: {e}")
