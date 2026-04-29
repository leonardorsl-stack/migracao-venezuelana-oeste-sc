#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera pirâmide etária comparativa entre venezuelanos (RAIS) e população total
do Oeste SC (Região Intermediária de Chapecó - 109 municípios).

Entradas:
- RAIS 2023-2024: data/processed/rais_vinculos_sc_venezuela_202{3,4}.parquet
- IBGE Censo 2022: data/processed/ibge_populacao_idade_sexo_oeste_sc_2022.parquet

Saídas:
- outputs/figures/12_piramide_etaria_venezuelanos_vs_total.png
- outputs/figures/13_comparativo_faixa_etaria_percentual.png
- outputs/figures/17_indice_concentracao_etaria.png
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pathlib import Path

# ---------------------------------------------------------------------------
# 1. CONFIGURAÇÕES
# ---------------------------------------------------------------------------
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9

OUTPUT_DIR = Path('outputs/figures')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FAIXAS = ['15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60+']

# Cores
COR_MASC_OESTE = '#1f77b4'
COR_FEM_OESTE = '#ff7f0e'
COR_MASC_VEN = '#2ca02c'
COR_FEM_VEN = '#d62728'


def faixa_etaria_rais(idade: int) -> str:
    if 15 <= idade <= 19:
        return '15-19'
    if 20 <= idade <= 24:
        return '20-24'
    if 25 <= idade <= 29:
        return '25-29'
    if 30 <= idade <= 34:
        return '30-34'
    if 35 <= idade <= 39:
        return '35-39'
    if 40 <= idade <= 44:
        return '40-44'
    if 45 <= idade <= 49:
        return '45-49'
    if 50 <= idade <= 54:
        return '50-54'
    if 55 <= idade <= 59:
        return '55-59'
    if idade >= 60:
        return '60+'
    return None


def faixa_etaria_ibge(idade_label: str) -> str:
    # O IBGE já tem faixas de 5 anos para maiores de 5
    mapping = {
        '15 a 19 anos': '15-19',
        '20 a 24 anos': '20-24',
        '25 a 29 anos': '25-29',
        '30 a 34 anos': '30-34',
        '35 a 39 anos': '35-39',
        '40 a 44 anos': '40-44',
        '45 a 49 anos': '45-49',
        '50 a 54 anos': '50-54',
        '55 a 59 anos': '55-59',
        '60 a 64 anos': '60+',
        '65 a 69 anos': '60+',
        '70 a 74 anos': '60+',
        '75 a 79 anos': '60+',
        '80 a 84 anos': '60+',
        '85 a 89 anos': '60+',
        '90 a 94 anos': '60+',
        '95 a 99 anos': '60+',
        '100 anos ou mais': '60+',
    }
    return mapping.get(idade_label, None)


# ---------------------------------------------------------------------------
# 2. DADOS RAIS (Venezuelanos em SC, Oeste)
# ---------------------------------------------------------------------------
print("Carregando RAIS 2023-2024...")
df23 = pd.read_parquet('data/processed/rais_vinculos_sc_venezuela_2023.parquet')
df24 = pd.read_parquet('data/processed/rais_vinculos_sc_venezuela_2024.parquet')
df_rais = pd.concat([df23, df24], ignore_index=True)

# Padronizar colunas
df_rais['sexo'] = df_rais['sexo'].astype(str).str.strip()
df_rais['idade'] = pd.to_numeric(df_rais['idade'], errors='coerce')

# Mapear sexo: RAIS 1=Masculino, 2=Feminino
df_rais['sexo_label'] = df_rais['sexo'].map({'1': 'Homens', '2': 'Mulheres'})

# Criar faixa etária
df_rais['faixa'] = df_rais['idade'].apply(faixa_etaria_rais)
df_rais = df_rais.dropna(subset=['faixa', 'sexo_label'])

# Agrupar
rais_counts = df_rais.groupby(['faixa', 'sexo_label']).size().reset_index(name='count')
rais_total = rais_counts['count'].sum()
rais_counts['pct'] = rais_counts['count'] / rais_total * 100

rais_pivot = rais_counts.pivot(index='faixa', columns='sexo_label', values='pct').reindex(FAIXAS)
rais_pivot = rais_pivot.fillna(0)

print("RAIS - Totais por sexo:")
print(df_rais['sexo_label'].value_counts())
print("RAIS - % por faixa:")
print(rais_pivot)

# ---------------------------------------------------------------------------
# 3. DADOS IBGE (População total Oeste SC)
# ---------------------------------------------------------------------------
print("\nCarregando IBGE Censo 2022 Oeste SC...")
df_ibge = pd.read_parquet('data/processed/ibge_populacao_idade_sexo_oeste_sc_2022.parquet')

# Filtrar apenas sexo = Homens ou Mulheres (excluir Total)
df_ibge = df_ibge[df_ibge['D4N'].isin(['Homens', 'Mulheres'])].copy()

# Converter valor para numérico
df_ibge['pop'] = pd.to_numeric(df_ibge['V'], errors='coerce')

# Criar faixa etária
df_ibge['faixa'] = df_ibge['D5N'].apply(faixa_etaria_ibge)
df_ibge = df_ibge.dropna(subset=['faixa'])

# Agrupar por faixa e sexo
ibge_counts = df_ibge.groupby(['faixa', 'D4N'])['pop'].sum().reset_index()
ibge_total = ibge_counts['pop'].sum()
ibge_counts['pct'] = ibge_counts['pop'] / ibge_total * 100

ibge_pivot = ibge_counts.pivot(index='faixa', columns='D4N', values='pct').reindex(FAIXAS)
ibge_pivot = ibge_pivot.fillna(0)

print("IBGE - Totais por sexo:")
print(df_ibge.groupby('D4N')['pop'].sum())
print("IBGE - % por faixa:")
print(ibge_pivot)

# ---------------------------------------------------------------------------
# 4. GRÁFICO 1: Pirâmide lado a lado (subplots)
# ---------------------------------------------------------------------------
print("\nGerando Gráfico 1: Pirâmide lado a lado...")

fig, axes = plt.subplots(1, 2, figsize=(14, 8), sharey=True)

y_pos = np.arange(len(FAIXAS))
bar_height = 0.35

# --- Esquerda: População total Oeste SC ---
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
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{abs(x):.1f}'))
ax.axvline(0, color='black', linewidth=0.8)
ax.legend(loc='lower right')
ax.grid(axis='x', alpha=0.3)

# --- Direita: Venezuelanos RAIS ---
ax = axes[1]
ax.barh(y_pos + bar_height/2, -rais_pivot['Homens'], height=bar_height,
        color=COR_MASC_VEN, label='Homens', edgecolor='white', linewidth=0.3)
ax.barh(y_pos - bar_height/2, rais_pivot['Mulheres'], height=bar_height,
        color=COR_FEM_VEN, label='Mulheres', edgecolor='white', linewidth=0.3)
ax.set_yticks(y_pos)
ax.set_yticklabels(FAIXAS)
ax.set_xlabel('Percentual (%)')
ax.set_title('Venezuelanos\nRAIS 2023-2024', fontweight='bold')
ax.set_xlim(-8, 8)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{abs(x):.1f}'))
ax.axvline(0, color='black', linewidth=0.8)
ax.legend(loc='lower right')
ax.grid(axis='x', alpha=0.3)

fig.suptitle('Pirâmide Etária Comparativa: Oeste SC vs. Venezuelanos', fontsize=14, fontweight='bold', y=1.02)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / '12_piramide_etaria_venezuelanos_vs_total.png', bbox_inches='tight')
plt.close(fig)
print(f"  Salvo: {OUTPUT_DIR / '12_piramide_etaria_venezuelanos_vs_total.png'}")

# ---------------------------------------------------------------------------
# 5. GRÁFICO 2: Barras agrupadas comparando as duas populações
# ---------------------------------------------------------------------------
print("\nGerando Gráfico 2: Comparativo percentual...")

fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

x = np.arange(len(FAIXAS))
width = 0.25

# --- Homens ---
ax = axes[0]
rects1 = ax.bar(x - width/2, ibge_pivot['Homens'], width, label='Oeste SC', color=COR_MASC_OESTE, edgecolor='white', linewidth=0.3)
rects2 = ax.bar(x + width/2, rais_pivot['Homens'], width, label='Venezuelanos', color=COR_MASC_VEN, edgecolor='white', linewidth=0.3)
ax.set_ylabel('Percentual (%)')
ax.set_title('Homens', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(FAIXAS, rotation=45, ha='right')
ax.legend()
ax.grid(axis='y', alpha=0.3)

# --- Mulheres ---
ax = axes[1]
rects1 = ax.bar(x - width/2, ibge_pivot['Mulheres'], width, label='Oeste SC', color=COR_FEM_OESTE, edgecolor='white', linewidth=0.3)
rects2 = ax.bar(x + width/2, rais_pivot['Mulheres'], width, label='Venezuelanos', color=COR_FEM_VEN, edgecolor='white', linewidth=0.3)
ax.set_ylabel('Percentual (%)')
ax.set_title('Mulheres', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(FAIXAS, rotation=45, ha='right')
ax.legend()
ax.grid(axis='y', alpha=0.3)

fig.suptitle('Distribuição Etária por Sexo: Oeste SC vs. Venezuelanos (RAIS)', fontsize=13, fontweight='bold', y=1.02)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / '13_comparativo_faixa_etaria_percentual.png', bbox_inches='tight')
plt.close(fig)
print(f"  Salvo: {OUTPUT_DIR / '13_comparativo_faixa_etaria_percentual.png'}")

# ---------------------------------------------------------------------------
# 6. GRÁFICO 3: Índice de concentração
# ---------------------------------------------------------------------------
print("\nGerando Gráfico 3: Índice de concentração...")

# Calcular % totais (independentemente de sexo)
rais_total_by_faixa = rais_counts.groupby('faixa')['count'].sum().reindex(FAIXAS)
rais_total_pct = rais_total_by_faixa / rais_total_by_faixa.sum() * 100

ibge_total_by_faixa = ibge_counts.groupby('faixa')['pop'].sum().reindex(FAIXAS)
ibge_total_pct = ibge_total_by_faixa / ibge_total_by_faixa.sum() * 100

# Índice = % venezuelanos / % população total
indice = (rais_total_pct / ibge_total_pct).reindex(FAIXAS)
indice = indice.replace([np.inf, -np.inf], np.nan).fillna(0)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(FAIXAS, indice, marker='o', color='#2c3e50', linewidth=2.5, markersize=8)
ax.axhline(1, color='red', linestyle='--', linewidth=1.5, label='Paridade (índice = 1)')
ax.fill_between(FAIXAS, 1, indice, where=(indice > 1), alpha=0.2, color='green', label='Super-representação')
ax.fill_between(FAIXAS, 1, indice, where=(indice < 1), alpha=0.2, color='red', label='Sub-representação')
ax.set_xlabel('Faixa etária')
ax.set_ylabel('Índice de concentração')
ax.set_title('Índice de Concentração Etária de Venezuelanos\n(% venezuelanos na faixa / % população total na faixa)', fontweight='bold')
ax.set_xticks(range(len(FAIXAS)))
ax.set_xticklabels(FAIXAS, rotation=45, ha='right')
ax.legend()
ax.grid(alpha=0.3)

# Anotações nos pontos
for i, v in enumerate(indice):
    ax.annotate(f'{v:.1f}', (i, v), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)

fig.tight_layout()
fig.savefig(OUTPUT_DIR / '17_indice_concentracao_etaria.png', bbox_inches='tight')
plt.close(fig)
print(f"  Salvo: {OUTPUT_DIR / '17_indice_concentracao_etaria.png'}")

# ---------------------------------------------------------------------------
# 7. RELATÓRIO TEXTO
# ---------------------------------------------------------------------------
print("\n" + "="*70)
print("RELATÓRIO: DISTRIBUIÇÃO ETÁRIA")
print("="*70)

print("\n--- POPULAÇÃO TOTAL OESTE SC (Censo 2022, 109 municípios) ---")
for faixa in FAIXAS:
    h = ibge_pivot.loc[faixa, 'Homens']
    m = ibge_pivot.loc[faixa, 'Mulheres']
    t = h + m
    print(f"{faixa:>6}: {t:6.2f}%  (H: {h:5.2f}% | M: {m:5.2f}%)")

print("\n--- VENEZUELANOS RAIS (2023-2024) ---")
for faixa in FAIXAS:
    h = rais_pivot.loc[faixa, 'Homens']
    m = rais_pivot.loc[faixa, 'Mulheres']
    t = h + m
    print(f"{faixa:>6}: {t:6.2f}%  (H: {h:5.2f}% | M: {m:5.2f}%)")

print("\n--- ÍNDICE DE CONCENTRAÇÃO ---")
for faixa in FAIXAS:
    print(f"{faixa:>6}: {indice[faixa]:6.2f}")

print("\n" + "="*70)
print("Concluído com sucesso!")
print("="*70)
