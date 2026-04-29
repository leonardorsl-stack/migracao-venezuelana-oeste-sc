"""
Auditoria completa do painel longitudinal Oeste SC 2018-2024
"""
from pathlib import Path

import pandas as pd

# ============================================================
# CONFIG
# ============================================================
PAINEL_PATH = Path("data/processed/painel_oeste_sc_2018_2024.parquet")
OUTPUT_REPORT = Path("AUDITORIA_PAINEL.md")
OUTPUT_CORRIGIDO = Path("data/processed/painel_oeste_sc_2018_2024_corrigido.parquet")

relatorio = []
def log(titulo, conteudo=""):
    relatorio.append(f"## {titulo}\n\n{conteudo}\n")

def secao(titulo):
    relatorio.append(f"\n# {titulo}\n")

def subsecao(titulo):
    relatorio.append(f"\n## {titulo}\n")

def bloco(texto):
    relatorio.append(f"\n{texto}\n")

def codigo(texto):
    relatorio.append(f"\n```\n{texto}\n```\n")

# ============================================================
# 1. CARREGAMENTO DO PAINEL
# ============================================================
secao("1. ESTRUTURA E COMPLETUDE")

df = pd.read_parquet(PAINEL_PATH)
bloco(f"**Colunas no painel:** {list(df.columns)}")
bloco(f"**Shape:** {df.shape}")
bloco(f"**Tipos:**\n{df.dtypes}")

# Total de linhas
n_linhas = len(df)
bloco(f"**Total de linhas:** {n_linhas} (esperado: 763)")

# Municípios únicos
municipios_unicos = df['codigo_ibge_7d'].nunique()
bloco(f"**Municípios únicos (7d):** {municipios_unicos} (esperado: 109)")

municipios_unicos_6d = df['codigo_ibge_6d'].nunique()
bloco(f"**Municípios únicos (6d):** {municipios_unicos_6d} (esperado: 109)")

# Anos
anos = sorted(df['ano'].unique())
bloco(f"**Anos:** {anos} (esperado: [2018, 2019, 2020, 2021, 2022, 2023, 2024])")

# Duplicatas
pares = df.groupby(['codigo_ibge_7d', 'ano']).size()
duplicados = pares[pares > 1]
bloco(f"**Duplicatas (municipio, ano):** {len(duplicados)} pares")

# Verificar balanceamento
balanceamento = df.groupby('ano')['codigo_ibge_7d'].nunique()
bloco(f"**Municípios por ano:**\n{balanceamento.to_string()}")

# Verificar colunas esperadas
COLUNAS_ESPERADAS = [
    'codigo_ibge_7d', 'codigo_ibge_6d', 'municipio', 'ano', 'populacao_total',
    'total_vinculos_rais', 'taxa_vinculos_por_mil',
    'total_internacoes_sih', 'dias_permanencia_sih', 'valor_total_sih', 'obitos_hospitalares_sih', 'taxa_internacoes_por_mil',
    'total_obitos', 'total_nascimentos', 'taxa_mortalidade', 'taxa_natalidade'
]
cols_faltantes = [c for c in COLUNAS_ESPERADAS if c not in df.columns]
cols_extras = [c for c in df.columns if c not in COLUNAS_ESPERADAS]
bloco(f"**Colunas faltantes:** {cols_faltantes}")
bloco(f"**Colunas extras:** {cols_extras}")

# NaNs em colunas críticas
nans = df.isnull().sum()
bloco(f"**NaNs por coluna:**\n{nans[nans > 0].to_string() if (nans > 0).any() else 'Nenhum NaN encontrado'}")

# ============================================================
# 2. CONSISTÊNCIA COM DADOS FONTES
# ============================================================
secao("2. CONSISTÊNCIA COM DADOS FONTES")

# --- 2.1 RAIS ---
subsecao("2.1 RAIS → painel")

rais_por_ano = {}
for ano in range(2018, 2025):
    rais_path = Path(f"data/processed/rais_vinculos_sc_venezuela_{ano}.parquet")
    if rais_path.exists():
        dfr = pd.read_parquet(rais_path)
        # Identificar coluna de município
        cols_mun = [c for c in dfr.columns if 'municipio' in c.lower() or 'codigo_ibge' in c.lower() or 'mun' in c.lower()]
        rais_por_ano[ano] = {'df': dfr, 'cols': cols_mun}
        bloco(f"RAIS {ano}: {len(dfr)} registros, cols mun: {cols_mun}")
    else:
        bloco(f"RAIS {ano}: ARQUIVO NÃO ENCONTRADO")

# Vamos verificar a estrutura de um RAIS para entender as colunas
if 2023 in rais_por_ano:
    dfr = rais_por_ano[2023]['df']
    bloco(f"**Amostra RAIS 2023:**\n{dfr.head(3).to_string()}")
    bloco(f"**Colunas RAIS:** {list(dfr.columns)}")

# --- 2.2 SIH ---
subsecao("2.2 SIH/SUS → painel")

sih_path = Path("data/raw/datasus/sih_sus_sc_venezuela_2018_2025.parquet")
if sih_path.exists():
    dfsih = pd.read_parquet(sih_path)
    bloco(f"SIH completo: {len(dfsih)} registros")
    bloco(f"Colunas SIH: {list(dfsih.columns)}")
    bloco(f"Amostra SIH:\n{dfsih.head(3).to_string()}")
else:
    bloco("SIH completo: ARQUIVO NÃO ENCONTRADO")

# --- 2.3 População ---
subsecao("2.3 População IBGE → painel")

pop_path = Path("data/processed/ibge_populacao_estimada_oeste_sc.parquet")
if pop_path.exists():
    dfpop = pd.read_parquet(pop_path)
    bloco(f"População IBGE: {len(dfpop)} registros")
    bloco(f"Colunas: {list(dfpop.columns)}")
    bloco(f"Amostra:\n{dfpop.head(10).to_string()}")
else:
    bloco("População IBGE: ARQUIVO NÃO ENCONTRADO")

# --- 2.4 SIM ---
subsecao("2.4 SIM → painel")

sim_path = Path("data/processed/datasus_sim_oeste_sc.parquet")
if sim_path.exists():
    dfsim = pd.read_parquet(sim_path)
    bloco(f"SIM: {len(dfsim)} registros")
    bloco(f"Colunas: {list(dfsim.columns)}")
    bloco(f"Amostra:\n{dfsim.head(5).to_string()}")
else:
    bloco("SIM: ARQUIVO NÃO ENCONTRADO")

# --- 2.5 SINASC ---
subsecao("2.5 SINASC → painel")

sinasc_path = Path("data/processed/datasus_sinasc_oeste_sc.parquet")
if sinasc_path.exists():
    dfsinasc = pd.read_parquet(dfsinasc_path := sinasc_path)
    bloco(f"SINASC: {len(dfsinasc)} registros")
    bloco(f"Colunas: {list(dfsinasc.columns)}")
    bloco(f"Amostra:\n{dfsinasc.head(5).to_string()}")
else:
    bloco("SINASC: ARQUIVO NÃO ENCONTRADO")

# ============================================================
# SALVAR RELATÓRIO PARCIAL
# ============================================================
with open(OUTPUT_REPORT, 'w') as f:
    f.write("\n".join(relatorio))

print("Parte 1 concluída. Relatório salvo em", OUTPUT_REPORT)
