"""
Dashboard Streamlit para o projeto.

Projeto: migracao-venezuelana-oeste-sc
Autores: Leonardo Rafael Santos Leitao e Vicente Neves da Silva Ribeiro (UFFS)
"""

import pandas as pd
import streamlit as st


def main():
    """
    Funcao principal do dashboard Streamlit.
    """
    st.set_page_config(
        page_title="Raio X da Migracao Venezuelana no Oeste de SC",
        page_icon="🌎",
        layout="wide",
    )

    st.title("🌎 Raio X da Migracao Venezuelana no Oeste de SC")
    st.markdown("***Dashboard interativo do projeto de pesquisa UFFS***")

    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        municipio = st.selectbox(
            "Municipio",
            ["Todos", "Chapeco", "Xanxere", "Concordia", "Joacaba",
             "Sao Miguel do Oeste", "Maravilha", "Sao Lourenco do Oeste"]
        )
    with col2:
        ano = st.selectbox("Ano", ["Todos", 2018, 2019, 2020, 2021, 2022, 2023, 2024])
    with col3:
        tema = st.selectbox("Tema", ["Demografia", "Saude", "Trabalho", "Educacao", "Espacial"])

    st.divider()

    # Placeholders para graficos
    st.subheader(f"Indicadores: {tema}")
    if tema == "Demografia":
        st.info("Aqui sera exibida a piramide etaria e indicadores demograficos.")
        # Placeholder: grafico de barras com dados ficticios
        df_demo = pd.DataFrame({
            "faixa_etaria": ["0-14", "15-29", "30-44", "45-59", "60+"],
            "venezuelana": [15, 45, 30, 8, 2],
            "brasileira": [22, 25, 28, 18, 7],
        })
        st.bar_chart(df_demo.set_index("faixa_etaria"))
    elif tema == "Saude":
        st.info("Aqui serao exibidas series temporais de obitos, nascimentos e internacoes.")
    elif tema == "Trabalho":
        st.info("Aqui serao exibidos saldos de emprego, salarios e rotatividade.")
    elif tema == "Educacao":
        st.info("Aqui serao exibidas taxas de matricula e evasao escolar.")
    elif tema == "Espacial":
        st.info("Aqui sera exibido o mapa coropletico e analise LISA.")

    st.divider()
    st.caption("Fonte: IBGE, DataSUS, RAIS, CAGED, SED/SC, SAS/SC | Projeto UFFS 2026")


if __name__ == "__main__":
    main()
