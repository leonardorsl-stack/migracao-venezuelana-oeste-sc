"""
Dashboard Streamlit — Raio X da Migração Venezuelana no Oeste de SC

Projeto: migracao-venezuelana-oeste-sc
Autores: Leonardo Rafael Santos Leitao e Vicente Neves da Silva Ribeiro (UFFS)

Uso:
    streamlit run src/visualization/dashboard.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from config import SETTINGS  # noqa: E402

# =====================================================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================================================
st.set_page_config(
    page_title="Raio X da Migração Venezuelana no Oeste de SC",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================================
# FUNÇÕES DE CARGA DE DADOS (com cache)
# =====================================================================
@st.cache_data(show_spinner=False)
def carregar_painel() -> pd.DataFrame:
    path = SETTINGS.DATA_PROCESSED / "painel_oeste_sc_2018_2024.parquet"
    if not path.exists():
        st.error(f"Arquivo não encontrado: {path}")
        return pd.DataFrame()
    return pd.read_parquet(path)


@st.cache_data(show_spinner=False)
def carregar_rais_oeste() -> pd.DataFrame:
    oeste_6d = [int(str(c)[:6]) for c in SETTINGS.REGIAO_OESTE_SC]
    frames = []
    for ano in range(2018, 2025):
        f = SETTINGS.DATA_PROCESSED / f"rais_vinculos_sc_venezuela_{ano}.parquet"
        if not f.exists():
            continue
        df = pd.read_parquet(f)
        df["ano"] = ano
        df["codigo_ibge_6d"] = df["municipio"].astype(int)
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    rais = pd.concat(frames, ignore_index=True)
    return rais[rais["codigo_ibge_6d"].isin(oeste_6d)]


@st.cache_data(show_spinner=False)
def carregar_sih_oeste() -> pd.DataFrame:
    path = SETTINGS.DATA_RAW / "datasus" / "sih_sus_sc_venezuela_2018_2025.parquet"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_parquet(path)
    oeste_6d = [int(str(c)[:6]) for c in SETTINGS.REGIAO_OESTE_SC]
    df["mun_res_num"] = pd.to_numeric(df["MUNIC_RES"], errors="coerce")
    return df[df["mun_res_num"].isin(oeste_6d)].copy()


# =====================================================================
# CARREGAMENTO
# =====================================================================
painel = carregar_painel()
rais_oeste = carregar_rais_oeste()
sih_oeste = carregar_sih_oeste()

if painel.empty:
    st.error("Dados do painel longitudinal não encontrados. Execute o pipeline primeiro.")
    st.stop()

municipios = sorted(painel["municipio"].dropna().unique().tolist())
anos = sorted(painel["ano"].unique().tolist())

# =====================================================================
# SIDEBAR — FILTROS
# =====================================================================
st.sidebar.title("🎛️ Filtros")

municipio_sel = st.sidebar.multiselect(
    "Município(s)",
    options=["Todos"] + municipios,
    default=["Todos"],
)

ano_sel = st.sidebar.slider(
    "Ano",
    min_value=min(anos),
    max_value=max(anos),
    value=(min(anos), max(anos)),
)

mask = (painel["ano"] >= ano_sel[0]) & (painel["ano"] <= ano_sel[1])
if "Todos" not in municipio_sel:
    mask &= painel["municipio"].isin(municipio_sel)
painel_filt = painel[mask].copy()

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Registros selecionados:** {len(painel_filt):,}")
st.sidebar.markdown(f"**Municípios:** {painel_filt['municipio'].nunique()}")
st.sidebar.markdown(f"**Período:** {ano_sel[0]}–{ano_sel[1]}")

# =====================================================================
# TÍTULO PRINCIPAL
# =====================================================================
st.title("🌎 Raio X da Migração Venezuelana no Oeste de SC")
st.markdown(
    "***Dashboard interativo do projeto de pesquisa UFFS — Região Intermediária de Chapecó (109 municípios, 2018-2024)***"
)
st.divider()

# =====================================================================
# KPIs
# =====================================================================
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_vinc = painel_filt["total_vinculos_rais"].sum()
    st.metric("Vínculos RAIS", f"{total_vinc:,.0f}")

with col2:
    total_int = painel_filt["total_internacoes_sih"].sum()
    st.metric("Internações SIH", f"{total_int:,.0f}")

with col3:
    pop_ult = painel_filt[painel_filt["ano"] == painel_filt["ano"].max()]["populacao_total"].sum()
    st.metric("População (último ano)", f"{pop_ult:,.0f}")

with col4:
    taxa_vinc = (
        painel_filt[painel_filt["ano"] == painel_filt["ano"].max()]["total_vinculos_rais"].sum()
        / pop_ult * 1000 if pop_ult > 0 else 0
    )
    st.metric("Taxa vínculos/mil", f"{taxa_vinc:.1f}")

with col5:
    mun_com = painel_filt[painel_filt["total_vinculos_rais"] > 0]["municipio"].nunique()
    st.metric("Municípios com vínculos", f"{mun_com}")

st.divider()

# =====================================================================
# ABAS
# =====================================================================
tab1, tab2, tab3, tab4 = st.tabs(
    ["📈 Visão Geral", "💼 Trabalho", "🏥 Saúde", "📋 Dados Brutos"]
)

# ---------------------------------------------------------------------
# ABA 1: VISÃO GERAL
# ---------------------------------------------------------------------
with tab1:
    st.subheader("Evolução Temporal — Região Oeste SC")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**Vínculos de Emprego (RAIS)**")
        evo_vinc = painel_filt.groupby("ano").agg(
            {"total_vinculos_rais": "sum", "populacao_total": "sum"}
        ).reset_index()
        st.line_chart(evo_vinc.set_index("ano")[["total_vinculos_rais"]])
        st.caption("Fonte: RAIS/MTE")

    with c2:
        st.markdown("**Internações Hospitalares (SIH/SUS)**")
        evo_sih = painel_filt.groupby("ano").agg(
            {"total_internacoes_sih": "sum", "populacao_total": "sum"}
        ).reset_index()
        st.line_chart(evo_sih.set_index("ano")[["total_internacoes_sih"]])
        st.caption("Fonte: SIH/SUS")

    st.markdown("---")
    st.subheader(f"Top 10 Municípios — {painel_filt['ano'].max()}")
    top_mun = (
        painel_filt[painel_filt["ano"] == painel_filt["ano"].max()]
        .nlargest(10, "total_vinculos_rais")[["municipio", "total_vinculos_rais"]]
        .sort_values("total_vinculos_rais")
    )
    st.bar_chart(top_mun.set_index("municipio"))

    st.markdown("---")
    st.subheader("Mapa de Calor — Vínculos por Município e Ano")
    heatmap = painel_filt.pivot_table(
        index="municipio", columns="ano", values="total_vinculos_rais", fill_value=0
    )
    st.dataframe(heatmap.style.format("{:,.0f}"), use_container_width=True)

# ---------------------------------------------------------------------
# ABA 2: TRABALHO
# ---------------------------------------------------------------------
with tab2:
    if rais_oeste.empty:
        st.info("Dados da RAIS não disponíveis.")
    else:
        st.subheader("Perfil Ocupacional")
        c1, c2 = st.columns(2)

        with c1:
            st.markdown("**Principais Ocupações (CBO)**")
            cbo = rais_oeste["cbo_2002"].value_counts().head(10).reset_index()
            cbo.columns = ["CBO", "Vínculos"]
            st.bar_chart(cbo.sort_values("Vínculos").set_index("CBO"))

        with c2:
            st.markdown("**Principais Setores (CNAE)**")
            cnae = rais_oeste["cnae_20_classe"].value_counts().head(10).reset_index()
            cnae.columns = ["CNAE", "Vínculos"]
            st.bar_chart(cnae.sort_values("Vínculos").set_index("CNAE"))

        st.markdown("---")
        st.subheader("Perfil Demográfico dos Trabalhadores")
        c3, c4 = st.columns(2)

        with c3:
            st.markdown("**Distribuição por Sexo**")
            sexo = rais_oeste["sexo"].map({"1": "Masculino", "2": "Feminino"}).value_counts()
            st.bar_chart(sexo)

        with c4:
            st.markdown("**Distribuição por Idade**")
            bins = [0, 18, 25, 30, 40, 50, 60, 100]
            labels = ["<18", "18-24", "25-29", "30-39", "40-49", "50-59", "60+"]
            fx = pd.cut(rais_oeste["idade"], bins=bins, labels=labels, right=False).value_counts().sort_index()
            st.bar_chart(fx)

        st.markdown("---")
        st.subheader("Evolução da Composição de Gênero")
        sexo_ano = (
            rais_oeste.groupby("ano")["sexo"]
            .apply(lambda x: (x == "2").mean() * 100)
            .reset_index(name="% Feminino")
        )
        st.line_chart(sexo_ano.set_index("ano"))

# ---------------------------------------------------------------------
# ABA 3: SAÚDE
# ---------------------------------------------------------------------
with tab3:
    if sih_oeste.empty:
        st.info("Dados do SIH/SUS não disponíveis.")
    else:
        st.subheader("Perfil de Morbidade Hospitalar")
        c1, c2 = st.columns(2)

        with c1:
            st.markdown("**Top 10 Diagnósticos (CID-10)**")
            cids = sih_oeste["DIAG_PRINC"].value_counts().head(10).reset_index()
            cids.columns = ["CID-10", "Internações"]
            st.bar_chart(cids.sort_values("Internações").set_index("CID-10"))

        with c2:
            st.markdown("**Evolução Anual das Internações**")
            evo = sih_oeste.groupby("ano").size().reset_index(name="Internações")
            st.line_chart(evo.set_index("ano"))

        st.markdown("---")
        st.subheader("Distribuição por Capítulo CID-10")

        def cap_cid(cid):
            c = str(cid)[0].upper() if pd.notna(cid) else ""
            caps = {
                "A": "I. Infecções", "B": "I. Infecções",
                "C": "II. Neoplasias", "D": "II-III. Neoplasias/Sangue",
                "E": "IV. Endócrinas", "F": "V. Mentais",
                "G": "VI. Nervoso", "H": "VII-VIII. Olho/Ouvido",
                "I": "IX. Circulatório", "J": "X. Respiratório",
                "K": "XI. Digestivo", "L": "XII. Pele",
                "M": "XIII. Osteomuscular", "N": "XIV. Geniturinário",
                "O": "XV. Gravidez/Parto", "P": "XVI. Perinatal",
                "Q": "XVII. Malformações", "R": "XVIII. Sintomas",
                "S": "XIX. Trauma", "T": "XIX. Trauma",
                "V": "XX. Causas externas", "W": "XX. Causas externas",
                "X": "XX. Causas externas", "Y": "XX. Causas externas",
                "Z": "XXI. Saúde/serviços",
            }
            return caps.get(c, "Outros")

        sih_oeste["capitulo"] = sih_oeste["DIAG_PRINC"].apply(cap_cid)
        caps = sih_oeste["capitulo"].value_counts().head(10).reset_index()
        caps.columns = ["Capítulo", "Internações"]
        st.bar_chart(caps.sort_values("Internações").set_index("Capítulo"))

        st.markdown("---")
        st.subheader("Análise por Município de Residência")
        mun = sih_oeste["MUNIC_RES"].value_counts().head(15).reset_index()
        mun.columns = ["Código IBGE", "Internações"]
        st.dataframe(mun, use_container_width=True)

# ---------------------------------------------------------------------
# ABA 4: DADOS BRUTOS
# ---------------------------------------------------------------------
with tab4:
    st.subheader("Painel Longitudinal — Dados Filtrados")
    st.dataframe(painel_filt, use_container_width=True)
    st.download_button(
        label="📥 Baixar dados filtrados (CSV)",
        data=painel_filt.to_csv(index=False).encode("utf-8"),
        file_name="painel_oeste_sc_filtrado.csv",
        mime="text/csv",
    )
    st.markdown("---")
    st.subheader("Estatísticas Descritivas")
    st.write(painel_filt.describe())

# =====================================================================
# RODAPÉ
# =====================================================================
st.divider()
st.caption(
    "Fonte: IBGE, DataSUS (SIH/SUS), RAIS/MTE | "
    "Projeto UFFS — Crise, migração e trabalho | "
    "Dados atualizados em abril de 2026"
)
