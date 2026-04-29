"""
Auditoria completa do painel longitudinal Oeste SC 2018-2024 - VERSÃO FINAL
"""
from pathlib import Path

import numpy as np
import pandas as pd

# ============================================================
# CONFIG
# ============================================================
PAINEL_PATH = Path("data/processed/painel_oeste_sc_2018_2024.parquet")
OUTPUT_REPORT = Path("AUDITORIA_PAINEL.md")
OUTPUT_CORRIGIDO = Path("data/processed/painel_oeste_sc_2018_2024_corrigido.parquet")

relatorio = []
issues = []
correcoes_necessarias = False

def secao(t):
    relatorio.append(f"\n# {t}\n")

def subsecao(t):
    relatorio.append(f"\n## {t}\n")

def bloco(t):
    relatorio.append(f"\n{t}\n")

def codigo(t):
    relatorio.append(f"\n```\n{t}\n```\n")

def issue(t):
    issues.append(t)
    relatorio.append(f"\n⚠️ **PROBLEMA:** {t}\n")

def ok(t):
    relatorio.append(f"\n✅ **OK:** {t}\n")

def aviso(t):
    relatorio.append(f"\nℹ️ **AVISO:** {t}\n")

# ============================================================
# CARREGAMENTO
# ============================================================
df = pd.read_parquet(PAINEL_PATH)
painel_mun_6d = set(df['codigo_ibge_6d'].unique())
painel_mun_7d = set(df['codigo_ibge_7d'].unique())

# ============================================================
# 1. ESTRUTURA E COMPLETUDE
# ============================================================
secao("1. ESTRUTURA E COMPLETUDE")

n_linhas = len(df)
bloco(f"**Total de linhas:** {n_linhas} (esperado: 763)")
if n_linhas == 763:
    ok("Total de linhas = 763")
else:
    issue(f"Total de linhas = {n_linhas}, esperado 763")

municipios_unicos = df['codigo_ibge_7d'].nunique()
bloco(f"**Municípios únicos (7d):** {municipios_unicos} (esperado: 109)")
if municipios_unicos == 109:
    ok("Municípios únicos = 109")
else:
    issue(f"Municípios únicos = {municipios_unicos}, esperado 109")

anos = sorted(df['ano'].unique())
bloco(f"**Anos presentes:** {anos}")
if anos == [2018, 2019, 2020, 2021, 2022, 2023, 2024]:
    ok("Anos completos 2018-2024")
else:
    issue(f"Anos incompletos: {anos}")

balanceamento = df.groupby('ano')['codigo_ibge_7d'].nunique()
bloco(f"**Municípios por ano:**\n{balanceamento.to_string()}")
if (balanceamento == 109).all():
    ok("109 municípios em cada ano")
else:
    issue(f"Desbalanceamento: {balanceamento.to_dict()}")

pares = df.groupby(['codigo_ibge_7d', 'ano']).size()
duplicados = pares[pares > 1]
bloco(f"**Duplicatas (municipio, ano):** {len(duplicados)}")
if len(duplicados) == 0:
    ok("Sem duplicatas")
else:
    issue(f"{len(duplicados)} duplicatas encontradas")

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
if not cols_faltantes and not cols_extras:
    ok("Colunas correspondem exatamente ao esperado")
else:
    issue(f"Divergência de colunas. Faltantes: {cols_faltantes}, Extras: {cols_extras}")

nans = df.isnull().sum()
bloco(f"**NaNs por coluna:**\n{nans[nans > 0].to_string() if (nans > 0).any() else 'Nenhum NaN'}")

nans_ano = df[df.isnull().any(axis=1)]['ano'].value_counts().sort_index()
bloco(f"**Linhas com NaN por ano:**\n{nans_ano.to_string()}")

nans_obitos_2024 = df[(df['ano']==2024) & (df['total_obitos'].isnull())].shape[0]
nans_nasc_2023 = df[(df['ano']==2023) & (df['total_nascimentos'].isnull())].shape[0]
nans_nasc_2024 = df[(df['ano']==2024) & (df['total_nascimentos'].isnull())].shape[0]
bloco(f"**NaNs estruturais:** obitos_2024={nans_obitos_2024}, nasc_2023={nans_nasc_2023}, nasc_2024={nans_nasc_2024}")

# Verificação: SIM tem até 2023 (109×6=654), SINASC tem até 2022 (109×5=545)
# Portanto: 2024 deve ter obitos=NaN, 2023-2024 devem ter nascimentos=NaN
if nans_obitos_2024 == 109 and nans_nasc_2023 == 109 and nans_nasc_2024 == 109:
    ok("NaNs estruturais corretos: SIM sem 2024, SINASC sem 2023-2024")
elif nans_obitos_2024 == 109 and nans_nasc_2023 == 0 and nans_nasc_2024 == 109:
    issue("SINASC 2023 está como 0.0 em vez de NaN (SINASC só tem dados até 2022)")
    correcoes_necessarias = True
else:
    issue(f"NaNs estruturais inesperados: obitos_2024={nans_obitos_2024}, nasc_2023={nans_nasc_2023}, nasc_2024={nans_nasc_2024}")
    correcoes_necessarias = True

# ============================================================
# 2. CONSISTÊNCIA COM DADOS FONTES
# ============================================================
secao("2. CONSISTÊNCIA COM DADOS FONTES")

# --- 2.1 RAIS ---
subsecao("2.1 RAIS → painel")

for ano in range(2018, 2025):
    rais_path = Path(f"data/processed/rais_vinculos_sc_venezuela_{ano}.parquet")
    dfr = pd.read_parquet(rais_path)
    dfr['municipio_int'] = dfr['municipio'].astype(int)
    dfr_filtrado = dfr[dfr['municipio_int'].isin(painel_mun_6d)]

    soma_rais = len(dfr_filtrado)
    soma_painel = df[df['ano']==ano]['total_vinculos_rais'].sum()

    # Verificar município a município
    rais_agg = dfr_filtrado.groupby('municipio_int').size().reset_index(name='bruto')
    painel_ano = df[df['ano']==ano][['codigo_ibge_6d', 'total_vinculos_rais']].copy()
    merge = painel_ano.merge(rais_agg, left_on='codigo_ibge_6d', right_on='municipio_int', how='outer')
    merge = merge.fillna(0)
    diff = merge[merge['total_vinculos_rais'] != merge['bruto']]

    bloco(f"**RAIS {ano}:** Painel={soma_painel}, Bruto filtrado={soma_rais}, Diff={soma_painel-soma_rais}, Municípios divergentes={len(diff)}")
    if len(diff) > 0:
        issue(f"RAIS {ano}: {len(diff)} municípios divergentes")
        correcoes_necessarias = True
    else:
        ok(f"RAIS {ano}: total bate ({soma_painel})")

# --- 2.2 SIH ---
subsecao("2.2 SIH/SUS → painel")

dfsih = pd.read_parquet("data/raw/datasus/sih_sus_sc_venezuela_2018_2025.parquet")
dfsih['MUNIC_RES_INT'] = dfsih['MUNIC_RES'].astype(int)
dfsih_filtrado = dfsih[dfsih['MUNIC_RES_INT'].isin(painel_mun_6d)]

bloco(f"SIH total: {len(dfsih)}, filtrado Oeste SC: {len(dfsih_filtrado)}, municípios no SIH: {dfsih_filtrado['MUNIC_RES_INT'].nunique()}")

sih_agg = dfsih_filtrado.groupby(['ano', 'MUNIC_RES_INT']).agg(
    total_internacoes_sih_bruto=('ano', 'size'),
    dias_permanencia_sih_bruto=('DIAS_PERM', 'sum'),
    valor_total_sih_bruto=('VAL_TOT', 'sum'),
    obitos_hospitalares_sih_bruto=('MORTE', lambda x: (x == 1).sum())
).reset_index()

for ano in range(2018, 2025):
    painel_ano = df[df['ano']==ano][['codigo_ibge_6d', 'total_internacoes_sih', 'dias_permanencia_sih', 'valor_total_sih', 'obitos_hospitalares_sih']].copy()
    sih_ano = sih_agg[sih_agg['ano']==ano].copy()

    merge = painel_ano.merge(sih_ano, left_on='codigo_ibge_6d', right_on='MUNIC_RES_INT', how='outer')
    merge = merge.fillna(0)

    for col in ['total_internacoes_sih', 'dias_permanencia_sih', 'valor_total_sih', 'obitos_hospitalares_sih']:
        col_bruto = col + '_bruto'
        diff = merge[merge[col] != merge[col_bruto]]
        soma_painel = merge[col].sum()
        soma_bruto = merge[col_bruto].sum()
        bloco(f"**SIH {ano} {col}:** Painel={soma_painel:.0f}, Bruto={soma_bruto:.0f}, Divergentes={len(diff)}")
        if len(diff) > 0:
            issue(f"SIH {ano} {col}: {len(diff)} divergências")
            correcoes_necessarias = True
        else:
            ok(f"SIH {ano} {col}: bate")

# --- 2.3 População ---
subsecao("2.3 População IBGE → painel")

dfpop = pd.read_parquet("data/processed/ibge_populacao_estimada_oeste_sc.parquet")
bloco(f"População fonte: {len(dfpop)} registros, anos: {sorted(dfpop['ano'].unique())}")

merge_pop = df[['codigo_ibge_7d', 'ano', 'populacao_total']].merge(
    dfpop[['codigo_ibge_7d', 'ano', 'populacao']],
    on=['codigo_ibge_7d', 'ano'],
    how='outer'
)
merge_pop = merge_pop.fillna(0)
diff_pop = merge_pop[merge_pop['populacao_total'] != merge_pop['populacao']]
bloco(f"**Divergências população:** {len(diff_pop)}")
if len(diff_pop) > 0:
    issue(f"População: {len(diff_pop)} divergências entre painel e fonte IBGE")
    bloco(diff_pop.head(10).to_string())
    correcoes_necessarias = True
else:
    ok("População: painel bate com fonte IBGE")

# --- 2.4 SIM ---
subsecao("2.4 SIM → painel")

dfsim = pd.read_parquet("data/processed/datasus_sim_oeste_sc.parquet")
bloco(f"SIM fonte: {len(dfsim)} registros, anos: {sorted(dfsim['ano'].unique())}")

merge_sim = df[['codigo_ibge_6d', 'ano', 'total_obitos']].merge(
    dfsim[['codigo_ibge_6d', 'ano', 'total_obitos']],
    on=['codigo_ibge_6d', 'ano'],
    suffixes=('_painel', '_fonte'),
    how='outer'
)
merge_sim = merge_sim.fillna(0)
diff_sim = merge_sim[merge_sim['total_obitos_painel'] != merge_sim['total_obitos_fonte']]
bloco(f"**Divergências SIM:** {len(diff_sim)}")
if len(diff_sim) > 0:
    issue(f"SIM: {len(diff_sim)} divergências")
    bloco(diff_sim.head(10).to_string())
    correcoes_necessarias = True
else:
    ok("SIM: total_obitos bate com fonte")

# --- 2.5 SINASC ---
subsecao("2.5 SINASC → painel")

dfsinasc = pd.read_parquet("data/processed/datasus_sinasc_oeste_sc.parquet")
bloco(f"SINASC fonte: {len(dfsinasc)} registros, anos: {sorted(dfsinasc['ano'].unique())}")

merge_sinasc = df[['codigo_ibge_6d', 'ano', 'total_nascimentos']].merge(
    dfsinasc[['codigo_ibge_6d', 'ano', 'total_nascimentos']],
    on=['codigo_ibge_6d', 'ano'],
    suffixes=('_painel', '_fonte'),
    how='outer'
)
merge_sinasc = merge_sinasc.fillna(0)
diff_sinasc = merge_sinasc[merge_sinasc['total_nascimentos_painel'] != merge_sinasc['total_nascimentos_fonte']]
bloco(f"**Divergências SINASC:** {len(diff_sinasc)}")
if len(diff_sinasc) > 0:
    issue(f"SINASC: {len(diff_sinasc)} divergências")
    bloco(diff_sinasc.head(10).to_string())
    correcoes_necessarias = True
else:
    ok("SINASC: total_nascimentos bate com fonte")

# Verificar se 2023-2024 estão corretamente tratados
nasc_2023 = df[df['ano']==2023]['total_nascimentos'].unique()
nasc_2024 = df[df['ano']==2024]['total_nascimentos'].unique()
bloco(f"**Nascimentos 2023:** {nasc_2023}, **2024:** {nasc_2024}")
if all(pd.isna(x) for x in nasc_2023) and all(pd.isna(x) for x in nasc_2024):
    ok("SINASC 2023-2024 corretamente como NaN (sem dados)")
elif all(x == 0 for x in nasc_2023 if not pd.isna(x)) and all(pd.isna(x) for x in nasc_2024):
    issue("SINASC 2023 está como 0.0 em vez de NaN (SINASC só tem dados até 2022)")
    correcoes_necessarias = True
else:
    issue(f"SINASC 2023-2024 com valores inesperados: 2023={nasc_2023}, 2024={nasc_2024}")
    correcoes_necessarias = True

# ============================================================
# 3. CÁLCULOS DERIVADOS
# ============================================================
secao("3. CÁLCULOS DERIVADOS")

# taxa_vinculos_por_mil
df['calc_taxa_vinculos'] = (df['total_vinculos_rais'] / df['populacao_total']) * 1000
diff_vinc = df[np.abs(df['taxa_vinculos_por_mil'] - df['calc_taxa_vinculos']) > 0.01]
bloco(f"**taxa_vinculos_por_mil:** {len(diff_vinc)} divergências (>0.01)")
if len(diff_vinc) > 0:
    issue(f"taxa_vinculos_por_mil: {len(diff_vinc)} cálculos incorretos")
    bloco(diff_vinc[['codigo_ibge_7d','ano','total_vinculos_rais','populacao_total','taxa_vinculos_por_mil','calc_taxa_vinculos']].head(5).to_string())
    correcoes_necessarias = True
else:
    ok("taxa_vinculos_por_mil: todos corretos")

# taxa_internacoes_por_mil
df['calc_taxa_internacoes'] = (df['total_internacoes_sih'] / df['populacao_total']) * 1000
diff_int = df[np.abs(df['taxa_internacoes_por_mil'] - df['calc_taxa_internacoes']) > 0.01]
bloco(f"**taxa_internacoes_por_mil:** {len(diff_int)} divergências (>0.01)")
if len(diff_int) > 0:
    issue(f"taxa_internacoes_por_mil: {len(diff_int)} cálculos incorretos")
    bloco(diff_int[['codigo_ibge_7d','ano','total_internacoes_sih','populacao_total','taxa_internacoes_por_mil','calc_taxa_internacoes']].head(5).to_string())
    correcoes_necessarias = True
else:
    ok("taxa_internacoes_por_mil: todos corretos")

# taxa_mortalidade (pode ter NaN)
df_mort = df.dropna(subset=['total_obitos', 'taxa_mortalidade']).copy()
df_mort['calc_taxa_mortalidade'] = (df_mort['total_obitos'] / df_mort['populacao_total']) * 1000
diff_mort = df_mort[np.abs(df_mort['taxa_mortalidade'] - df_mort['calc_taxa_mortalidade']) > 0.01]
bloco(f"**taxa_mortalidade:** {len(diff_mort)} divergências (>0.01) em {len(df_mort)} registros válidos")
if len(diff_mort) > 0:
    issue(f"taxa_mortalidade: {len(diff_mort)} cálculos incorretos")
    bloco(diff_mort[['codigo_ibge_7d','ano','total_obitos','populacao_total','taxa_mortalidade','calc_taxa_mortalidade']].head(5).to_string())
    correcoes_necessarias = True
else:
    ok("taxa_mortalidade: todos corretos")

# taxa_natalidade
df_nasc = df.dropna(subset=['total_nascimentos', 'taxa_natalidade']).copy()
df_nasc['calc_taxa_natalidade'] = (df_nasc['total_nascimentos'] / df_nasc['populacao_total']) * 1000
diff_nasc = df_nasc[np.abs(df_nasc['taxa_natalidade'] - df_nasc['calc_taxa_natalidade']) > 0.01]
bloco(f"**taxa_natalidade:** {len(diff_nasc)} divergências (>0.01) em {len(df_nasc)} registros válidos")
if len(diff_nasc) > 0:
    issue(f"taxa_natalidade: {len(diff_nasc)} cálculos incorretos")
    bloco(diff_nasc[['codigo_ibge_7d','ano','total_nascimentos','populacao_total','taxa_natalidade','calc_taxa_natalidade']].head(5).to_string())
    correcoes_necessarias = True
else:
    ok("taxa_natalidade: todos corretos")

# ============================================================
# 4. ANOMALIAS
# ============================================================
secao("4. ANOMALIAS")

anom_vinc = df[df['taxa_vinculos_por_mil'] > 500]
bloco(f"**Municípios com taxa_vinculos_por_mil > 500:** {len(anom_vinc)}")
if len(anom_vinc) > 0:
    bloco(anom_vinc[['municipio','ano','total_vinculos_rais','populacao_total','taxa_vinculos_por_mil']].to_string())
    aviso(f"{len(anom_vinc)} registros com taxa_vinculos_por_mil > 500")

anom_int = df[df['taxa_internacoes_por_mil'] > 50]
bloco(f"**Municípios com taxa_internacoes_por_mil > 50:** {len(anom_int)}")
if len(anom_int) > 0:
    bloco(anom_int[['municipio','ano','total_internacoes_sih','populacao_total','taxa_internacoes_por_mil']].to_string())
    aviso(f"{len(anom_int)} registros com taxa_internacoes_por_mil > 50")

anom_pop = df[df['populacao_total'] == 0]
bloco(f"**Municípios com populacao_total = 0:** {len(anom_pop)}")
if len(anom_pop) > 0:
    issue(f"{len(anom_pop)} registros com populacao_total = 0")
    bloco(anom_pop[['municipio','ano']].to_string())
    correcoes_necessarias = True
else:
    ok("Nenhum município com população = 0")

negativos = {}
for col in df.select_dtypes(include=[np.number]).columns:
    neg = df[df[col] < 0]
    if len(neg) > 0:
        negativos[col] = len(neg)
bloco(f"**Valores negativos:** {negativos}")
if negativos:
    issue(f"Valores negativos encontrados: {negativos}")
    correcoes_necessarias = True
else:
    ok("Nenhum valor negativo")

# ============================================================
# 5. COMPARABILIDADE TEMPORAL
# ============================================================
secao("5. COMPARABILIDADE TEMPORAL")

pop_pivot = df.pivot(index=['codigo_ibge_7d', 'municipio'], columns='ano', values='populacao_total').reset_index()
pop_pivot['var_2021_2022_pct'] = ((pop_pivot[2022] - pop_pivot[2021]) / pop_pivot[2021]) * 100

saltos = pop_pivot[pop_pivot['var_2021_2022_pct'] > 50].sort_values('var_2021_2022_pct', ascending=False)
bloco(f"**Municípios com população +50% 2021→2022:** {len(saltos)}")
if len(saltos) > 0:
    bloco(saltos[['codigo_ibge_7d','municipio',2021,2022,'var_2021_2022_pct']].to_string())
    aviso(f"{len(saltos)} municípios com salto populacional >50% 2021→2022 (efeito Censo 2022)")

dobrou = pop_pivot[pop_pivot[2022] / pop_pivot[2021] > 2]
bloco(f"**Municípios onde população dobrou 2021→2022:** {len(dobrou)}")
if len(dobrou) > 0:
    bloco(dobrou[['codigo_ibge_7d','municipio',2021,2022,'var_2021_2022_pct']].to_string())
    aviso(f"{len(dobrou)} municípios com população que dobrou de 2021 para 2022")

mais_que_dobrou = pop_pivot.nlargest(10, 'var_2021_2022_pct')[['codigo_ibge_7d','municipio',2021,2022,'var_2021_2022_pct']]
bloco(f"**Top 10 maiores variações 2021→2022:**\n{mais_que_dobrou.to_string()}")

aviso("Municípios com grande salto populacional terão taxas artificialmente reduzidas em 2022. Recomenda-se cautela na interpretação de taxas para esses municípios no ano de 2022.")

# ============================================================
# 6. CORREÇÕES E RECOMENDAÇÕES
# ============================================================
secao("6. CORREÇÕES E RECOMENDAÇÕES")

if correcoes_necessarias:
    bloco("**Correções necessárias detectadas.**")

    # Verificar especificamente o problema do SINASC 2023
    if nans_nasc_2023 == 0:
        bloco("""
### Correção 1: SINASC 2023 → NaN

O painel possui `total_nascimentos=0.0` para todos os 109 municípios em 2023. 
No entanto, a fonte SINASC só possui dados até 2022 (545 registros = 109 × 5 anos).

**Ação:** Substituir `total_nascimentos` e `taxa_natalidade` de 2023 de 0.0 para NaN.
""")

    bloco("""
### Lista completa de problemas
""")
    for i, issue_text in enumerate(issues, 1):
        bloco(f"{i}. {issue_text}")
else:
    ok("Nenhuma correção necessária no painel.")

# ============================================================
# RESUMO EXECUTIVO
# ============================================================
resumo = f"""## Resumo Executivo

- **Painel:** {n_linhas} linhas, {municipios_unicos} municípios, anos {anos[0]}-{anos[-1]}
- **Problemas encontrados:** {len(issues)}
- **Correções necessárias:** {'SIM' if correcoes_necessarias else 'NÃO'}

### Lista de Problemas
"""
for i, issue_text in enumerate(issues, 1):
    resumo += f"{i}. {issue_text}\n"

if not issues:
    resumo += "Nenhum problema crítico encontrado.\n"

relatorio.insert(0, resumo)

# ============================================================
# SALVAR RELATÓRIO
# ============================================================
with open(OUTPUT_REPORT, 'w') as f:
    f.write("\n".join(relatorio))

print(f"Relatório salvo em {OUTPUT_REPORT}")
print(f"Problemas encontrados: {len(issues)}")
print(f"Correções necessárias: {correcoes_necessarias}")
