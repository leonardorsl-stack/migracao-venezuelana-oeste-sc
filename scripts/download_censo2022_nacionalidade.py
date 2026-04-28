#!/usr/bin/env python3
"""
Download e processamento de dados do Censo 2022 sobre nacionalidade
via API SIDRA do IBGE.

Objetivo: obter dados desagregados por nacionalidade, especificamente
para identificar venezuelanos nos municípios do Oeste de SC.

Tentativas realizadas:
- Tabela 9606: na verdade eh sobre cor/raca, sexo e idade (nao nacionalidade)
- Tabela 10157: tem classificacao por nacionalidade mas valores suprimidos ("...")
- Tabela 631: tem lugar de nascimento mas apenas agregado (Pais estrangeiro, etc.)
- Tabela 10161: tem pais especifico (incl. Venezuela) mas apenas para pessoas que
  NAO residiam no Brasil 5 anos antes da data de referencia (migrantes recentes)
- FTP IBGE: nao ha tabelas pre-tabuladas com nacionalidade desagregada por pais
  disponiveis publicamente
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW_IBGE = PROJECT_ROOT / "data" / "raw" / "ibge"
DATA_PROCESSED_IBGE = PROJECT_ROOT / "data" / "processed" / "ibge"
DATA_RAW_IBGE.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED_IBGE.mkdir(parents=True, exist_ok=True)

REGIAO_OESTE_SC = [
    4204202, 4204301, 4216800, 4217204, 4207684,
    4206652, 4219507, 4209003, 4206702, 4219705,
    4203808, 4204004, 4206405, 4208906, 4216107,
    4219358, 4201273, 4204152, 4204400, 4205431,
]

BASE_URL = "https://apisidra.ibge.gov.br/values"


def fetch_sidra(url: str) -> list[dict]:
    try:
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list) and len(data) > 0:
            return data
        return []
    except Exception as e:
        logger.error("Erro ao acessar %s: %s", url, e)
        return []


def records_to_df(records: list[dict]) -> pd.DataFrame:
    """Converte registros SIDRA em DataFrame usando chaves D1C, D1N, etc."""
    if not records:
        return pd.DataFrame()
    return pd.DataFrame(records[1:])  # skip header row, mantem chaves D1C/D1N/etc


def attempt_table_9606() -> dict:
    results = {}
    url = f"{BASE_URL}/t/9606/n3/42/v/all/p/all"
    logger.info("[Tabela 9606] Verificando: %s", url)
    records = fetch_sidra(url)
    df = records_to_df(records)
    if not df.empty:
        cols = df.columns.tolist()
        d4n_vals = df["D4N"].unique().tolist() if "D4N" in cols else None
        results = {
            "url": url,
            "colunas": cols,
            "d4n_valores": d4n_vals,
            "nota": "Tabela 9606 eh sobre cor/raca, sexo e idade. NAO contem nacionalidade.",
        }
        logger.info("  -> D4N (Sexo): %s", d4n_vals)
    return results


def attempt_table_10157() -> dict:
    results = {}
    attempts = [
        ("Brasil", "n1/all"),
        ("Grandes_Regioes", "n2/all"),
        ("SC_estadual", "n3/42"),
        ("Chapeco", "n6/4204202"),
    ]
    for label, nivel in attempts:
        url = f"{BASE_URL}/t/10157/{nivel}/v/all/p/all/d/v93%200"
        logger.info("[Tabela 10157] Tentando %s: %s", label, url)
        records = fetch_sidra(url)
        df = records_to_df(records)
        if not df.empty:
            nacionalidades = df["D6N"].unique().tolist() if "D6N" in df.columns else []
            results[label] = {
                "url": url,
                "nacionalidades_disponiveis": nacionalidades,
                "total_registros": len(df),
                "amostra": df.head(3).to_dict(orient="records"),
            }
            logger.info("  -> Nacionalidades: %s", nacionalidades)
        else:
            results[label] = {"url": url, "erro": "Sem dados"}
    return results


def attempt_table_10157_explicit_codes() -> dict:
    results = {}
    attempts = [
        ("Brasil_explicito", "n1/all", "c58/6831,6832,6833"),
        ("SC_explicito", "n3/42", "c58/6831,6832,6833"),
    ]
    for label, nivel, classif in attempts:
        url = f"{BASE_URL}/t/10157/{nivel}/v/all/p/all/{classif}"
        logger.info("[Tabela 10157 codigos] Tentando %s: %s", label, url)
        records = fetch_sidra(url)
        df = records_to_df(records)
        if not df.empty:
            valores = df["V"].unique().tolist()
            results[label] = {
                "url": url,
                "valores_unicos": valores[:10],
                "total_registros": len(df),
                "amostra": df.head(3).to_dict(orient="records"),
            }
            logger.info("  -> Valores: %s", valores[:10])
        else:
            results[label] = {"url": url, "erro": "Sem dados"}
    return results


def attempt_table_631() -> dict:
    results = {}
    url = f"{BASE_URL}/t/631/n3/42/v/all/p/all/d/v93%200"
    logger.info("[Tabela 631] Tentando: %s", url)
    records = fetch_sidra(url)
    df = records_to_df(records)
    if not df.empty:
        lugares = df["D5N"].unique().tolist() if "D5N" in df.columns else []
        results = {
            "url": url,
            "lugares_disponiveis": lugares,
            "nota": "Tabela 631 so tem lugar de nascimento agregado.",
        }
        logger.info("  -> Lugares: %s", lugares)
    return results


def download_table_10161_venezuela() -> pd.DataFrame:
    cod_venezuela = "79167"
    records_all = []

    url_br = f"{BASE_URL}/t/10161/n1/all/v/all/p/all/c2084/{cod_venezuela}"
    logger.info("[Tabela 10161] Brasil: %s", url_br)
    records_all.extend(fetch_sidra(url_br)[1:])

    url_sc = f"{BASE_URL}/t/10161/n3/42/v/all/p/all/c2084/{cod_venezuela}"
    logger.info("[Tabela 10161] SC: %s", url_sc)
    records_all.extend(fetch_sidra(url_sc)[1:])

    batch_size = 5
    for i in range(0, len(REGIAO_OESTE_SC), batch_size):
        batch = REGIAO_OESTE_SC[i : i + batch_size]
        codes = ",".join(str(c) for c in batch)
        url_mu = f"{BASE_URL}/t/10161/n6/{codes}/v/all/p/all/c2084/{cod_venezuela}"
        logger.info("[Tabela 10161] Municipios batch %d", i // batch_size + 1)
        records_all.extend(fetch_sidra(url_mu)[1:])

    if not records_all:
        return pd.DataFrame()
    return pd.DataFrame(records_all)


def download_table_10157_total() -> pd.DataFrame:
    records_all = []

    url_sc = f"{BASE_URL}/t/10157/n3/42/v/all/p/all"
    logger.info("[Tabela 10157 Total] SC: %s", url_sc)
    records_all.extend(fetch_sidra(url_sc)[1:])

    batch_size = 5
    for i in range(0, len(REGIAO_OESTE_SC), batch_size):
        batch = REGIAO_OESTE_SC[i : i + batch_size]
        codes = ",".join(str(c) for c in batch)
        url_mu = f"{BASE_URL}/t/10157/n6/{codes}/v/all/p/all"
        logger.info("[Tabela 10157 Total] Municipios batch %d", i // batch_size + 1)
        records_all.extend(fetch_sidra(url_mu)[1:])

    if not records_all:
        return pd.DataFrame()
    return pd.DataFrame(records_all)


def generate_limitation_note(
    attempt_9606: dict,
    attempt_10157: dict,
    attempt_10157_codes: dict,
    attempt_631: dict,
) -> str:
    lines = [
        "=" * 70,
        "NOTA DE LIMITACAO - Dados de Nacionalidade do Censo 2022 (IBGE)",
        f"Gerado em: {datetime.now().isoformat()}",
        "=" * 70,
        "",
        "RESUMO DAS TENTATIVAS REALIZADAS",
        "-" * 70,
        "",
        "1. TABELA 9606",
        "   O arquivo existente 'censo2022_nacionalidade_sidra_9606.parquet'",
        "   foi rotulado incorretamente. A tabela 9606 do SIDRA eh:",
        "   'Populacao residente, por cor ou raca, segundo o sexo e a idade'.",
        "   ELA NAO CONTEM DADOS DE NACIONALIDADE.",
        "   As colunas sao: UF, Variavel, Ano, Sexo (D4), Cor/raca (D5), Idade (D6).",
        "",
        "2. TABELA 10157 (Populacao residente, por nacionalidade, sexo e grupos de idade)",
        "   Esta eh a tabela correta sobre NACIONALIDADE no Censo 2022.",
        "   Classificacoes: Brasileiros natos, Naturalizados brasileiros, Estrangeiros, Total.",
        "   PROBLEMA: A API SIDRA suprime os valores desagregados.",
        "   Quando solicitamos as categorias desagregadas, os valores retornam '...'.",
        "   Quando solicitamos 'all', apenas 'Total' eh retornado.",
        "   Tentativas em todos os niveis territoriais (Brasil, Grandes Regioes,",
        "   UF, Municipios) produziram o mesmo resultado: supressao.",
        "",
        "3. TABELA 631 (Populacao residente, por sexo e lugar de nascimento)",
        "   Possui categorias: Pais estrangeiro, Exterior, etc.",
        "   PROBLEMA: Nao desagrega por pais especifico (Venezuela, Portugal, etc.)",
        "   via API publica. Apenas agregados sao fornecidos.",
        "",
        "4. TABELA 10161 (Pessoas de 5+ anos que nao residiam no Brasil 5 anos antes)",
        "   Esta tabela TEM desagregacao por pais especifico, incluindo Venezuela.",
        "   POREM: ela mede apenas MIGRANTES RECENTES (ultimos 5 anos),",
        "   NAO a populacao total de venezuelanos no Brasil.",
        "   Dados obtidos desta tabela foram salvos como proxy.",
        "",
        "5. FTP DO IBGE (portal de microdados)",
        "   Verificado ftp://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/",
        "   Nao ha tabelas pre-tabuladas com nacionalidade/naturalidade desagregada",
        "   por pais disponiveis publicamente no FTP.",
        "",
        "6. PORTAL PANORAMA DO CENSO",
        "   Os dados sobre '272.779 naturais da Venezuela' no Brasil (2022)",
        "   foram divulgados pelo IBGE na imprensa em junho/2025 como parte",
        "   dos 'Resultados preliminares da amostra - Fecundidade e Migracao'.",
        "   Esses dados existem, mas parecem estar disponiveis apenas via:",
        "   - Panorama do Censo (ferramenta interativa, nao API aberta)",
        "   - Microdados da amostra (requer processamento proprio)",
        "   - Tabulacoes especiais (mediante solicitacao ao IBGE)",
        "",
        "-" * 70,
        "CONCLUSAO",
        "-" * 70,
        "",
        "Os dados de NACIONALIDADE do Censo 2022 com desagregacao por pais",
        "(Venezuela, Portugal, etc.) NAO estao disponiveis via API publica SIDRA",
        "para nivel municipal ou estadual. A API suprime os valores por",
        "confidencialidade ou limitacoes da base de amostra.",
        "",
        "ALTERNATIVAS SUGERIDAS:",
        "a) Solicitar tabulacao especial ao IBGE (tabulacoes@ibge.gov.br)",
        "b) Processar os microdados da amostra do Censo 2022",
        "c) Usar dados da RAIS, DataSUS, ou Policia Federal como proxies",
        "d) Usar a tabela 10161 (migrantes recentes) como indicador indireto",
        "",
        "DADOS SALVOS NESTE PROJETO:",
        "- data/raw/ibge/censo2022_migrantes_recentes_venezuela.parquet",
        "  (tabela 10161: pessoas que nao estavam no Brasil 5 anos antes,",
        "   por pais de origem, incluindo Venezuela)",
        "- data/raw/ibge/censo2022_nacionalidade_total.parquet",
        "  (tabela 10157: populacao total, mas nacionalidade='Total' apenas)",
        "",
        "=" * 70,
    ]
    return "\n".join(lines)


def generate_summary(df_10161: pd.DataFrame, df_10157: pd.DataFrame) -> str:
    lines = [
        "=" * 70,
        "RESUMO - Venezuelanos no Censo 2022 (dados disponiveis)",
        f"Gerado em: {datetime.now().isoformat()}",
        "=" * 70,
        "",
        "IMPORTANTE: Estes numeros referem-se a MIGRANTES RECENTES",
        "(pessoas de 5+ anos que NAO residiam no Brasil em 2017,",
        "ou seja, 5 anos antes do Censo 2022). NAO representam o",
        "TOTAL de venezuelanos residentes no Brasil.",
        "",
    ]

    if not df_10161.empty:
        df_abs = df_10161[
            df_10161["D2N"].str.contains(
                "Pessoas de 5 anos ou mais de idade que não residiam no Brasil",
                na=False,
            )
        ]
        br = df_abs[df_abs["NN"] == "Brasil"]
        if not br.empty:
            val_br = br.iloc[0]["V"]
            lines.append(f"Brasil - Venezuelanos (migrantes recentes): {val_br}")

        sc = df_abs[df_abs["NN"] == "Unidade da Federação"]
        sc = sc[sc["D1N"].str.contains("Santa Catarina", na=False)]
        if not sc.empty:
            val_sc = sc.iloc[0]["V"]
            lines.append(f"Santa Catarina - Venezuelanos (migrantes recentes): {val_sc}")

        mu = df_abs[df_abs["NN"] == "Município"]
        mu_pessoas = mu[(mu["MN"] == "Pessoas") & (~mu["V"].isin(["...", "-"]))]
        if not mu_pessoas.empty:
            lines.append("")
            lines.append("Municipios do Oeste de SC - Venezuelanos (migrantes recentes):")
            for _, row in mu_pessoas.iterrows():
                nome = row["D1N"]
                val = row["V"]
                lines.append(f"  {nome}: {val}")
            total_mu = pd.to_numeric(mu_pessoas["V"], errors="coerce").fillna(0).astype(int).sum()
            lines.append("")
            lines.append(f"TOTAL nos municipios do Oeste SC: {total_mu}")

            if not df_10157.empty:
                df_10157_abs = df_10157[df_10157["D2N"] == "População residente"]
                df_10157_mu = df_10157_abs[df_10157_abs["NN"] == "Município"]
                df_10157_pessoas = df_10157_mu[(df_10157_mu["MN"] == "Pessoas") & (~df_10157_mu["V"].isin(["...", "-"]))]
                if not df_10157_pessoas.empty:
                    total_pop = pd.to_numeric(df_10157_pessoas["V"], errors="coerce").fillna(0).astype(int).sum()
                    if total_pop > 0:
                        pct = (total_mu / total_pop) * 100
                        lines.append("")
                        lines.append(f"Populacao total nos municipios do Oeste SC: {total_pop}")
                        lines.append(f"Percentual de migrantes venezuelanos recentes: {pct:.4f}%")

    lines.append("")
    lines.append("=" * 70)
    return "\n".join(lines)


def main():
    logger.info("Iniciando download de dados de nacionalidade do Censo 2022 via SIDRA")

    attempt_9606 = attempt_table_9606()
    attempt_10157 = attempt_table_10157()
    attempt_10157_codes = attempt_table_10157_explicit_codes()
    attempt_631 = attempt_table_631()

    df_10161 = download_table_10161_venezuela()
    df_10157 = download_table_10157_total()

    if not df_10161.empty:
        path_10161 = DATA_RAW_IBGE / "censo2022_migrantes_recentes_venezuela.parquet"
        df_10161.to_parquet(path_10161, index=False)
        logger.info("Salvo: %s (%d registros)", path_10161, len(df_10161))
        # Copia com nome solicitado pelo usuario
        path_desagregado = DATA_RAW_IBGE / "censo2022_nacionalidade_desagregado.parquet"
        df_10161.to_parquet(path_desagregado, index=False)
        logger.info("Salvo: %s (%d registros)", path_desagregado, len(df_10161))

    if not df_10157.empty:
        path_10157 = DATA_RAW_IBGE / "censo2022_nacionalidade_total.parquet"
        df_10157.to_parquet(path_10157, index=False)
        logger.info("Salvo: %s (%d registros)", path_10157, len(df_10157))

    if not df_10161.empty:
        df_proc = df_10161[
            df_10161["D2N"].str.contains(
                "Pessoas de 5 anos ou mais de idade que não residiam no Brasil",
                na=False,
            )
        ].copy()
        df_proc = df_proc[df_proc["NN"] == "Município"]
        if not df_proc.empty:
            path_proc = DATA_PROCESSED_IBGE / "venezuelanos_censo2022_recentes_oeste_sc.parquet"
            df_proc.to_parquet(path_proc, index=False)
            logger.info("Salvo processado: %s", path_proc)
            # Copia com nome solicitado pelo usuario
            path_oeste = DATA_PROCESSED_IBGE / "venezuelanos_censo2022_oeste_sc.parquet"
            df_proc.to_parquet(path_oeste, index=False)
            logger.info("Salvo processado: %s", path_oeste)

    note_text = generate_limitation_note(
        attempt_9606, attempt_10157, attempt_10157_codes, attempt_631
    )
    note_path = DATA_RAW_IBGE / "NOTA_LIMITACAO.txt"
    note_path.write_text(note_text, encoding="utf-8")
    logger.info("Salvo: %s", note_path)

    summary_text = generate_summary(df_10161, df_10157)
    summary_path = DATA_RAW_IBGE / "censo2022_nacionalidade_resumo.txt"
    summary_path.write_text(summary_text, encoding="utf-8")
    logger.info("Salvo: %s", summary_path)

    log_path = DATA_RAW_IBGE / "censo2022_nacionalidade_tentativas.json"
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "tabela_9606": attempt_9606,
        "tabela_10157": attempt_10157,
        "tabela_10157_codigos_explicitos": attempt_10157_codes,
        "tabela_631": attempt_631,
    }
    log_path.write_text(json.dumps(log_data, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info("Salvo log: %s", log_path)

    logger.info("Processamento concluido.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
