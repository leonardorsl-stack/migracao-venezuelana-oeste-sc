"""
Gera animações temporais da evolução dos vínculos RAIS de venezuelanos
no Oeste de SC (2018-2024).

Saídas:
- 10_animacao_evolucao_2018_2024.gif (mapa coroplético)
- 11_bar_chart_race_2018_2024.gif (bar chart race top 15)
"""

import os
import tempfile
import warnings

import geopandas as gpd
import imageio.v3 as iio
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# ------------------------------------------------------------------
# Configurações
# ------------------------------------------------------------------
PAINEL_PATH = "data/processed/painel_oeste_sc_2018_2024.parquet"
SHAPEFILE_PATH = "data/raw/ibge/shapefile/BR_Municipios_2022.shp"
OUTPUT_DIR = "outputs/figures"

MAP_GIF = os.path.join(OUTPUT_DIR, "10_animacao_evolucao_2018_2024.gif")
BAR_GIF = os.path.join(OUTPUT_DIR, "11_bar_chart_race_2018_2024.gif")

# Limites do Oeste SC (EPSG:4674 — SIRGAS 2000)
# Aproximados para dar um zoom razoável na região
BOUNDS = {
    "xmin": -54.0,
    "xmax": -48.5,
    "ymin": -27.5,
    "ymax": -25.8,
}

CMAP = "YlOrRd"
VMAX = 280  # escala fixa conforme solicitado
ANOS = list(range(2018, 2025))
DPI = 150

# ------------------------------------------------------------------
# 1. Carregar dados
# ------------------------------------------------------------------
print("Carregando painel...")
df = pd.read_parquet(PAINEL_PATH)

print("Carregando shapefile...")
gdf_br = gpd.read_file(SHAPEFILE_PATH)

# Filtrar SC e depois os municípios do painel
cods_painel = set(df["codigo_ibge_7d"].unique())
gdf_sc = gdf_br[gdf_br["SIGLA_UF"] == "SC"].copy()
gdf_sc["CD_MUN"] = gdf_sc["CD_MUN"].astype(int)
gdf_oeste = gdf_sc[gdf_sc["CD_MUN"].isin(cods_painel)].copy()

print(f"Municípios no shape após filtro: {len(gdf_oeste)}")
assert len(gdf_oeste) == 109, f"Esperado 109 municípios, encontrado {len(gdf_oeste)}"

# ------------------------------------------------------------------
# 2. Mapa coroplético — frames
# ------------------------------------------------------------------
print("\nGerando frames do mapa...")
map_frames_dir = tempfile.mkdtemp(prefix="map_frames_")
map_frame_paths = []

for ano in ANOS:
    df_ano = df[df["ano"] == ano][["codigo_ibge_7d", "taxa_vinculos_por_mil", "total_vinculos_rais"]].copy()
    merged = gdf_oeste.merge(df_ano, left_on="CD_MUN", right_on="codigo_ibge_7d", how="left")
    merged["taxa_vinculos_por_mil"] = merged["taxa_vinculos_por_mil"].fillna(0)

    fig, ax = plt.subplots(1, 1, figsize=(10, 8), dpi=DPI)
    merged.plot(
        column="taxa_vinculos_por_mil",
        cmap=CMAP,
        linewidth=0.3,
        edgecolor="0.6",
        ax=ax,
        vmin=0,
        vmax=VMAX,
        legend=False,
    )

    ax.set_xlim(BOUNDS["xmin"], BOUNDS["xmax"])
    ax.set_ylim(BOUNDS["ymin"], BOUNDS["ymax"])
    ax.set_aspect("equal")
    ax.axis("off")

    # Título
    ax.set_title(
        f"Taxa de Vínculos Venezuelanos — Oeste SC ({ano})",
        fontsize=14,
        fontweight="bold",
        pad=10,
    )

    # Barra de cores manual (mais controlável)
    sm = plt.cm.ScalarMappable(cmap=CMAP, norm=plt.Normalize(vmin=0, vmax=VMAX))
    sm._A = []
    cbar = fig.colorbar(sm, ax=ax, shrink=0.5, pad=0.02)
    cbar.set_label("Vínculos por mil habitantes", fontsize=10)

    # Anotação de rodapé
    ax.annotate(
        "Fonte: RAIS/MTE · Elaboração: projeto migracao-venezuelana-oeste-sc",
        xy=(0.5, 0.01),
        xycoords="figure fraction",
        ha="center",
        fontsize=7,
        color="gray",
    )

    frame_path = os.path.join(map_frames_dir, f"map_{ano}.png")
    plt.savefig(frame_path, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    map_frame_paths.append(frame_path)
    print(f"  Frame {ano} salvo.")

# Montar GIF do mapa
print(f"\nMontando GIF do mapa em {MAP_GIF}...")
images = [iio.imread(p) for p in map_frame_paths]
iio.imwrite(MAP_GIF, images, duration=1000, loop=0)
print(f"  GIF salvo: {MAP_GIF} ({os.path.getsize(MAP_GIF)/1024:.1f} KB)")

# ------------------------------------------------------------------
# 3. Bar chart race — frames
# ------------------------------------------------------------------
print("\nGerando frames do bar chart race...")
bar_frames_dir = tempfile.mkdtemp(prefix="bar_frames_")
bar_frame_paths = []

# Top 15 municípios por total acumulado de vínculos ao longo de todo o período
# para manter a paleta/cores consistentes entre frames
rank_global = (
    df.groupby("municipio")["total_vinculos_rais"]
    .sum()
    .sort_values(ascending=False)
    .head(15)
    .index.tolist()
)
cores = plt.cm.tab20(np.linspace(0, 1, len(rank_global)))
cor_por_mun = dict(zip(rank_global, cores, strict=False))

for ano in ANOS:
    df_ano = df[df["ano"] == ano][["municipio", "total_vinculos_rais"]].copy()

    # Garantir que todos os top 15 globais apareçam (mesmo com valor 0)
    presentes = set(df_ano["municipio"])
    faltantes = [m for m in rank_global if m not in presentes]
    if faltantes:
        df_falt = pd.DataFrame({"municipio": faltantes, "total_vinculos_rais": 0})
        df_ano = pd.concat([df_ano, df_falt], ignore_index=True)

    # Filtrar só os do rank_global e pegar os 15 maiores do ano
    df_ano = df_ano[df_ano["municipio"].isin(rank_global)]
    df_ano = df_ano.sort_values("total_vinculos_rais", ascending=True).tail(15)
    df_ano["cor"] = df_ano["municipio"].map(cor_por_mun)
    # Garantir que não haja NaN nas cores
    df_ano["cor"] = df_ano["cor"].fillna("#999999")

    fig, ax = plt.subplots(figsize=(10, 7), dpi=DPI)
    barras = ax.barh(df_ano["municipio"], df_ano["total_vinculos_rais"], color=df_ano["cor"], edgecolor="white")

    # Valores nas barras
    for barra, val in zip(barras, df_ano["total_vinculos_rais"], strict=False):
        if val > 0:
            ax.text(val + 1, barra.get_y() + barra.get_height() / 2, f"{int(val)}",
                    va="center", ha="left", fontsize=9, fontweight="bold")

    ax.set_xlim(0, df["total_vinculos_rais"].max() * 1.25)
    ax.set_title(f"Top 15 Municípios — Vínculos Venezuelanos RAIS ({ano})", fontsize=14, fontweight="bold")
    ax.set_xlabel("Número de vínculos", fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Anotação
    ax.annotate(
        "Fonte: RAIS/MTE · Elaboração: projeto migracao-venezuelana-oeste-sc",
        xy=(0.5, -0.08),
        xycoords="axes fraction",
        ha="center",
        fontsize=7,
        color="gray",
    )

    frame_path = os.path.join(bar_frames_dir, f"bar_{ano}.png")
    plt.savefig(frame_path, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    bar_frame_paths.append(frame_path)
    print(f"  Frame {ano} salvo.")

# Montar GIF do bar chart
print(f"\nMontando GIF do bar chart race em {BAR_GIF}...")
images = [iio.imread(p) for p in bar_frame_paths]
iio.imwrite(BAR_GIF, images, duration=1000, loop=0)
print(f"  GIF salvo: {BAR_GIF} ({os.path.getsize(BAR_GIF)/1024:.1f} KB)")

print("\n✅ Concluído!")
