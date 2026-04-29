"""
Script de correção do painel longitudinal Oeste SC 2018-2024
"""
from pathlib import Path

import numpy as np
import pandas as pd

PAINEL_PATH = Path("data/processed/painel_oeste_sc_2018_2024.parquet")
OUTPUT_CORRIGIDO = Path("data/processed/painel_oeste_sc_2018_2024_corrigido.parquet")

print("Carregando painel...")
df = pd.read_parquet(PAINEL_PATH)
print(f"Shape original: {df.shape}")

# ============================================================
# CORREÇÃO 1: SINASC 2023 → NaN
# ============================================================
# A fonte SINASC só tem dados até 2022.
# O painel preencheu 2023 com 0.0 em vez de NaN.
print("\nCorrigindo SINASC 2023...")
mask_2023 = df['ano'] == 2023
antes_nasc = df.loc[mask_2023, 'total_nascimentos'].unique()
antes_taxa = df.loc[mask_2023, 'taxa_natalidade'].unique()
print(f"  Antes: total_nascimentos={antes_nasc}, taxa_natalidade={antes_taxa}")

df.loc[mask_2023, 'total_nascimentos'] = np.nan
df.loc[mask_2023, 'taxa_natalidade'] = np.nan

depois_nasc = df.loc[mask_2023, 'total_nascimentos'].unique()
depois_taxa = df.loc[mask_2023, 'taxa_natalidade'].unique()
print(f"  Depois: total_nascimentos={depois_nasc}, taxa_natalidade={depois_taxa}")

# ============================================================
# VERIFICAÇÃO FINAL
# ============================================================
print("\n=== Verificação pós-correção ===")
print("NaNs em total_nascimentos por ano:")
print(df.groupby('ano')['total_nascimentos'].apply(lambda x: x.isnull().sum()))

print("\nNaNs em taxa_natalidade por ano:")
print(df.groupby('ano')['taxa_natalidade'].apply(lambda x: x.isnull().sum()))

# ============================================================
# SALVAR
# ============================================================
print(f"\nSalvando painel corrigido em {OUTPUT_CORRIGIDO}...")
df.to_parquet(OUTPUT_CORRIGIDO, index=False)
print("Concluído!")
