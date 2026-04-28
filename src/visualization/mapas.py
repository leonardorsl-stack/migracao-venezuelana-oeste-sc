"""
Modulo de visualizacao espacial.

Projeto: migracao-venezuelana-oeste-sc
Autores: Leonardo Rafael Santos Leitao e Vicente Neves da Silva Ribeiro (UFFS)
"""

from typing import Optional
import matplotlib.pyplot as plt


def plot_mapa_coropletico(gdf, coluna: str, titulo: str,
                          cmap: str = "YlOrRd", ax=None, **kwargs):
    """
    Plota mapa coropletico.

    Parameters
    ----------
    gdf : GeoDataFrame
        Dados espaciais com geometria.
    coluna : str
        Coluna numerica a ser colorida.
    titulo : str
        Titulo do mapa.
    cmap : str, default "YlOrRd"
        Mapa de cores do matplotlib.
    ax : matplotlib.axes.Axes, optional
        Eixo existente.
    **kwargs
        Argumentos adicionais para GeoDataFrame.plot().

    Returns
    -------
    matplotlib.axes.Axes
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 10))
    gdf.plot(column=coluna, cmap=cmap, legend=True, ax=ax,
             edgecolor="black", linewidth=0.5, legend_kwds={"shrink": 0.6}, **kwargs)
    ax.set_title(titulo, fontsize=14, fontweight="bold")
    ax.axis("off")
    return ax


def plot_mapa_bolhas(gdf, coluna: str, titulo: str,
                     cmap: str = "YlOrRd", ax=None, **kwargs):
    """
    Plota mapa de bolhas (tamanho proporcional ao valor).

    Parameters
    ----------
    gdf : GeoDataFrame
        Dados espaciais.
    coluna : str
        Coluna numerica para tamanho das bolhas.
    titulo : str
        Titulo do mapa.
    cmap : str, default "YlOrRd"
        Mapa de cores.
    ax : matplotlib.axes.Axes, optional
        Eixo existente.
    **kwargs
        Argumentos adicionais.

    Returns
    -------
    matplotlib.axes.Axes
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 10))
    # Centroide para posicionamento das bolhas
    gdf["centroid"] = gdf.geometry.centroid
    gdf_points = gdf.copy()
    gdf_points.set_geometry("centroid", inplace=True)
    gdf.boundary.plot(ax=ax, color="black", linewidth=0.5)
    gdf_points.plot(column=coluna, cmap=cmap, markersize=gdf[coluna] * 10,
                    alpha=0.7, ax=ax, edgecolor="black", **kwargs)
    ax.set_title(titulo, fontsize=14, fontweight="bold")
    ax.axis("off")
    return ax
