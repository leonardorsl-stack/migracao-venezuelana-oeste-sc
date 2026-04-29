#!/usr/bin/env python3
"""
Consolida os arquivos Parquet da RAIS ano-a-ano em um único arquivo.
Adiciona nome do município e flags de Região Oeste SC.
"""
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from config import REGIAO_OESTE_SC

DATA_DIR = Path("data/processed")
OUTPUT = DATA_DIR / "rais_vinculos_sc_venezuela_2018_2023.parquet"

# Mapeamento código IBGE → nome (usando API ou cache local)
# Por enquanto, vamos apenas consolidar
anos = list(range(2018, 2024))
frames = []

for ano in anos:
    path = DATA_DIR / f"rais_vinculos_sc_venezuela_{ano}.parquet"
    if path.exists():
        df = pd.read_parquet(path)
        frames.append(df)
        print(f"✓ {ano}: {len(df):,} registros")
    else:
        print(f"✗ {ano}: arquivo não encontrado")

if frames:
    consolidated = pd.concat(frames, ignore_index=True)
    
    # Adiciona flag de Região Oeste SC
    consolidated['regiao_oeste_sc'] = consolidated['municipio'].astype(str).str[:6].astype(int).isin(REGIAO_OESTE_SC)
    
    # Converte município para código IBGE 7d (já vem assim da RAIS)
    consolidated['codigo_ibge_7d'] = consolidated['municipio'].astype(int)
    
    consolidated.to_parquet(OUTPUT, compression='zstd', index=False)
    print(f"\n📦 Consolidado salvo: {OUTPUT}")
    print(f"   Total: {len(consolidated):,} vínculos")
    print(f"   Na Região Oeste SC: {consolidated['regiao_oeste_sc'].sum():,}")
    print(f"   Fora da Região Oeste SC: {(~consolidated['regiao_oeste_sc']).sum():,}")
    print(f"   Período: {consolidated['ano'].min()}–{consolidated['ano'].max()}")
else:
    print("Nenhum arquivo encontrado para consolidar.")
