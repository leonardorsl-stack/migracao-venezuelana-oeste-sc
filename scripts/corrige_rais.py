#!/usr/bin/env python3
"""
Script de correção dos arquivos RAIS processados.

Problemas corrigidos:
1. Padronização do campo sexo (remove espaços, converte '01'->'1', '02'->'2')
2. Remoção da coluna duplicada 'Idade' (I maiúsculo) em 2023-2024

Saída: arquivos com sufixo _corrigido em data/processed/
"""
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/processed")
YEARS = list(range(2018, 2025))

for year in YEARS:
    src = DATA_DIR / f"rais_vinculos_sc_venezuela_{year}.parquet"
    dst = DATA_DIR / f"rais_vinculos_sc_venezuela_{year}_corrigido.parquet"
    
    if not src.exists():
        print(f"[!] Arquivo não encontrado: {src}")
        continue
    
    df = pd.read_parquet(src)
    correcoes = []
    
    # 1. Padronizar sexo
    if 'sexo' in df.columns:
        sexo_antes = df['sexo'].unique()[:5]
        df['sexo'] = df['sexo'].astype(str).str.strip()
        # Mapear variações para '1' e '2'
        df['sexo'] = df['sexo'].replace({
            '01': '1',
            '02': '2',
            '1': '1',
            '2': '2',
            'MASCULINO': '1',
            'FEMININO': '2',
            'M': '1',
            'F': '2',
        })
        # Valores não mapeados viram NA
        df.loc[~df['sexo'].isin(['1', '2']), 'sexo'] = pd.NA
        correcoes.append(f"sexo padronizado (antes: {sexo_antes})")
    
    # 2. Remover coluna 'Idade' duplicada (I maiúsculo)
    if 'Idade' in df.columns:
        df = df.drop(columns=['Idade'])
        correcoes.append("coluna 'Idade' (I maiúsculo) removida")
    
    # Salvar
    df.to_parquet(dst, compression='zstd', index=False)
    print(f"[✓] {year}: {len(df)} registros -> {dst.name}")
    if correcoes:
        print(f"    Correções: {', '.join(correcoes)}")
    else:
        print(f"    Sem alterações necessárias")

print("\nCorreções concluídas.")
