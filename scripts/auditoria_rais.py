import json
import os

import pandas as pd

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================
DATA_DIR = "data/processed"
EXPECTED_RECORDS = {
    2018: 812,
    2019: 3492,
    2020: 9172,
    2021: 21728,
    2022: 39534,
    2023: 61760,
    2024: 90447,
}
YEARS = list(EXPECTED_RECORDS.keys())

REPORT = {
    "resumo_executivo": {},
    "detalhamento": {},
    "problemas": [],
    "recomendacoes": [],
}

def add_problema(severidade, categoria, descricao):
    REPORT["problemas"].append({
        "severidade": severidade,
        "categoria": categoria,
        "descricao": descricao,
    })

def add_recomendacao(descricao):
    REPORT["recomendacoes"].append(descricao)

def get_col(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None

# ============================================================================
# 1. CARREGAMENTO E INTEGRIDADE DOS DADOS BRUTOS
# ============================================================================
print("=" * 60)
print("1. INTEGRIDADE DOS DADOS BRUTOS")
print("=" * 60)

annual_dfs = {}
for year in YEARS:
    filepath = os.path.join(DATA_DIR, f"rais_vinculos_sc_venezuela_{year}.parquet")
    print(f"\n--- Ano {year} ---")
    df = pd.read_parquet(filepath)
    annual_dfs[year] = df
    n_rows = len(df)
    expected = EXPECTED_RECORDS[year]
    status = "PASSOU" if n_rows == expected else "FALHOU"
    print(f"Registros: {n_rows} (esperado: {expected}) -> {status}")
    if n_rows != expected:
        add_problema("ALTA", "Integridade", f"Ano {year}: {n_rows} registros, esperado {expected}")

    print(f"Colunas ({len(df.columns)}): {list(df.columns)}")
    print(f"Tipos:\n{df.dtypes}")

    nulos = df.isnull().sum()
    nulos_rel = (nulos / n_rows * 100).round(2)
    cols_com_nulos = nulos[nulos > 0]
    if len(cols_com_nulos) > 0:
        print(f"Colunas com nulos:\n{pd.concat([cols_com_nulos, nulos_rel[nulos > 0]], axis=1)}")
        for col in cols_com_nulos.index:
            add_problema("MÉDIA", "Nulos", f"Ano {year}: coluna '{col}' tem {cols_com_nulos[col]} nulos ({nulos_rel[col]}%)")
    else:
        print("Sem valores nulos.")

print("\n")

# ============================================================================
# 2. FILTRO DE NACIONALIDADE
# ============================================================================
print("=" * 60)
print("2. FILTRO DE NACIONALIDADE")
print("=" * 60)

for year in YEARS:
    df = annual_dfs[year]
    col_nac = get_col(df, ['nacionalidade', 'NACIONAL', 'Nacionalidade', 'NACIONALIDADE'])
    if col_nac is None:
        print(f"Ano {year}: coluna de nacionalidade não encontrada! Colunas: {list(df.columns)}")
        add_problema("CRÍTICA", "Nacionalidade", f"Ano {year}: coluna de nacionalidade não encontrada")
        continue

    nac_counts = df[col_nac].value_counts().to_dict()
    print(f"Ano {year} ({col_nac}): {nac_counts}")

    # Verificar se todos são Venezuela/092
    outros = {k: v for k, v in nac_counts.items() if str(k) not in ['092', 'Venezuela', 'VENEZUELA', 'venezuela']}
    if outros:
        add_problema("ALTA", "Nacionalidade", f"Ano {year}: encontrados outros valores além de Venezuela/092: {outros}")

print("\n")

# ============================================================================
# 3. AGREGAÇÃO POR MUNICÍPIO vs PAINEL
# ============================================================================
print("=" * 60)
print("3. AGREGAÇÃO POR MUNICÍPIO")
print("=" * 60)

raw_agg = {}
for year in YEARS:
    df = annual_dfs[year]
    col_mun = get_col(df, ['municipio', 'MUNICIPIO', 'MUNICÍPIO', 'codigo_municipio', 'CODIGO_MUNICIPIO', 'MUNICIPIO_EMP'])
    if col_mun is None:
        print(f"Ano {year}: colunas disponíveis: {list(df.columns)}")
        add_problema("ALTA", "Município", f"Ano {year}: não encontrou coluna de município")
        continue

    agg = df.groupby(col_mun).size().reset_index(name=f'vinculos_{year}')
    raw_agg[year] = agg
    print(f"Ano {year}: {len(agg)} municípios distintos na RAIS bruta")

# Carregar painel
painel_path = os.path.join(DATA_DIR, "painel_oeste_sc_2018_2024.parquet")
painel = pd.read_parquet(painel_path)
print(f"\nPainel: {len(painel)} municípios, colunas: {list(painel.columns)}")

for year in YEARS:
    col_vinc = f'vinculos_{year}'
    if col_vinc not in painel.columns:
        add_problema("ALTA", "Painel", f"Coluna {col_vinc} não encontrada no painel")
        continue

    painel_sum = painel[col_vinc].sum()
    if year in raw_agg:
        raw_sum = raw_agg[year].iloc[:, 1].sum()
    else:
        raw_sum = 0

    diff = painel_sum - raw_sum
    status = "PASSOU" if diff == 0 else "FALHOU"
    print(f"Ano {year}: painel={painel_sum}, bruto={raw_sum}, diff={diff} -> {status}")
    if diff != 0:
        add_problema("ALTA", "Agregação", f"Ano {year}: diferença de {diff} vínculos entre painel ({painel_sum}) e bruto ({raw_sum})")

print("\n")

# ============================================================================
# 4. CÁLCULO DAS TAXAS
# ============================================================================
print("=" * 60)
print("4. CÁLCULO DAS TAXAS")
print("=" * 60)

for year in YEARS:
    col_vinc = f'vinculos_{year}'
    col_taxa = f'taxa_vinculos_por_mil_{year}'
    col_pop = f'populacao_{year}'

    if col_vinc not in painel.columns or col_taxa not in painel.columns:
        print(f"Ano {year}: colunas necessárias não encontradas no painel")
        continue

    if col_pop in painel.columns:
        calculada = (painel[col_vinc] / painel[col_pop] * 1000).round(6)
        diff = (calculada - painel[col_taxa]).abs()
        max_diff = diff.max()
        status = "PASSOU" if max_diff < 0.01 else "FALHOU"
        print(f"Ano {year}: diferença máxima na taxa = {max_diff:.6f} -> {status}")
        if max_diff >= 0.01:
            add_problema("ALTA", "Taxas", f"Ano {year}: taxa calculada diverge em até {max_diff}")
    else:
        print(f"Ano {year}: coluna de população não encontrada, não é possível verificar cálculo")
        add_problema("MÉDIA", "Taxas", f"Ano {year}: coluna {col_pop} não encontrada no painel")

    taxas_altas = painel[col_taxa][painel[col_taxa] > 500]
    if len(taxas_altas) > 0:
        add_problema("MÉDIA", "Taxas", f"Ano {year}: {len(taxas_altas)} municípios com taxa > 500")
        print(f"Ano {year}: {len(taxas_altas)} municípios com taxa > 500")

    negativas = painel[col_taxa][painel[col_taxa] < 0]
    if len(negativas) > 0:
        add_problema("ALTA", "Taxas", f"Ano {year}: {len(negativas)} municípios com taxa negativa")

print("\n")

# ============================================================================
# 5. PERFIL ETÁRIO E DE GÊNERO
# ============================================================================
print("=" * 60)
print("5. PERFIL ETÁRIO E DE GÊNERO")
print("=" * 60)

for year in YEARS:
    df = annual_dfs[year]

    # Sexo
    col_sexo = get_col(df, ['sexo', 'SEXO', 'Sexo'])
    if col_sexo:
        sexo_counts = df[col_sexo].value_counts().to_dict()
        print(f"Ano {year} - Sexo ({col_sexo}): {sexo_counts}")
        # RAIS geralmente usa 1=Masc, 2=Fem
        valores_esperados = {'1', '2', 'M', 'F', 'MASCULINO', 'FEMININO'}
        valores_invalidos = [str(v) for v in df[col_sexo].unique() if str(v).upper() not in valores_esperados]
        if valores_invalidos:
            add_problema("MÉDIA", "Sexo", f"Ano {year}: valores inesperados em sexo: {valores_invalidos}")
    else:
        add_problema("BAIXA", "Sexo", f"Ano {year}: coluna de sexo não encontrada")
        print(f"Ano {year}: coluna de sexo não encontrada.")

    # Idade
    col_idade = get_col(df, ['idade', 'IDADE', 'Idade', 'IDADE_1'])
    if col_idade:
        # Converter para numérico se necessário
        idade_num = pd.to_numeric(df[col_idade], errors='coerce')
        idade_min = idade_num.min()
        idade_max = idade_num.max()
        print(f"Ano {year} - Idade ({col_idade}): min={idade_min}, max={idade_max}")
        if idade_min < 14:
            n = (idade_num < 14).sum()
            add_problema("MÉDIA", "Idade", f"Ano {year}: {n} registros com idade < 14 (min={idade_min})")
        if idade_max > 100:
            n = (idade_num > 100).sum()
            add_problema("MÉDIA", "Idade", f"Ano {year}: {n} registros com idade > 100 (max={idade_max})")

        bins = [0, 17, 24, 39, 54, 64, 100, 200]
        labels = ['<18', '18-24', '25-39', '40-54', '55-64', '65-100', '>100']
        faixas = pd.cut(idade_num, bins=bins, labels=labels, right=True)
        print(f"Ano {year} - Faixas etárias:\n{faixas.value_counts().sort_index()}")
    else:
        add_problema("BAIXA", "Idade", f"Ano {year}: coluna de idade não encontrada")
        print(f"Ano {year}: coluna de idade não encontrada")

print("\n")

# ============================================================================
# 6. CONSISTÊNCIA TEMPORAL
# ============================================================================
print("=" * 60)
print("6. CONSISTÊNCIA TEMPORAL")
print("=" * 60)

vinculos_ano = {year: len(annual_dfs[year]) for year in YEARS}
for i in range(1, len(YEARS)):
    y_ant = YEARS[i-1]
    y_atual = YEARS[i]
    cresc = (vinculos_ano[y_atual] - vinculos_ano[y_ant]) / vinculos_ano[y_ant] * 100
    print(f"{y_ant} -> {y_atual}: {vinculos_ano[y_ant]} -> {vinculos_ano[y_atual]} ({cresc:+.1f}%)")
    if cresc < -50:
        add_problema("ALTA", "Temporal", f"Queda abrupta de {cresc:.1f}% de {y_ant} para {y_atual}")

# Duplicados entre anos - verificar se há identificador
print("\nVerificação de duplicados entre anos (usando combinação de colunas)...")
# Como não temos CPF, usaremos uma combinação de atributos para verificar duplicidade óbvia
for year in YEARS:
    df = annual_dfs[year]
    # Listar colunas disponíveis
    print(f"Ano {year} colunas: {list(df.columns)}")

# Verificar se há registros idênticos em todos os campos entre anos consecutivos
for i in range(1, len(YEARS)):
    y1 = YEARS[i-1]
    y2 = YEARS[i]
    df1 = annual_dfs[y1]
    df2 = annual_dfs[y2]

    # Usar apenas colunas comuns
    cols_comuns = list(set(df1.columns) & set(df2.columns))
    # Excluir ano se existir
    cols_comuns = [c for c in cols_comuns if c != 'ano']

    merged = pd.merge(df1[cols_comuns], df2[cols_comuns], on=cols_comuns, how='inner')
    n_dup = len(merged)
    if n_dup > 0:
        print(f"{y1} <-> {y2}: {n_dup} registros idênticos em todas as colunas comuns")
        add_problema("BAIXA", "Duplicados", f"Entre {y1} e {y2}: {n_dup} registros idênticos em colunas comuns ({cols_comuns})")
    else:
        print(f"{y1} <-> {y2}: 0 registros idênticos em todas as colunas comuns")

print("\n")

# ============================================================================
# SALVAR RELATÓRIO JSON
# ============================================================================
with open("auditoria_report.json", "w", encoding="utf-8") as f:
    json.dump(REPORT, f, ensure_ascii=False, indent=2)

print("Auditoria concluída. Relatório salvo em auditoria_report.json")
