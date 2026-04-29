#!/usr/bin/env python3
"""
Gera mapas coropléticos da Região Oeste de SC com dados de vínculos RAIS
de venezuelanos (2024).
"""

import geopandas as gpd
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import pandas as pd

# ---------------------------------------------------------------------------
# 1. Ler shapefile e filtrar SC
# ---------------------------------------------------------------------------
shapefile_path = "/Users/leonardosantos/Documents/raio_x_migraçao/data/raw/ibge/shapefile/BR_Municipios_2022.shp"
gdf = gpd.read_file(shapefile_path)
print(f"Shapefile total: {len(gdf)} municípios")

gdf_sc = gdf[gdf["SIGLA_UF"] == "SC"].copy()
print(f"Municípios de SC: {len(gdf_sc)}")

# ---------------------------------------------------------------------------
# 2. Ler painel e filtrar 2024
# ---------------------------------------------------------------------------
painel_path = "/Users/leonardosantos/Documents/raio_x_migraçao/data/processed/painel_oeste_sc_2018_2024.parquet"
df = pd.read_parquet(painel_path)
df_2024 = df[df["ano"] == 2024].copy()
print(f"Municípios no painel 2024: {len(df_2024)}")

# ---------------------------------------------------------------------------
# 3. Merge shapefile + painel
# ---------------------------------------------------------------------------
gdf_sc["CD_MUN"] = gdf_sc["CD_MUN"].astype(str).str.strip()
df_2024["codigo_ibge_7d"] = df_2024["codigo_ibge_7d"].astype(str).str.strip()

gdf_mapa = gdf_sc.merge(
    df_2024,
    left_on="CD_MUN",
    right_on="codigo_ibge_7d",
    how="inner"
)
print(f"Municípios após merge: {len(gdf_mapa)}")

# Verificar se todos os 109 municípios foram encontrados
if len(gdf_mapa) != 109:
    print(f"AVISO: Esperado 109 municípios, mas merge retornou {len(gdf_mapa)}")
    faltantes = set(df_2024["codigo_ibge_7d"]) - set(gdf_sc["CD_MUN"])
    if faltantes:
        print(f"Códigos faltantes no shapefile: {faltantes}")
else:
    print("OK: Todos os 109 municípios foram encontrados no shapefile.")

# ---------------------------------------------------------------------------
# Identificar Chapecó para destaque
# ---------------------------------------------------------------------------
chapeco_idx = gdf_mapa[gdf_mapa["NM_MUN"] == "Chapecó"].index
if len(chapeco_idx) == 0:
    # tentar pelo nome do painel
    chapeco_idx = gdf_mapa[gdf_mapa["municipio"] == "Chapecó"].index
print(f"Chapecó encontrado: {len(chapeco_idx)} registro(s)")

# ---------------------------------------------------------------------------
# 4. Mapa 1 – Taxa de vínculos por mil habitantes
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(1, 1, figsize=(14, 12))

# Plotar mapa coroplético
gdf_mapa.plot(
    column="taxa_vinculos_por_mil",
    cmap="YlOrRd",
    linewidth=0.5,
    ax=ax,
    edgecolor="gray",
    legend=False,
    missing_kwds={"color": "lightgray", "label": "Sem dados"}
)

# Destacar Chapecó com contorno preto
if len(chapeco_idx) > 0:
    gdf_mapa.loc[chapeco_idx].boundary.plot(ax=ax, color="black", linewidth=2.5)
    # Adicionar label de Chapecó
    chapeco_geom = gdf_mapa.loc[chapeco_idx].geometry.iloc[0]
    centroid = chapeco_geom.centroid
    ax.annotate(
        "Chapecó",
        xy=(centroid.x, centroid.y),
        xytext=(centroid.x + 0.3, centroid.y + 0.3),
        fontsize=11,
        fontweight="bold",
        color="black",
        arrowprops=dict(arrowstyle="->", color="black", lw=1.2),
        path_effects=[pe.withStroke(linewidth=2.5, foreground="white")]
    )

# Colorbar manual para controle total
sm = plt.cm.ScalarMappable(
    cmap="YlOrRd",
    norm=plt.Normalize(
        vmin=gdf_mapa["taxa_vinculos_por_mil"].min(),
        vmax=gdf_mapa["taxa_vinculos_por_mil"].max()
    )
)
sm._A = []
cbar = fig.colorbar(sm, ax=ax, shrink=0.6, aspect=30, pad=0.02)
cbar.set_label("Vínculos RAIS por mil hab.", fontsize=12, fontweight="bold")

# Títulos e fonte
ax.set_title(
    "Inserção Laboral de Venezuelanos no Oeste de SC (2024)",
    fontsize=16,
    fontweight="bold",
    pad=15
)
ax.annotate(
    "Fonte: RAIS 2024 / IBGE",
    xy=(0.01, 0.01),
    xycoords="axes fraction",
    fontsize=10,
    style="italic",
    color="#333333"
)

# Remover eixos
ax.set_axis_off()

# Salvar
output1 = "/Users/leonardosantos/Documents/raio_x_migraçao/outputs/figures/08_mapa_coropletico_oeste_sc_2024.png"
plt.savefig(output1, dpi=300, bbox_inches="tight", pad_inches=0.2)
plt.close(fig)
print(f"Mapa 1 salvo: {output1}")

# ---------------------------------------------------------------------------
# 5. Mapa 2 – Volume absoluto de vínculos
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(1, 1, figsize=(14, 12))

gdf_mapa.plot(
    column="total_vinculos_rais",
    cmap="Blues",
    linewidth=0.5,
    ax=ax,
    edgecolor="gray",
    legend=False,
    missing_kwds={"color": "lightgray", "label": "Sem dados"}
)

# Destacar Chapecó
if len(chapeco_idx) > 0:
    gdf_mapa.loc[chapeco_idx].boundary.plot(ax=ax, color="black", linewidth=2.5)
    chapeco_geom = gdf_mapa.loc[chapeco_idx].geometry.iloc[0]
    centroid = chapeco_geom.centroid
    ax.annotate(
        "Chapecó",
        xy=(centroid.x, centroid.y),
        xytext=(centroid.x + 0.3, centroid.y + 0.3),
        fontsize=11,
        fontweight="bold",
        color="black",
        arrowprops=dict(arrowstyle="->", color="black", lw=1.2),
        path_effects=[pe.withStroke(linewidth=2.5, foreground="white")]
    )

# Colorbar
sm2 = plt.cm.ScalarMappable(
    cmap="Blues",
    norm=plt.Normalize(
        vmin=gdf_mapa["total_vinculos_rais"].min(),
        vmax=gdf_mapa["total_vinculos_rais"].max()
    )
)
sm2._A = []
cbar2 = fig.colorbar(sm2, ax=ax, shrink=0.6, aspect=30, pad=0.02)
cbar2.set_label("Total de vínculos RAIS", fontsize=12, fontweight="bold")

# Títulos e fonte
ax.set_title(
    "Volume de Vínculos RAIS de Venezuelanos no Oeste de SC (2024)",
    fontsize=16,
    fontweight="bold",
    pad=15
)
ax.annotate(
    "Fonte: RAIS 2024 / IBGE",
    xy=(0.01, 0.01),
    xycoords="axes fraction",
    fontsize=10,
    style="italic",
    color="#333333"
)

ax.set_axis_off()

output2 = "/Users/leonardosantos/Documents/raio_x_migraçao/outputs/figures/09_mapa_coropletico_volume_2024.png"
plt.savefig(output2, dpi=300, bbox_inches="tight", pad_inches=0.2)
plt.close(fig)
print(f"Mapa 2 salvo: {output2}")

print("\n--- Resumo ---")
print(f"Municípios plotados: {len(gdf_mapa)}")
print(f"Taxa mínima: {gdf_mapa['taxa_vinculos_por_mil'].min():.4f}")
print(f"Taxa máxima: {gdf_mapa['taxa_vinculos_por_mil'].max():.4f}")
print(f"Vínculos mínimo: {gdf_mapa['total_vinculos_rais'].min()}")
print(f"Vínculos máximo: {gdf_mapa['total_vinculos_rais'].max()}")
