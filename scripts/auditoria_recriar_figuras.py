#!/usr/bin/env python3
"""
Script de correção de figuras identificadas na auditoria.

Recria as figuras com problemas graves encontrados na auditoria:
- Figuras 12, 13, 17: títulos imprecisos ("Venezuelanos" em vez de "Trabalhadores 
  Venezuelanos na RAIS") + ausência de nota metodológica e fonte
- Figuras 08, 09: ausência de destaque a Guatambú (município com maior taxa)
- Figura 01: ausência de fonte e nota metodológica sobre RAIS
"""

import os

import geopandas as gpd
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# ---------------------------------------------------------------------------
# Configurações globais
# ---------------------------------------------------------------------------
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['figure.figsize'] = (12, 8)
sns.set_style("whitegrid")
sns.set_palette("deep")

BASE_DIR = "/Users/leonardosantos/Documents/raio_x_migraçao"
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------------------
def add_fonte_nota_rais(ax, fig=None, incluir_nota=True):
    """Adiciona fonte e nota metodológica sobre RAIS."""
    texto_fonte = "Fonte: RAIS/MTE (2023–2024) · Elaboração: projeto migração-venezuelana-oeste-sc"
    ax.annotate(texto_fonte, xy=(0.01, -0.06), xycoords='axes fraction',
                fontsize=8, style='italic', color='#333333')
    if incluir_nota:
        texto_nota = (
            "Nota: dados da RAIS referem-se a vínculos empregatícios formais. "
            "Excluem crianças, adolescentes (<14 anos), idosos fora do mercado formal, "
            "trabalhadores informais e desempregados."
        )
        ax.annotate(texto_nota, xy=(0.01, -0.12), xycoords='axes fraction',
                    fontsize=7, color='#555555', wrap=True)


def add_fonte(ax, texto="Fonte: RAIS/MTE · Elaboração: projeto migração-venezuelana-oeste-sc"):
    ax.annotate(texto, xy=(0.01, -0.06), xycoords='axes fraction',
                fontsize=8, style='italic', color='#333333')


# =============================================================================
# FIGURA 01 — Evolução dos vínculos RAIS regional (2018-2024)  [CORRIGIDA]
# =============================================================================
painel = pd.read_parquet(os.path.join(BASE_DIR, "data", "processed", "painel_oeste_sc_2018_2024.parquet"))
painel['ano'] = painel['ano'].astype(int)

reg = (
    painel.groupby('ano')
    .agg(populacao_total=('populacao_total', 'sum'),
         total_vinculos_rais=('total_vinculos_rais', 'sum'))
    .reset_index()
)
reg['taxa_vinculos_por_mil'] = reg['total_vinculos_rais'] / reg['populacao_total'] * 1000

fig, ax1 = plt.subplots(figsize=(12, 7))
color_line = '#1f77b4'
ax1.set_xlabel('Ano', fontsize=13)
ax1.set_ylabel('Taxa de vínculos por mil habitantes', color=color_line, fontsize=13)
ax1.plot(reg['ano'], reg['taxa_vinculos_por_mil'], color=color_line, marker='o', linewidth=2.5, markersize=8)
ax1.tick_params(axis='y', labelcolor=color_line)
ax1.set_xticks(reg['ano'])
ax1.set_ylim(0, reg['taxa_vinculos_por_mil'].max() * 1.15)

for x, y in zip(reg['ano'], reg['taxa_vinculos_por_mil'], strict=False):
    ax1.annotate(f'{y:.1f}', xy=(x, y), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=9, color=color_line)

ax2 = ax1.twinx()
color_bar = '#d62728'
ax2.set_ylabel('Número absoluto de vínculos', color=color_bar, fontsize=13)
bars = ax2.bar(reg['ano'], reg['total_vinculos_rais'], color=color_bar, alpha=0.3, width=0.5)
ax2.tick_params(axis='y', labelcolor=color_bar)
ax2.set_ylim(0, reg['total_vinculos_rais'].max() * 1.3)

for bar in bars:
    height = bar.get_height()
    ax2.annotate(f'{int(height):,}'.replace(',', '.'), xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, color=color_bar)

fig.suptitle('Evolução da Inserção Laboral Formal de Venezuelanos no Oeste de SC (RAIS)',
             fontsize=15, fontweight='bold')
fig.tight_layout()

# Adicionar fonte + nota na parte inferior
fig.text(0.12, 0.01,
         "Fonte: RAIS/MTE (2018–2024) · Elaboração: projeto migração-venezuelana-oeste-sc",
         fontsize=8, style='italic', color='#333333')
fig.text(0.12, -0.02,
         "Nota: a RAIS cobre apenas vínculos empregatícios formais (CEI + CNPJ). Não inclui trabalhadores informais, desempregados, crianças ou idosos fora do mercado de trabalho formal.",
         fontsize=7, color='#555555')

plt.savefig(os.path.join(OUTPUT_DIR, '01_evolucao_vinculos_regional.png'), bbox_inches='tight')
plt.close()
print("✅ Figura 01 recriada com fonte e nota metodológica.")


# =============================================================================
# FIGURA 08 — Mapa coroplético taxa per mil (2024)  [CORRIGIDA]
# =============================================================================
shapefile_path = os.path.join(BASE_DIR, "data/raw/ibge/shapefile/BR_Municipios_2022.shp")
gdf = gpd.read_file(shapefile_path)
gdf_sc = gdf[gdf["SIGLA_UF"] == "SC"].copy()

df = pd.read_parquet(os.path.join(BASE_DIR, "data/processed/painel_oeste_sc_2018_2024.parquet"))
df_2024 = df[df["ano"] == 2024].copy()

gdf_sc["CD_MUN"] = gdf_sc["CD_MUN"].astype(str).str.strip()
df_2024["codigo_ibge_7d"] = df_2024["codigo_ibge_7d"].astype(str).str.strip()

gdf_mapa = gdf_sc.merge(df_2024, left_on="CD_MUN", right_on="codigo_ibge_7d", how="inner")
assert len(gdf_mapa) == 109, f"Esperado 109 municípios, merge retornou {len(gdf_mapa)}"

# Identificar destaques
chapeco_idx = gdf_mapa[gdf_mapa["NM_MUN"] == "Chapecó"].index
guatambu_idx = gdf_mapa[gdf_mapa["NM_MUN"] == "Guatambú"].index

fig, ax = plt.subplots(1, 1, figsize=(14, 12))

gdf_mapa.plot(
    column="taxa_vinculos_por_mil",
    cmap="YlOrRd",
    linewidth=0.5,
    ax=ax,
    edgecolor="gray",
    legend=False,
    missing_kwds={"color": "lightgray", "label": "Sem dados"}
)

# Destacar Chapecó (maior volume)
if len(chapeco_idx) > 0:
    gdf_mapa.loc[chapeco_idx].boundary.plot(ax=ax, color="black", linewidth=2.5)
    chapeco_geom = gdf_mapa.loc[chapeco_idx].geometry.iloc[0]
    centroid = chapeco_geom.centroid
    ax.annotate(
        "Chapecó (maior volume)",
        xy=(centroid.x, centroid.y),
        xytext=(centroid.x + 0.3, centroid.y + 0.3),
        fontsize=11, fontweight="bold", color="black",
        arrowprops=dict(arrowstyle="->", color="black", lw=1.2),
        path_effects=[pe.withStroke(linewidth=2.5, foreground="white")]
    )

# Destacar Guatambú (maior taxa)
if len(guatambu_idx) > 0:
    gdf_mapa.loc[guatambu_idx].boundary.plot(ax=ax, color="darkblue", linewidth=2.5)
    guatambu_geom = gdf_mapa.loc[guatambu_idx].geometry.iloc[0]
    centroid_g = guatambu_geom.centroid
    ax.annotate(
        "Guatambú (maior taxa)",
        xy=(centroid_g.x, centroid_g.y),
        xytext=(centroid_g.x - 0.8, centroid_g.y + 0.5),
        fontsize=11, fontweight="bold", color="darkblue",
        arrowprops=dict(arrowstyle="->", color="darkblue", lw=1.2),
        path_effects=[pe.withStroke(linewidth=2.5, foreground="white")]
    )

sm = plt.cm.ScalarMappable(cmap="YlOrRd",
    norm=plt.Normalize(vmin=gdf_mapa["taxa_vinculos_por_mil"].min(),
                       vmax=gdf_mapa["taxa_vinculos_por_mil"].max()))
sm._A = []
cbar = fig.colorbar(sm, ax=ax, shrink=0.6, aspect=30, pad=0.02)
cbar.set_label("Vínculos RAIS por mil hab.", fontsize=12, fontweight="bold")

ax.set_title(
    "Inserção Laboral Formal de Venezuelanos no Oeste de SC (2024)\nTaxa de vínculos RAIS por mil habitantes",
    fontsize=16, fontweight="bold", pad=15
)
ax.annotate(
    "Fonte: RAIS 2024 / IBGE",
    xy=(0.01, 0.01), xycoords="axes fraction",
    fontsize=10, style="italic", color="#333333"
)
ax.set_axis_off()

output1 = os.path.join(OUTPUT_DIR, "08_mapa_coropletico_oeste_sc_2024.png")
plt.savefig(output1, dpi=300, bbox_inches="tight", pad_inches=0.2)
plt.close(fig)
print("✅ Figura 08 recriada com destaque a Guatambú (maior taxa) e Chapecó (maior volume).")


# =============================================================================
# FIGURA 09 — Mapa coroplético volume absoluto (2024)  [CORRIGIDA]
# =============================================================================
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

if len(chapeco_idx) > 0:
    gdf_mapa.loc[chapeco_idx].boundary.plot(ax=ax, color="black", linewidth=2.5)
    chapeco_geom = gdf_mapa.loc[chapeco_idx].geometry.iloc[0]
    centroid = chapeco_geom.centroid
    ax.annotate(
        "Chapecó (maior volume)",
        xy=(centroid.x, centroid.y),
        xytext=(centroid.x + 0.3, centroid.y + 0.3),
        fontsize=11, fontweight="bold", color="black",
        arrowprops=dict(arrowstyle="->", color="black", lw=1.2),
        path_effects=[pe.withStroke(linewidth=2.5, foreground="white")]
    )

# Destacar Guatambú também no mapa de volume (segundo maior volume)
if len(guatambu_idx) > 0:
    gdf_mapa.loc[guatambu_idx].boundary.plot(ax=ax, color="darkblue", linewidth=2.5)
    guatambu_geom = gdf_mapa.loc[guatambu_idx].geometry.iloc[0]
    centroid_g = guatambu_geom.centroid
    ax.annotate(
        "Guatambú (2º maior volume, 1ª taxa)",
        xy=(centroid_g.x, centroid_g.y),
        xytext=(centroid_g.x - 0.8, centroid_g.y + 0.5),
        fontsize=11, fontweight="bold", color="darkblue",
        arrowprops=dict(arrowstyle="->", color="darkblue", lw=1.2),
        path_effects=[pe.withStroke(linewidth=2.5, foreground="white")]
    )

sm2 = plt.cm.ScalarMappable(cmap="Blues",
    norm=plt.Normalize(vmin=gdf_mapa["total_vinculos_rais"].min(),
                       vmax=gdf_mapa["total_vinculos_rais"].max()))
sm2._A = []
cbar2 = fig.colorbar(sm2, ax=ax, shrink=0.6, aspect=30, pad=0.02)
cbar2.set_label("Total de vínculos RAIS", fontsize=12, fontweight="bold")

ax.set_title(
    "Volume de Vínculos RAIS de Venezuelanos no Oeste de SC (2024)",
    fontsize=16, fontweight="bold", pad=15
)
ax.annotate(
    "Fonte: RAIS 2024 / IBGE",
    xy=(0.01, 0.01), xycoords="axes fraction",
    fontsize=10, style="italic", color="#333333"
)
ax.set_axis_off()

output2 = os.path.join(OUTPUT_DIR, "09_mapa_coropletico_volume_2024.png")
plt.savefig(output2, dpi=300, bbox_inches="tight", pad_inches=0.2)
plt.close(fig)
print("✅ Figura 09 recriada com destaque a Guatambú e Chapecó.")


# =============================================================================
# FIGURAS 12, 13, 17 — Perfil Etário  [CORRIGIDAS]
# =============================================================================
FAIXAS = ['15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60+']

COR_MASC_OESTE = '#1f77b4'
COR_FEM_OESTE = '#ff7f0e'
COR_MASC_VEN = '#2ca02c'
COR_FEM_VEN = '#d62728'

def faixa_etaria_rais(idade: int) -> str:
    if 15 <= idade <= 19: return '15-19'
    if 20 <= idade <= 24: return '20-24'
    if 25 <= idade <= 29: return '25-29'
    if 30 <= idade <= 34: return '30-34'
    if 35 <= idade <= 39: return '35-39'
    if 40 <= idade <= 44: return '40-44'
    if 45 <= idade <= 49: return '45-49'
    if 50 <= idade <= 54: return '50-54'
    if 55 <= idade <= 59: return '55-59'
    if idade >= 60: return '60+'
    return None

def faixa_etaria_ibge(idade_label: str) -> str:
    mapping = {
        '15 a 19 anos': '15-19', '20 a 24 anos': '20-24', '25 a 29 anos': '25-29',
        '30 a 34 anos': '30-34', '35 a 39 anos': '35-39', '40 a 44 anos': '40-44',
        '45 a 49 anos': '45-49', '50 a 54 anos': '50-54', '55 a 59 anos': '55-59',
        '60 a 64 anos': '60+', '65 a 69 anos': '60+', '70 a 74 anos': '60+',
        '75 a 79 anos': '60+', '80 a 84 anos': '60+', '85 a 89 anos': '60+',
        '90 a 94 anos': '60+', '95 a 99 anos': '60+', '100 anos ou mais': '60+',
    }
    return mapping.get(idade_label)

# Dados RAIS
df23 = pd.read_parquet(os.path.join(BASE_DIR, 'data/processed/rais_vinculos_sc_venezuela_2023.parquet'))
df24 = pd.read_parquet(os.path.join(BASE_DIR, 'data/processed/rais_vinculos_sc_venezuela_2024.parquet'))
df_rais = pd.concat([df23, df24], ignore_index=True)
df_rais['sexo'] = df_rais['sexo'].astype(str).str.strip()
df_rais['idade'] = pd.to_numeric(df_rais['idade'], errors='coerce')
df_rais['sexo_label'] = df_rais['sexo'].map({'1': 'Homens', '2': 'Mulheres'})
df_rais['faixa'] = df_rais['idade'].apply(faixa_etaria_rais)
df_rais = df_rais.dropna(subset=['faixa', 'sexo_label'])

rais_counts = df_rais.groupby(['faixa', 'sexo_label']).size().reset_index(name='count')
rais_total = rais_counts['count'].sum()
rais_counts['pct'] = rais_counts['count'] / rais_total * 100
rais_pivot = rais_counts.pivot(index='faixa', columns='sexo_label', values='pct').reindex(FAIXAS).fillna(0)

# Dados IBGE
df_ibge = pd.read_parquet(os.path.join(BASE_DIR, 'data/processed/ibge_populacao_idade_sexo_oeste_sc_2022.parquet'))
df_ibge = df_ibge[df_ibge['D4N'].isin(['Homens', 'Mulheres'])].copy()
df_ibge['pop'] = pd.to_numeric(df_ibge['V'], errors='coerce')
df_ibge['faixa'] = df_ibge['D5N'].apply(faixa_etaria_ibge)
df_ibge = df_ibge.dropna(subset=['faixa'])
ibge_counts = df_ibge.groupby(['faixa', 'D4N'])['pop'].sum().reset_index()
ibge_total = ibge_counts['pop'].sum()
ibge_counts['pct'] = ibge_counts['pop'] / ibge_total * 100
ibge_pivot = ibge_counts.pivot(index='faixa', columns='D4N', values='pct').reindex(FAIXAS).fillna(0)

# Índice de concentração
rais_total_by_faixa = rais_counts.groupby('faixa')['count'].sum().reindex(FAIXAS)
rais_total_pct = rais_total_by_faixa / rais_total_by_faixa.sum() * 100
ibge_total_by_faixa = ibge_counts.groupby('faixa')['pop'].sum().reindex(FAIXAS)
ibge_total_pct = ibge_total_by_faixa / ibge_total_by_faixa.sum() * 100
indice = (rais_total_pct / ibge_total_pct).reindex(FAIXAS)
indice = indice.replace([np.inf, -np.inf], np.nan).fillna(0)

# --- Figura 12: Pirâmide etária ---
fig, axes = plt.subplots(1, 2, figsize=(14, 8), sharey=True)
y_pos = np.arange(len(FAIXAS))
bar_height = 0.35

ax = axes[0]
ax.barh(y_pos + bar_height/2, -ibge_pivot['Homens'], height=bar_height,
        color=COR_MASC_OESTE, label='Homens', edgecolor='white', linewidth=0.3)
ax.barh(y_pos - bar_height/2, ibge_pivot['Mulheres'], height=bar_height,
        color=COR_FEM_OESTE, label='Mulheres', edgecolor='white', linewidth=0.3)
ax.set_yticks(y_pos)
ax.set_yticklabels(FAIXAS)
ax.set_xlabel('Percentual (%)')
ax.set_title('População Total\nOeste SC (Censo 2022)', fontweight='bold')
ax.set_xlim(-8, 8)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{abs(x):.1f}'))
ax.axvline(0, color='black', linewidth=0.8)
ax.legend(loc='lower right')
ax.grid(axis='x', alpha=0.3)

ax = axes[1]
ax.barh(y_pos + bar_height/2, -rais_pivot['Homens'], height=bar_height,
        color=COR_MASC_VEN, label='Homens', edgecolor='white', linewidth=0.3)
ax.barh(y_pos - bar_height/2, rais_pivot['Mulheres'], height=bar_height,
        color=COR_FEM_VEN, label='Mulheres', edgecolor='white', linewidth=0.3)
ax.set_yticks(y_pos)
ax.set_yticklabels(FAIXAS)
ax.set_xlabel('Percentual (%)')
ax.set_title('Trabalhadores Venezuelanos na RAIS\n(2023–2024)', fontweight='bold')
ax.set_xlim(-8, 8)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{abs(x):.1f}'))
ax.axvline(0, color='black', linewidth=0.8)
ax.legend(loc='lower right')
ax.grid(axis='x', alpha=0.3)

fig.suptitle('Pirâmide Etária Comparativa: População Total Oeste SC vs. Trabalhadores Venezuelanos na RAIS',
             fontsize=14, fontweight='bold', y=1.02)
fig.text(0.12, -0.02,
         "Fonte: IBGE Censo 2022 e RAIS/MTE (2023–2024) · Elaboração: projeto migração-venezuelana-oeste-sc",
         fontsize=8, style='italic', color='#333333')
fig.text(0.12, -0.06,
         "Nota metodológica: os dados da RAIS incluem apenas trabalhadores com vínculo empregatício formal. "
         "Excluem crianças, adolescentes (<14 anos), idosos fora do mercado formal, trabalhadores informais e desempregados.",
         fontsize=7, color='#555555')
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, '12_piramide_etaria_venezuelanos_vs_total.png'), bbox_inches='tight')
plt.close(fig)
print("✅ Figura 12 recriada com título corrigido, fonte e nota metodológica.")

# --- Figura 13: Comparativo percentual ---
fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
x = np.arange(len(FAIXAS))
width = 0.25

ax = axes[0]
ax.bar(x - width/2, ibge_pivot['Homens'], width, label='Oeste SC', color=COR_MASC_OESTE, edgecolor='white', linewidth=0.3)
ax.bar(x + width/2, rais_pivot['Homens'], width, label='Trab. Venezuelanos RAIS', color=COR_MASC_VEN, edgecolor='white', linewidth=0.3)
ax.set_ylabel('Percentual (%)')
ax.set_title('Homens', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(FAIXAS, rotation=45, ha='right')
ax.legend()
ax.grid(axis='y', alpha=0.3)

ax = axes[1]
ax.bar(x - width/2, ibge_pivot['Mulheres'], width, label='Oeste SC', color=COR_FEM_OESTE, edgecolor='white', linewidth=0.3)
ax.bar(x + width/2, rais_pivot['Mulheres'], width, label='Trab. Venezuelanos RAIS', color=COR_FEM_VEN, edgecolor='white', linewidth=0.3)
ax.set_ylabel('Percentual (%)')
ax.set_title('Mulheres', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(FAIXAS, rotation=45, ha='right')
ax.legend()
ax.grid(axis='y', alpha=0.3)

fig.suptitle('Distribuição Etária por Sexo: Oeste SC vs. Trabalhadores Venezuelanos na RAIS',
             fontsize=13, fontweight='bold', y=1.02)
fig.text(0.12, -0.02,
         "Fonte: IBGE Censo 2022 e RAIS/MTE (2023–2024) · Elaboração: projeto migração-venezuelana-oeste-sc",
         fontsize=8, style='italic', color='#333333')
fig.text(0.12, -0.06,
         "Nota: a RAIS cobre apenas vínculos formais. Não representa o perfil etário da população venezuelana total no Oeste de SC.",
         fontsize=7, color='#555555')
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, '13_comparativo_faixa_etaria_percentual.png'), bbox_inches='tight')
plt.close(fig)
print("✅ Figura 13 recriada com título corrigido, fonte e nota metodológica.")

# --- Figura 17: Índice de concentração ---
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(FAIXAS, indice, marker='o', color='#2c3e50', linewidth=2.5, markersize=8)
ax.axhline(1, color='red', linestyle='--', linewidth=1.5, label='Paridade (índice = 1)')
ax.fill_between(FAIXAS, 1, indice, where=(indice > 1), alpha=0.2, color='green', label='Super-representação')
ax.fill_between(FAIXAS, 1, indice, where=(indice < 1), alpha=0.2, color='red', label='Sub-representação')
ax.set_xlabel('Faixa etária')
ax.set_ylabel('Índice de concentração')
ax.set_title('Índice de Concentração Etária de Trabalhadores Venezuelanos na RAIS\n(% trabalhadores venezuelanos na faixa / % população total na faixa)',
             fontweight='bold')
ax.set_xticks(range(len(FAIXAS)))
ax.set_xticklabels(FAIXAS, rotation=45, ha='right')
ax.legend()
ax.grid(alpha=0.3)

for i, v in enumerate(indice):
    ax.annotate(f'{v:.1f}', (i, v), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)

ax.annotate(
    "Fonte: RAIS/MTE (2023–2024) e IBGE Censo 2022 · Elaboração: projeto migração-venezuelana-oeste-sc",
    xy=(0.01, -0.1), xycoords='axes fraction', fontsize=8, style='italic', color='#333333'
)
ax.annotate(
    "Nota: índice calculado sobre trabalhadores formais (RAIS). Não representa a população venezuelana total.",
    xy=(0.01, -0.16), xycoords='axes fraction', fontsize=7, color='#555555'
)

fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, '17_indice_concentracao_etaria.png'), bbox_inches='tight')
plt.close(fig)
print("✅ Figura 17 recriada com título corrigido, fonte e nota metodológica.")

print("\n" + "="*60)
print("AUDITORIA — TODAS AS FIGURAS CORRIGIDAS FORAM RECRIADAS")
print("="*60)
