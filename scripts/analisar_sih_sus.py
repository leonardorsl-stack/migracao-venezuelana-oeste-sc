#!/usr/bin/env python3
"""Análise do SIH/SUS - Internações hospitalares de venezuelanos em SC (2018-2025)."""

import json
import sys
from pathlib import Path

import pandas as pd

DATA_DIR = Path("/Users/leonardosantos/Documents/raio_x_migraçao/data/raw/datasus")
OUTPUT_DIR = Path("/Users/leonardosantos/Documents/raio_x_migraçao/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Importa a lista oficial de 109 municípios da Região Intermediária de Chapecó
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from config import SETTINGS

REGIAO_OESTE_SC = SETTINGS.REGIAO_OESTE_SC
# Códigos de 6 dígitos para compatibilidade com MUNIC_RES do SIH
REGIAO_OESTE_SC_6D = [int(str(c)[:6]) for c in REGIAO_OESTE_SC]

def carregar_dados():
    df = pd.read_parquet(DATA_DIR / "sih_sus_sc_venezuela_2018_2025.parquet")
    # Converter tipos
    df['ano'] = df['ano'].astype(int)
    df['mes'] = df['mes'].astype(int)
    df['MUNIC_RES'] = df['MUNIC_RES'].astype(str).str.strip()
    df['MUNIC_MOV'] = df['MUNIC_MOV'].astype(str).str.strip()
    df['DIAG_PRINC'] = df['DIAG_PRINC'].astype(str).str.strip().str.upper()
    df['DIAG_SECUN'] = df['DIAG_SECUN'].astype(str).str.strip().str.upper()
    df['CAR_INT'] = df['CAR_INT'].astype(str).str.strip()
    df['SEXO'] = df['SEXO'].astype(str).str.strip()
    df['IDADE'] = pd.to_numeric(df['IDADE'], errors='coerce')
    df['COD_IDADE'] = df['COD_IDADE'].astype(str).str.strip()
    df['DIAS_PERM'] = pd.to_numeric(df['DIAS_PERM'], errors='coerce')
    df['MORTE'] = pd.to_numeric(df['MORTE'], errors='coerce')
    df['VAL_TOT'] = pd.to_numeric(df['VAL_TOT'], errors='coerce')
    df['CBOR'] = df['CBOR'].astype(str).str.strip()
    df['CNAER'] = df['CNAER'].astype(str).str.strip()

    # Calcular idade em anos
    def calc_idade_anos(row):
        cod = str(row['COD_IDADE'])
        idade = row['IDADE']
        if pd.isna(idade):
            return None
        idade = int(idade)
        if cod == '2' or cod == '3':  # dias
            return 0
        elif cod == '4':  # anos
            return idade
        elif cod == '5':  # >100 anos
            return 100
        return None

    df['idade_anos'] = df.apply(calc_idade_anos, axis=1)

    # Flag Oeste SC
    df['municipio_res_num'] = pd.to_numeric(df['MUNIC_RES'], errors='coerce')
    df['municipio_mov_num'] = pd.to_numeric(df['MUNIC_MOV'], errors='coerce')
    df['oeste_sc_res'] = df['municipio_res_num'].isin(REGIAO_OESTE_SC_6D)
    df['oeste_sc_mov'] = df['municipio_mov_num'].isin(REGIAO_OESTE_SC_6D)

    return df


def analisar_evolucao_temporal(df):
    print("\n" + "="*60)
    print("1. EVOLUÇÃO TEMPORAL")
    print("="*60)

    ev_ano = df.groupby('ano').size().reset_index(name='internacoes')
    print("\nPor ano:")
    for _, row in ev_ano.iterrows():
        print(f"  {int(row['ano'])}: {row['internacoes']} internações")

    # Taxa de crescimento ano a ano
    print("\nTaxa de crescimento:")
    for i in range(1, len(ev_ano)):
        ano_atual = int(ev_ano.iloc[i]['ano'])
        ano_ant = int(ev_ano.iloc[i-1]['ano'])
        val_atual = ev_ano.iloc[i]['internacoes']
        val_ant = ev_ano.iloc[i-1]['internacoes']
        if val_ant > 0:
            cresc = ((val_atual - val_ant) / val_ant) * 100
            print(f"  {ano_ant} → {ano_atual}: +{cresc:.1f}%")

    return ev_ano


def analisar_cids(df):
    print("\n" + "="*60)
    print("2. TOP CIDs (DIAGNÓSTICOS PRINCIPAIS)")
    print("="*60)

    # Agrupar por capítulo CID-10 (primeiros 3 caracteres = categoria)
    df['cid_categoria'] = df['DIAG_PRINC'].str[:3]

    top_cids = df['DIAG_PRINC'].value_counts().head(20)
    print("\nTop 20 CIDs (4 dígitos):")
    for cid, cnt in top_cids.items():
        pct = (cnt / len(df)) * 100
        print(f"  {cid}: {cnt} ({pct:.1f}%)")

    # Capítulos (aproximação pelas letras)
    def cap_cid(cid):
        if not cid or len(cid) < 1:
            return 'Ignorado'
        c = cid[0]
        caps = {
            'A': 'A00-B99: Infecções/parasitoses',
            'B': 'A00-B99: Infecções/parasitoses',
            'C': 'C00-D48: Neoplasias',
            'D': 'C00-D48: Neoplasias / D50-D89: Sangue',
            'E': 'E00-E90: Endócrinas/metabólicas',
            'F': 'F00-F99: Transtornos mentais',
            'G': 'G00-G99: Sistema nervoso',
            'H': 'H00-H59: Olho / H60-H95: Ouvido',
            'I': 'I00-I99: Circulatório',
            'J': 'J00-J99: Respiratório',
            'K': 'K00-K93: Digestivo',
            'L': 'L00-L99: Pele',
            'M': 'M00-M99: Osteomuscular',
            'N': 'N00-N99: Geniturinário',
            'O': 'O00-O99: Gravidez/parto',
            'P': 'P00-P96: Perinatal',
            'Q': 'Q00-Q99: Malformações congênitas',
            'R': 'R00-R99: Sintomas/signais',
            'S': 'S00-T98: Trauma/envenenamento',
            'T': 'S00-T98: Trauma/envenenamento',
            'V': 'V01-Y98: Causas externas',
            'W': 'V01-Y98: Causas externas',
            'X': 'V01-Y98: Causas externas',
            'Y': 'V01-Y98: Causas externas',
            'Z': 'Z00-Z99: Fatores saúde/serviços',
        }
        return caps.get(c, 'Outros')

    df['capitulo_cid'] = df['DIAG_PRINC'].apply(cap_cid)
    caps = df['capitulo_cid'].value_counts().head(15)
    print("\nPor capítulo CID-10:")
    for cap, cnt in caps.items():
        pct = (cnt / len(df)) * 100
        print(f"  {cap}: {cnt} ({pct:.1f}%)")

    return top_cids


def analisar_municipios(df):
    print("\n" + "="*60)
    print("3. DISTRIBUIÇÃO POR MUNICÍPIO")
    print("="*60)

    # Município de residência
    mun_res = df['MUNIC_RES'].value_counts().head(15)
    print("\nTop 15 municípios de RESIDÊNCIA:")
    for mun, cnt in mun_res.items():
        pct = (cnt / len(df)) * 100
        flag = " [OESTE]" if int(mun) in REGIAO_OESTE_SC else ""
        print(f"  {mun}: {cnt} ({pct:.1f}%){flag}")

    # Município do hospital
    mun_mov = df['MUNIC_MOV'].value_counts().head(15)
    print("\nTop 15 municípios do HOSPITAL:")
    for mun, cnt in mun_mov.items():
        pct = (cnt / len(df)) * 100
        flag = " [OESTE]" if int(mun) in REGIAO_OESTE_SC else ""
        print(f"  {mun}: {cnt} ({pct:.1f}%){flag}")

    # Resumo Oeste SC
    res_oeste = df['oeste_sc_res'].sum()
    mov_oeste = df['oeste_sc_mov'].sum()
    print("\nResumo Oeste SC:")
    print(f"  Residem no Oeste: {res_oeste} ({res_oeste/len(df)*100:.1f}%)")
    print(f"  Internados no Oeste: {mov_oeste} ({mov_oeste/len(df)*100:.1f}%)")


def analisar_acidentes_trabalho(df):
    print("\n" + "="*60)
    print("4. ACIDENTES DE TRABALHO E CARÁTER DA INTERNAÇÃO")
    print("="*60)

    car_map = {
        '01': 'Eletivo',
        '02': 'Urgência',
        '03': 'Acidente trabalho (local)',
        '04': 'Acidente trajeto',
        '05': 'Acidente trânsito',
        '06': 'Outras lesões/envenenamentos'
    }

    car_counts = df['CAR_INT'].value_counts()
    print("\nCaráter da internação:")
    for car, cnt in car_counts.items():
        pct = (cnt / len(df)) * 100
        desc = car_map.get(car, 'Desconhecido')
        print(f"  {car} - {desc}: {cnt} ({pct:.1f}%)")

    # Acidentes de trabalho (cód. 3 e 4)
    acidentes = df[df['CAR_INT'].isin(['3', '4'])]
    print(f"\nAcidentes de trabalho + trajeto: {len(acidentes)} ({len(acidentes)/len(df)*100:.1f}%)")

    if len(acidentes) > 0:
        print("\nCIDs principais em acidentes de trabalho:")
        cids_acid = acidentes['DIAG_PRINC'].value_counts().head(10)
        for cid, cnt in cids_acid.items():
            print(f"  {cid}: {cnt}")

        print("\nEvolução anual de acidentes:")
        ev_acid = acidentes.groupby('ano').size()
        for ano, cnt in ev_acid.items():
            print(f"  {ano}: {cnt}")

    return acidentes


def analisar_demografia(df):
    print("\n" + "="*60)
    print("5. PERFIL DEMOGRÁFICO")
    print("="*60)

    # Sexo
    sexo_map = {'1': 'Masculino', '2': 'Feminino', '3': 'Feminino'}
    df['sexo_desc'] = df['SEXO'].map(sexo_map).fillna('Ignorado')
    sexo_counts = df['sexo_desc'].value_counts()
    print("\nSexo:")
    for sexo, cnt in sexo_counts.items():
        print(f"  {sexo}: {cnt} ({cnt/len(df)*100:.1f}%)")

    # Idade
    idade_valida = df['idade_anos'].dropna()
    print("\nIdade (anos):")
    print(f"  Média: {idade_valida.mean():.1f}")
    print(f"  Mediana: {idade_valida.median():.1f}")
    print(f"  Min: {idade_valida.min():.0f}")
    print(f"  Max: {idade_valida.max():.0f}")

    # Faixas etárias
    bins = [0, 18, 30, 40, 50, 60, 100]
    labels = ['0-17', '18-29', '30-39', '40-49', '50-59', '60+']
    df['faixa_etaria'] = pd.cut(df['idade_anos'], bins=bins, labels=labels, right=False)
    fx_counts = df['faixa_etaria'].value_counts().sort_index()
    print("\nFaixa etária:")
    for fx, cnt in fx_counts.items():
        print(f"  {fx}: {cnt} ({cnt/len(df)*100:.1f}%)")


def analisar_permanencia(df):
    print("\n" + "="*60)
    print("6. PERMANÊNCIA E ÓBITOS")
    print("="*60)

    dias = df['DIAS_PERM'].dropna()
    print("\nDias de permanência:")
    print(f"  Média: {dias.mean():.1f}")
    print(f"  Mediana: {dias.median():.1f}")
    print(f"  Max: {dias.max():.0f}")

    # Óbitos
    obitos = df['MORTE'].sum()
    print(f"\nÓbitos: {int(obitos)} ({obitos/len(df)*100:.2f}%)")

    if obitos > 0:
        obitos_ano = df[df['MORTE'] == 1].groupby('ano').size()
        print("\nÓbitos por ano:")
        for ano, cnt in obitos_ano.items():
            print(f"  {ano}: {cnt}")

    # UTI
    uti_cols = ['UTI_MES_IN', 'UTI_MES_AN', 'UTI_MES_AL', 'UTI_MES_TO']
    for col in uti_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df['uti_total'] = df[uti_cols].sum(axis=1)
    uti_count = (df['uti_total'] > 0).sum()
    print(f"\nInternações com UTI: {uti_count} ({uti_count/len(df)*100:.1f}%)")


def analisar_valores(df):
    print("\n" + "="*60)
    print("7. VALORES DAS INTERNAÇÕES")
    print("="*60)

    val = df['VAL_TOT'].dropna()
    print("\nValor total (R$):")
    print(f"  Soma: R$ {val.sum():,.2f}")
    print(f"  Média: R$ {val.mean():,.2f}")
    print(f"  Mediana: R$ {val.median():,.2f}")

    # Por ano
    print("\nValor total por ano:")
    val_ano = df.groupby('ano')['VAL_TOT'].sum()
    for ano, v in val_ano.items():
        print(f"  {ano}: R$ {v:,.2f}")


def analisar_cbo_cnae(df):
    print("\n" + "="*60)
    print("8. OCUPAÇÃO (CBO) E ATIVIDADE ECONÔMICA (CNAE)")
    print("="*60)

    # CBO
    cbo_validos = df[df['CBOR'].str.len() >= 3]['CBOR'].value_counts().head(15)
    if len(cbo_validos) > 0:
        print("\nTop CBOs:")
        for cbo, cnt in cbo_validos.items():
            print(f"  {cbo}: {cnt}")
    else:
        print("\nCBO: poucos registros preenchidos")

    # CNAE
    cnae_validos = df[df['CNAER'].str.len() >= 2]['CNAER'].value_counts().head(10)
    if len(cnae_validos) > 0:
        print("\nTop CNAEs:")
        for cnae, cnt in cnae_validos.items():
            print(f"  {cnae}: {cnt}")
    else:
        print("\nCNAE: poucos registros preenchidos")


def analisar_procedimentos(df):
    print("\n" + "="*60)
    print("9. PROCEDIMENTOS REALIZADOS")
    print("="*60)

    proc = df['PROC_REA'].value_counts().head(15)
    print("\nTop procedimentos:")
    for p, cnt in proc.items():
        print(f"  {p}: {cnt}")


def gerar_resumo_json(df):
    """Gera um resumo estruturado em JSON."""

    # Óbitos por ano
    obitos_ano = df[df['MORTE'] == 1].groupby('ano').size().to_dict()

    # Internações por ano
    intern_ano = df.groupby('ano').size().to_dict()

    # Top 10 CIDs
    top_cids = df['DIAG_PRINC'].value_counts().head(10).to_dict()

    # Top 10 municípios residência
    top_mun = df['MUNIC_RES'].value_counts().head(10).to_dict()

    # Sexo
    sexo_counts = df['sexo_desc'].value_counts().to_dict() if 'sexo_desc' in df.columns else {}

    # Acidentes trabalho
    acidentes = df[df['CAR_INT'].isin(['3', '4'])]

    # Valor total
    val_total = float(df['VAL_TOT'].sum())

    resumo = {
        'total_registros': len(df),
        'periodo': '2018-2025',
        'internacoes_por_ano': {str(k): int(v) for k, v in intern_ano.items()},
        'obitos_por_ano': {str(k): int(v) for k, v in obitos_ano.items()},
        'top_10_cids': top_cids,
        'top_10_municipios_residencia': top_mun,
        'sexo': sexo_counts,
        'acidentes_trabalho': {
            'total': len(acidentes),
            'por_ano': {str(k): int(v) for k, v in acidentes.groupby('ano').size().to_dict().items()}
        },
        'valor_total_rs': val_total,
        'dias_permanencia_media': float(df['DIAS_PERM'].mean()),
        'uti_percentual': float((df['uti_total'] > 0).sum() / len(df) * 100) if 'uti_total' in df.columns else 0,
        'oeste_sc_residencia_percentual': float(df['oeste_sc_res'].sum() / len(df) * 100),
        'oeste_sc_hospital_percentual': float(df['oeste_sc_mov'].sum() / len(df) * 100),
    }

    out = OUTPUT_DIR / 'resumo_sih_sus_venezuela_sc_2018_2025.json'
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(resumo, f, ensure_ascii=False, indent=2)

    print(f"\n📄 Resumo JSON salvo: {out}")
    return resumo


def main():
    print("="*60)
    print("ANÁLISE SIH/SUS - VENEZUELANOS EM SC (2018-2025)")
    print("="*60)

    df = carregar_dados()
    print(f"\nTotal de registros: {len(df)}")

    ev = analisar_evolucao_temporal(df)
    cids = analisar_cids(df)
    analisar_municipios(df)
    analisar_acidentes_trabalho(df)
    analisar_demografia(df)
    analisar_permanencia(df)
    analisar_valores(df)
    analisar_cbo_cnae(df)
    analisar_procedimentos(df)

    resumo = gerar_resumo_json(df)

    print("\n" + "="*60)
    print("✅ ANÁLISE CONCLUÍDA")
    print("="*60)


if __name__ == "__main__":
    main()
