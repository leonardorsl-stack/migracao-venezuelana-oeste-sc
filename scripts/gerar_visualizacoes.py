#!/usr/bin/env python3
"""
Gera 7 visualizações para o projeto migração-venezuelana-oeste-sc.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Configurações globais
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['figure.figsize'] = (12, 8)
sns.set_style("whitegrid")
sns.set_palette("deep")

BASE_DIR = "/Users/leonardosantos/Documents/raio_x_migraçao"
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Carregar dados
# ---------------------------------------------------------------------------
painel = pd.read_parquet(os.path.join(BASE_DIR, "data", "processed", "painel_oeste_sc_2018_2024.parquet"))
painel['ano'] = painel['ano'].astype(int)

# Dados SIH raw para 2025
sih_raw = pd.read_parquet(os.path.join(BASE_DIR, "data", "raw", "datasus", "sih_sus_sc_venezuela_2018_2025.parquet"))
sih_raw['ano'] = sih_raw['ano'].astype(int)

# Códigos IBGE da região oeste (7d do painel)
codigos_oeste = set(painel['codigo_ibge_7d'].unique())

# Preparar mapeamento 6d -> 7d do painel
map_6d_7d = painel[['codigo_ibge_6d', 'codigo_ibge_7d']].drop_duplicates().set_index('codigo_ibge_6d')['codigo_ibge_7d'].to_dict()
sih_raw['MUNIC_RES_6d'] = pd.to_numeric(sih_raw['MUNIC_RES'], errors='coerce').astype(int)

# Agregar SIH por ano (regional) - apenas municípios da região oeste (usando 6d)
sih_regional = sih_raw[sih_raw['MUNIC_RES_6d'].isin(map_6d_7d.keys())].groupby('ano').size().reset_index(name='total_internacoes_sih')

# Agregar SIH por município e ano para 2024/2025 (usando 7d)
sih_mun = (
    sih_raw[sih_raw['MUNIC_RES_6d'].isin(map_6d_7d.keys())]
    .groupby(['MUNIC_RES_6d', 'ano'])
    .size()
    .reset_index(name='total_internacoes_sih')
)
sih_mun['codigo_ibge_7d'] = sih_mun['MUNIC_RES_6d'].map(map_6d_7d)


# ---------------------------------------------------------------------------
# 01. Evolução dos vínculos RAIS regional (2018-2024)
# ---------------------------------------------------------------------------
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
line1 = ax1.plot(reg['ano'], reg['taxa_vinculos_por_mil'], color=color_line, marker='o', linewidth=2.5, markersize=8, label='Taxa por mil hab.')
ax1.tick_params(axis='y', labelcolor=color_line)
ax1.set_xticks(reg['ano'])
ax1.set_ylim(0, reg['taxa_vinculos_por_mil'].max() * 1.15)

# Adicionar rótulos na linha
for x, y in zip(reg['ano'], reg['taxa_vinculos_por_mil']):
    ax1.annotate(f'{y:.1f}', xy=(x, y), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=9, color=color_line)

ax2 = ax1.twinx()
color_bar = '#d62728'
ax2.set_ylabel('Número absoluto de vínculos', color=color_bar, fontsize=13)
bars = ax2.bar(reg['ano'], reg['total_vinculos_rais'], color=color_bar, alpha=0.3, width=0.5, label='Vínculos absolutos')
ax2.tick_params(axis='y', labelcolor=color_bar)
ax2.set_ylim(0, reg['total_vinculos_rais'].max() * 1.3)

# Rótulos nas barras
for bar in bars:
    height = bar.get_height()
    ax2.annotate(f'{int(height):,}'.replace(',', '.'), xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, color=color_bar)

fig.suptitle('Evolução da Inserção Laboral de Venezuelanos no Oeste de SC', fontsize=15, fontweight='bold')
fig.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '01_evolucao_vinculos_regional.png'), bbox_inches='tight')
plt.close()

# ---------------------------------------------------------------------------
# 02. Top 20 municípios por taxa de vínculos (2024) — barras horizontais
# ---------------------------------------------------------------------------
p2024 = painel[painel['ano'] == 2024].copy()
top20 = p2024.nlargest(20, 'taxa_vinculos_por_mil').sort_values('taxa_vinculos_por_mil')

fig, ax = plt.subplots(figsize=(12, 10))
colors = sns.color_palette("coolwarm_r", n_colors=20)
colors = [c if mun != 'Chapecó' else '#d62728' for c, mun in zip(colors, top20['municipio'])]

bars = ax.barh(top20['municipio'], top20['taxa_vinculos_por_mil'], color=colors, edgecolor='black', linewidth=0.3)
for bar, val in zip(bars, top20['taxa_vinculos_por_mil']):
    ax.text(val + 2, bar.get_y() + bar.get_height()/2, f'{val:.1f}', va='center', fontsize=9)

ax.set_xlabel('Taxa de vínculos RAIS por mil habitantes', fontsize=13)
ax.set_title('Top 20 Municípios — Taxa de Vínculos por Mil Habitantes (2024)\nChapecó destacada em vermelho (maior volume absoluto)', fontsize=14, fontweight='bold')
ax.set_xlim(0, top20['taxa_vinculos_por_mil'].max() * 1.2)
ax.axhline(y='Chapecó', color='red', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '02_mapa_taxa_vinculos_2024.png'), bbox_inches='tight')
plt.close()

# ---------------------------------------------------------------------------
# 03. Top 15 municípios por volume absoluto (2024)
# ---------------------------------------------------------------------------
top15_vol = p2024.nlargest(15, 'total_vinculos_rais').sort_values('total_vinculos_rais', ascending=True)
fig, ax = plt.subplots(figsize=(12, 8))
colors = ['#d62728' if i >= len(top15_vol)-3 else '#4c72b0' for i in range(len(top15_vol))]

bars = ax.barh(top15_vol['municipio'], top15_vol['total_vinculos_rais'], color=colors, edgecolor='black', linewidth=0.3)
for bar, val in zip(bars, top15_vol['total_vinculos_rais']):
    ax.text(val + 50, bar.get_y() + bar.get_height()/2, f'{int(val):,}'.replace(',', '.'), va='center', fontsize=10)

ax.set_xlabel('Número de vínculos RAIS', fontsize=13)
ax.set_title('Top 15 Municípios — Vínculos RAIS de Venezuelanos (2024)\nTop 3 destacados em vermelho', fontsize=14, fontweight='bold')
ax.set_xlim(0, top15_vol['total_vinculos_rais'].max() * 1.15)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '03_top15_municipios_volume_2024.png'), bbox_inches='tight')
plt.close()

# ---------------------------------------------------------------------------
# 04. Dispersão população vs vínculos (2024)
# ---------------------------------------------------------------------------
p2024_nonzero = p2024[p2024['total_vinculos_rais'] > 0].copy()
if p2024_nonzero.empty:
    p2024_nonzero = p2024.copy()

fig, ax = plt.subplots(figsize=(12, 8))
scatter = ax.scatter(p2024_nonzero['populacao_total'], p2024_nonzero['total_vinculos_rais'],
                     s=p2024_nonzero['taxa_vinculos_por_mil']*3,
                     c=p2024_nonzero['taxa_vinculos_por_mil'], cmap='viridis',
                     alpha=0.7, edgecolors='black', linewidth=0.5)

# Rótulos para municípios extremos
muns_destaque = ['Chapecó', 'Guatambú', 'Itapiranga', 'Seara']
for _, row in p2024_nonzero.iterrows():
    if row['municipio'] in muns_destaque:
        ax.annotate(row['municipio'], (row['populacao_total'], row['total_vinculos_rais']),
                    textcoords="offset points", xytext=(8, 5), fontsize=10, fontweight='bold')

# Linha de regressão
x = p2024_nonzero['populacao_total']
y = p2024_nonzero['total_vinculos_rais']
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
ax.plot(x, slope*x + intercept, color='red', linestyle='--', linewidth=2, label=f'Regressão (R²={r_value**2:.3f})')

ax.set_xlabel('População total (2024)', fontsize=13)
ax.set_ylabel('Número de vínculos RAIS (2024)', fontsize=13)
ax.set_title('População vs Vínculos RAIS de Venezuelanos por Município (2024)\nTamanho do ponto proporcional à taxa por mil habitantes', fontsize=14, fontweight='bold')
ax.legend(loc='upper left')
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Taxa de vínculos por mil habitantes', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '04_dispersao_populacao_vs_vinculos.png'), bbox_inches='tight')
plt.close()

# ---------------------------------------------------------------------------
# 05. Evolução internações SIH (2018-2025) + comparação com vínculos
# ---------------------------------------------------------------------------
# Dados do painel (2018-2024)
reg_painel = (
    painel.groupby('ano')
    .agg(populacao_total=('populacao_total', 'sum'),
         total_internacoes_sih=('total_internacoes_sih', 'sum'),
         total_vinculos_rais=('total_vinculos_rais', 'sum'))
    .reset_index()
)

# Adicionar 2025 do SIH raw
intern_2025 = sih_regional[sih_regional['ano'] == 2025]['total_internacoes_sih'].sum()
pop_2024 = reg_painel[reg_painel['ano'] == 2024]['populacao_total'].values[0]
reg_2025 = pd.DataFrame({'ano': [2025], 'populacao_total': [pop_2024], 'total_internacoes_sih': [intern_2025], 'total_vinculos_rais': [np.nan]})
reg_full = pd.concat([reg_painel, reg_2025], ignore_index=True)

fig, ax1 = plt.subplots(figsize=(12, 7))
color_line = '#2ca02c'
ax1.set_xlabel('Ano', fontsize=13)
ax1.set_ylabel('Internações SIH (total regional)', color=color_line, fontsize=13)
ax1.plot(reg_full['ano'], reg_full['total_internacoes_sih'], color=color_line, marker='s', linewidth=2.5, markersize=8, label='Internações SIH')
ax1.tick_params(axis='y', labelcolor=color_line)
ax1.set_xticks(reg_full['ano'])

for x, y in zip(reg_full['ano'], reg_full['total_internacoes_sih']):
    ax1.annotate(f'{int(y)}', xy=(x, y), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=9, color=color_line)

ax2 = ax1.twinx()
color_line2 = '#1f77b4'
ax2.set_ylabel('Vínculos RAIS (total regional)', color=color_line2, fontsize=13)
ax2.plot(reg_full['ano'][:-1], reg_full['total_vinculos_rais'][:-1], color=color_line2, marker='o', linewidth=2.5, markersize=8, linestyle='--', label='Vínculos RAIS')
ax2.tick_params(axis='y', labelcolor=color_line2)

for x, y in zip(reg_full['ano'][:-1], reg_full['total_vinculos_rais'][:-1]):
    ax2.annotate(f'{int(y):,}'.replace(',', '.'), xy=(x, y), textcoords="offset points", xytext=(0, -15), ha='center', fontsize=9, color=color_line2)

fig.suptitle('Evolução das Internações SIH e Vínculos RAIS de Venezuelanos no Oeste de SC (2018-2025)', fontsize=14, fontweight='bold')
fig.legend(loc='upper left', bbox_to_anchor=(0.12, 0.88))
fig.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '05_evolucao_internacoes_sih.png'), bbox_inches='tight')
plt.close()

# ---------------------------------------------------------------------------
# 06. Comparativo RAIS vs SIH por município — top 15 (2024)
# ---------------------------------------------------------------------------
# Juntar dados do painel 2024 com SIH 2024 (do painel já temos, mas usar o SIH raw para consistência)
p2024_sih_raw = sih_mun[sih_mun['ano'] == 2024].rename(columns={'total_internacoes_sih': 'total_internacoes_sih_raw'})
comp = p2024.merge(p2024_sih_raw[['codigo_ibge_7d', 'total_internacoes_sih_raw']], on='codigo_ibge_7d', how='left')
comp['total_internacoes_sih_raw'] = comp['total_internacoes_sih_raw'].fillna(0).astype(int)

# Usar os dados do painel para internações (mais completos com população) — para comparabilidade normalizada
# Vou criar duas versões no mesmo gráfico: absoluta + eixo secundário normalizado
# Mas a tarefa pede barras duplas grouped. Vou fazer grouped bar com top 15 por soma
comp['soma'] = comp['total_vinculos_rais'] + comp['total_internacoes_sih']
top15_comp = comp.nlargest(15, 'soma').sort_values('soma', ascending=True)

fig, ax = plt.subplots(figsize=(14, 9))
y_pos = np.arange(len(top15_comp))
bar_width = 0.35

bars1 = ax.barh(y_pos - bar_width/2, top15_comp['total_vinculos_rais'], bar_width, label='Vínculos RAIS', color='#1f77b4', edgecolor='black', linewidth=0.3)
bars2 = ax.barh(y_pos + bar_width/2, top15_comp['total_internacoes_sih'], bar_width, label='Internações SIH', color='#ff7f0e', edgecolor='black', linewidth=0.3)

ax.set_yticks(y_pos)
ax.set_yticklabels(top15_comp['municipio'])
ax.set_xlabel('Quantidade absoluta', fontsize=13)
ax.set_title('Comparativo Vínculos RAIS vs Internações SIH — Top 15 Municípios (2024)', fontsize=14, fontweight='bold')
ax.legend(loc='lower right')

for bar in bars1:
    width = bar.get_width()
    if width > 0:
        ax.text(width + 30, bar.get_y() + bar.get_height()/2, f'{int(width):,}'.replace(',', '.'), va='center', fontsize=8)
for bar in bars2:
    width = bar.get_width()
    if width > 0:
        ax.text(width + 30, bar.get_y() + bar.get_height()/2, f'{int(width):,}'.replace(',', '.'), va='center', fontsize=8)

ax.set_xlim(0, max(top15_comp['total_vinculos_rais'].max(), top15_comp['total_internacoes_sih'].max()) * 1.25)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '06_comparativo_rais_vs_sih_2024.png'), bbox_inches='tight')
plt.close()

# ---------------------------------------------------------------------------
# 07. Dispersão taxa vínculos vs taxa internações (2024)
# ---------------------------------------------------------------------------
p2024_nz = p2024[(p2024['taxa_vinculos_por_mil'] > 0) | (p2024['taxa_internacoes_por_mil'] > 0)].copy()

fig, ax = plt.subplots(figsize=(12, 8))
scatter = ax.scatter(p2024_nz['taxa_vinculos_por_mil'], p2024_nz['taxa_internacoes_por_mil'],
                     s=p2024_nz['populacao_total']/500,
                     c=range(len(p2024_nz)), cmap='tab20', alpha=0.7, edgecolors='black', linewidth=0.5)

# Regressão
x = p2024_nz['taxa_vinculos_por_mil']
y = p2024_nz['taxa_internacoes_por_mil']
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
ax.plot(x, slope*x + intercept, color='red', linestyle='--', linewidth=2, label=f'Regressão (R²={r_value**2:.3f})')

# Outliers: pontos com maiores resíduos
pred = slope * x + intercept
residuals = np.abs(y - pred)
outlier_idx = residuals.nlargest(5).index
for idx in outlier_idx:
    row = p2024_nz.loc[idx]
    ax.annotate(row['municipio'], (row['taxa_vinculos_por_mil'], row['taxa_internacoes_por_mil']),
                textcoords="offset points", xytext=(8, 5), fontsize=9)

ax.set_xlabel('Taxa de vínculos RAIS por mil habitantes', fontsize=13)
ax.set_ylabel('Taxa de internações SIH por mil habitantes', fontsize=13)
ax.set_title('Taxa de Vínculos RAIS vs Taxa de Internações SIH por Município (2024)\nTamanho do ponto proporcional à população total', fontsize=14, fontweight='bold')
ax.legend(loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '07_taxa_internacoes_vs_vinculos.png'), bbox_inches='tight')
plt.close()

# ---------------------------------------------------------------------------
# Verificação final
# ---------------------------------------------------------------------------
print("Visualizações geradas com sucesso:")
for f in sorted(os.listdir(OUTPUT_DIR)):
    if f.endswith('.png'):
        size_kb = os.path.getsize(os.path.join(OUTPUT_DIR, f)) / 1024
        print(f"  {f}: {size_kb:.1f} KB")
