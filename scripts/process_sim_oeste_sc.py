"""
Processamento dos microdados do SIM (óbitos) do DataSUS para a Região Oeste de SC.

Gera dois arquivos Parquet:
- data/processed/datasus_sim_oeste_sc.parquet: agregação por município/ano com sexo, faixa etária e capítulo CID-10.
- data/processed/datasus_sim_causas_trabalho_oeste.parquet: subconjunto de óbitos por causas externas/acidentes de trabalho.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Adiciona src ao path para importar config
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.append(str(PROJECT_ROOT / "src"))

from config import SETTINGS

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

MUNICIPIOS_OESTE_7D = SETTINGS.REGIAO_OESTE_SC
MUNICIPIOS_OESTE_6D = [str(c)[:6] for c in MUNICIPIOS_OESTE_7D]

MUNICIPIO_NOME = {
    "420420": "Chapecó",
    "420430": "Concórdia",
    "421680": "Seara",
    "421720": "São Miguel do Oeste",
    "420768": "Itapiranga",
    "420665": "Guatambú",
    "421950": "Xanxerê",
    "420900": "Joaçaba",
    "420670": "Herval d'Oeste",
    "421970": "Xaxim",
    "420380": "Cunha Porã",
    "420400": "Cunhataí",
    "420640": "Guaraciaba",
    "420890": "Jupiá",
    "421610": "Riqueza",
    "421935": "Vargeão",
    "420127": "Águas de Chapecó",
    "420415": "Bom Jesus do Oeste",
    "420440": "Coronel Freitas",
    "420543": "Caxambu do Sul",
}

ANOS = list(range(2018, 2024))

RAW_DIR = SETTINGS.DATA_RAW / "datasus" / "SIM"
PROCESSED_DIR = SETTINGS.DATA_PROCESSED


# ---------------------------------------------------------------------------
# Funções auxiliares
# ---------------------------------------------------------------------------

def decodifica_idade(idade: pd.Series) -> pd.Series:
    """Converte campo IDADE do SIM para faixa etária simplificada.

    Formato SIM:
        1º dígito = unidade (0=min, 1=h, 2=dias, 3=meses, 4=anos, 5=100+ anos, 9=ignorado)
        demais    = quantidade
    """
    s = idade.astype(str).str.strip()
    s = s.where(s.str.len() == 3, "999")

    unidade = s.str[0].astype(int)
    valor = s.str[1:3].astype(int)

    condicoes = [
        (unidade == 9) | (s == "999"),                           # ignorado
        (unidade < 4) & (valor < 1),                             # < 1 dia (neonatal precoce)
        (unidade == 2) & (valor >= 1) & (valor < 28),            # 1-27 dias
        (unidade == 3) & (valor >= 1) & (valor < 12),            # 1-11 meses
        (unidade == 4) & (valor < 1),                            # < 1 ano
        (unidade == 4) & (valor >= 1) & (valor < 5),             # 1-4 anos
        (unidade == 4) & (valor >= 5) & (valor < 10),            # 5-9 anos
        (unidade == 4) & (valor >= 10) & (valor < 20),           # 10-19 anos
        (unidade == 4) & (valor >= 20) & (valor < 30),           # 20-29 anos
        (unidade == 4) & (valor >= 30) & (valor < 40),           # 30-39 anos
        (unidade == 4) & (valor >= 40) & (valor < 50),           # 40-49 anos
        (unidade == 4) & (valor >= 50) & (valor < 60),           # 50-59 anos
        (unidade == 4) & (valor >= 60) & (valor < 70),           # 60-69 anos
        (unidade == 4) & (valor >= 70) & (valor < 80),           # 70-79 anos
        (unidade == 4) & (valor >= 80) & (valor < 90),           # 80-89 anos
        (unidade == 4) & (valor >= 90),                          # 90+ anos
        (unidade == 5),                                          # 100+ anos
    ]
    escolhas = [
        "Ignorado",
        "< 1 dia",
        "1-27 dias",
        "1-11 meses",
        "< 1 ano",
        "1-4 anos",
        "5-9 anos",
        "10-19 anos",
        "20-29 anos",
        "30-39 anos",
        "40-49 anos",
        "50-59 anos",
        "60-69 anos",
        "70-79 anos",
        "80-89 anos",
        "90+ anos",
        "90+ anos",
    ]
    return pd.Series(np.select(condicoes, escolhas, default="Ignorado"), index=idade.index)


def cap_cid10(causa: pd.Series) -> pd.Series:
    """Retorna o capítulo CID-10 a partir do código de 3 ou 4 caracteres."""
    c = causa.astype(str).str.upper().str.strip().str[0]
    mapping = {
        "A": "I. Infecciosas e parasitárias",
        "B": "I. Infecciosas e parasitárias",
        "C": "II. Neoplasias",
        "D": "II. Neoplasias / III. Sangue / IV. Endócrinas",
        "E": "IV. Endócrinas, nutricionais e metabólicas",
        "F": "V. Transtornos mentais e comportamentais",
        "G": "VI. Sistema nervoso",
        "H": "VII. Olho / VIII. Ouvido",
        "I": "IX. Sistema circulatório",
        "J": "X. Sistema respiratório",
        "K": "XI. Sistema digestivo",
        "L": "XII. Pele e tecido subcutâneo",
        "M": "XIII. Sistema osteomuscular",
        "N": "XIV. Sistema geniturinário",
        "O": "XV. Gravidez, parto e puerpério",
        "P": "XVI. Período perinatal",
        "Q": "XVII. Malformações congênitas",
        "R": "XVIII. Sintomas, sinais e achados",
        "S": "XIX. Lesões, envenenamentos (S00-T98)",
        "T": "XIX. Lesões, envenenamentos (S00-T98)",
        "V": "XX. Causas externas (V01-Y89)",
        "W": "XX. Causas externas (V01-Y89)",
        "X": "XX. Causas externas (V01-Y89)",
        "Y": "XX. Causas externas (V01-Y89)",
        "Z": "XXI. Fatores que influenciam o estado de saúde",
        "U": "XXII. Códigos para propósitos especiais",
    }
    return c.map(mapping).fillna("Não classificado")


def processa_ano(ano: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Processa um único ano do SIM e retorna (agregado, trabalho)."""
    path = RAW_DIR / f"DO_SC_{ano}.parquet"
    df = pd.read_parquet(path)

    # Normaliza códigos de município (6 dígitos, strip)
    df["codmunres_6d"] = df["CODMUNRES"].astype(str).str.strip().str[:6]
    df["codmunocor_6d"] = df["CODMUNOCOR"].astype(str).str.strip().str[:6]

    # Filtro: óbitos no Oeste (residência ou ocorrência)
    mask_oeste = (
        df["codmunres_6d"].isin(MUNICIPIOS_OESTE_6D)
        | df["codmunocor_6d"].isin(MUNICIPIOS_OESTE_6D)
    )
    df_oeste = df[mask_oeste].copy()

    if df_oeste.empty:
        return pd.DataFrame(), pd.DataFrame()

    # Adiciona colunas derivadas
    df_oeste["municipio_6d"] = df_oeste["codmunres_6d"].where(
        df_oeste["codmunres_6d"].isin(MUNICIPIOS_OESTE_6D),
        df_oeste["codmunocor_6d"],
    )
    df_oeste["municipio_nome"] = df_oeste["municipio_6d"].map(MUNICIPIO_NOME)
    df_oeste["ano"] = ano
    df_oeste["sexo_desc"] = df_oeste["SEXO"].map({"1": "Masculino", "2": "Feminino", "0": "Ignorado"}).fillna("Ignorado")
    df_oeste["faixa_etaria"] = decodifica_idade(df_oeste["IDADE"])
    df_oeste["cap_cid10"] = cap_cid10(df_oeste["CAUSABAS"])

    # --- Agregação 1: consolidado por município/ano ---
    agg = (
        df_oeste.groupby(["municipio_6d", "municipio_nome", "ano"])
        .agg(
            total_obitos=("CONTADOR", "size"),
            obitos_masculino=("sexo_desc", lambda x: (x == "Masculino").sum()),
            obitos_feminino=("sexo_desc", lambda x: (x == "Feminino").sum()),
            obitos_sexo_ignorado=("sexo_desc", lambda x: (x == "Ignorado").sum()),
        )
        .reset_index()
    )

    # Agregação por faixa etária (wide format)
    agg_fx = (
        df_oeste.groupby(["municipio_6d", "ano", "faixa_etaria"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    agg_fx.columns = [f"obitos_fx_{c}" if c not in ("municipio_6d", "ano") else c for c in agg_fx.columns]

    # Agregação por capítulo CID-10 (top 10 por município/ano)
    agg_cid = (
        df_oeste.groupby(["municipio_6d", "ano", "cap_cid10"])
        .size()
        .reset_index(name="obitos")
    )

    # Junta tudo
    agg = agg.merge(agg_fx, on=["municipio_6d", "ano"], how="left")

    # --- Subconjunto causas de trabalho ---
    # Capítulos XIX e XX do CID-10
    mask_trabalho = df_oeste["cap_cid10"].isin([
        "XIX. Lesões, envenenamentos (S00-T98)",
        "XX. Causas externas (V01-Y89)",
    ])
    # Inclui também ACIDTRAB == 1 (acidente de trabalho)
    mask_acid = df_oeste.get("ACIDTRAB", pd.Series("", index=df_oeste.index)).astype(str) == "1"
    df_trabalho = df_oeste[mask_trabalho | mask_acid].copy()

    # Seleciona colunas úteis para o subconjunto
    cols_trabalho = [
        "ano", "municipio_6d", "municipio_nome", "SEXO", "sexo_desc",
        "IDADE", "faixa_etaria", "CAUSABAS", "cap_cid10",
        "ACIDTRAB", "CIRCOBITO", "LOCOCOR", "CODMUNRES", "CODMUNOCOR",
    ]
    cols_existentes = [c for c in cols_trabalho if c in df_trabalho.columns]
    df_trabalho = df_trabalho[cols_existentes].copy()

    return agg, agg_cid, df_trabalho


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    list_agg: list[pd.DataFrame] = []
    list_agg_cid: list[pd.DataFrame] = []
    list_trabalho: list[pd.DataFrame] = []

    for ano in ANOS:
        print(f"Processando {ano} ...")
        agg, agg_cid, trabalho = processa_ano(ano)
        if not agg.empty:
            list_agg.append(agg)
            list_agg_cid.append(agg_cid)
        if not trabalho.empty:
            list_trabalho.append(trabalho)

    # Consolida
    df_agg = pd.concat(list_agg, ignore_index=True) if list_agg else pd.DataFrame()
    df_agg_cid = pd.concat(list_agg_cid, ignore_index=True) if list_agg_cid else pd.DataFrame()
    df_trabalho = pd.concat(list_trabalho, ignore_index=True) if list_trabalho else pd.DataFrame()

    # Salva consolidado principal (long format para CID)
    if not df_agg.empty:
        df_agg.to_parquet(PROCESSED_DIR / "datasus_sim_oeste_sc.parquet", index=False)
        print(f"Salvo datasus_sim_oeste_sc.parquet ({len(df_agg)} registros)")

    if not df_agg_cid.empty:
        df_agg_cid.to_parquet(PROCESSED_DIR / "datasus_sim_oeste_sc_cid.parquet", index=False)
        print(f"Salvo datasus_sim_oeste_sc_cid.parquet ({len(df_agg_cid)} registros)")

    if not df_trabalho.empty:
        df_trabalho.to_parquet(PROCESSED_DIR / "datasus_sim_causas_trabalho_oeste.parquet", index=False)
        print(f"Salvo datasus_sim_causas_trabalho_oeste.parquet ({len(df_trabalho)} registros)")

    print("Concluído!")


if __name__ == "__main__":
    main()
