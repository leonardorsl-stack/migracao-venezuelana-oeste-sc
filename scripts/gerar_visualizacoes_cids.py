"""
Gera visualizações de CIDs (diagnósticos) por município no Oeste SC.

Saídas:
    - outputs/figures/14_heatmap_cids_municipios.png
    - outputs/figures/15_composicao_morbidade_municipios.png
    - outputs/figures/16_evolucao_top5_cids.png
    - outputs/reports/top_cids_municipios_oeste_sc.txt
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.config import SETTINGS

# ---------------------------------------------------------------------------
# 1. Configuração de paths e estilo
# ---------------------------------------------------------------------------
OUTPUT_FIGURES = Path(SETTINGS.OUTPUTS) / "figures"
OUTPUT_REPORTS = Path(SETTINGS.OUTPUTS) / "reports"
OUTPUT_FIGURES.mkdir(parents=True, exist_ok=True)
OUTPUT_REPORTS.mkdir(parents=True, exist_ok=True)

plt.style.use("seaborn-v0_8-whitegrid")
sns.set_palette("deep")

# ---------------------------------------------------------------------------
# 2. Carregar dados
# ---------------------------------------------------------------------------
DF_SIH = pd.read_parquet(
    SETTINGS.DATA_RAW / "datasus" / "sih_sus_sc_venezuela_2018_2025.parquet"
)

# Municípios do Oeste SC (6 dígitos, sem dígito verificador)
OESTE_SC_6DIG = [str(m)[:6] for m in SETTINGS.REGIAO_OESTE_SC]

# Nomes dos municípios (do painel)
painel = pd.read_parquet(SETTINGS.DATA_PROCESSED / "painel_oeste_sc_2018_2024.parquet")
MUNICIPIO_NOME = {
    str(k): v
    for k, v in painel[["codigo_ibge_6d", "municipio"]]
    .drop_duplicates()
    .set_index("codigo_ibge_6d")["municipio"]
    .to_dict()
    .items()
}

# ---------------------------------------------------------------------------
# 3. Filtrar dados do Oeste SC
# ---------------------------------------------------------------------------
df = DF_SIH.copy()
df["MUNIC_RES_STR"] = df["MUNIC_RES"].astype(str).str.strip()
df_oeste = df[df["MUNIC_RES_STR"].isin(OESTE_SC_6DIG)].copy()

# Remover CIDs vazios
initial_len = len(df_oeste)
df_oeste = df_oeste[df_oeste["DIAG_PRINC"].notna() & (df_oeste["DIAG_PRINC"].str.strip() != "")]
print(f"Internações no Oeste SC: {len(df_oeste)} (removidas {initial_len - len(df_oeste)} sem CID)")

# ---------------------------------------------------------------------------
# 4. Identificar top CIDs e top municípios
# ---------------------------------------------------------------------------
top20_cids = df_oeste["DIAG_PRINC"].value_counts().head(20)
top15_mun = df_oeste["MUNIC_RES_STR"].value_counts().head(15)

# Para o heatmap: top 15 CIDs (entre os top 20) e top 15 municípios
top15_cids = top20_cids.head(15)

print("\n=== TOP 20 CIDs (frequência absoluta) ===")
for cid, freq in top20_cids.items():
    print(f"{cid:8s} {freq:5d}")

print("\n=== TOP 15 MUNICÍPIOS (frequência absoluta) ===")
for cod, freq in top15_mun.items():
    nome = MUNICIPIO_NOME.get(cod, cod)
    print(f"{cod:6s} {nome:25s} {freq:5d}")

# ---------------------------------------------------------------------------
# 5. HEATMAP — Matriz municípios × CIDs
# ---------------------------------------------------------------------------
# Filtrar apenas top 15 municípios e top 15 CIDs
hm_data = (
    df_oeste[
        df_oeste["MUNIC_RES_STR"].isin(top15_mun.index)
        & df_oeste["DIAG_PRINC"].isin(top15_cids.index)
    ]
    .groupby(["MUNIC_RES_STR", "DIAG_PRINC"])
    .size()
    .unstack(fill_value=0)
)

# Ordenar linhas (municípios) e colunas (CIDs) pela frequência total
hm_data = hm_data.reindex(index=top15_mun.index, columns=top15_cids.index)

# Renomear índice para nomes dos municípios
hm_data.index = [f"{MUNICIPIO_NOME.get(c, c)} ({c})" for c in hm_data.index]

fig, ax = plt.subplots(figsize=(16, 12))
sns.heatmap(
    hm_data,
    annot=True,
    fmt="d",
    cmap="YlOrRd",
    linewidths=0.5,
    linecolor="white",
    cbar_kws={"label": "Nº de internações"},
    ax=ax,
)
ax.set_title(
    "Principais Diagnósticos de Internação — Venezuelanos no Oeste de SC",
    fontsize=16,
    fontweight="bold",
    pad=20,
)
ax.set_xlabel("CID Principal", fontsize=12)
ax.set_ylabel("Município de Residência", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.yticks(rotation=0)
plt.tight_layout()
fig.savefig(OUTPUT_FIGURES / "14_heatmap_cids_municipios.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print(f"\nSalvo: {OUTPUT_FIGURES / '14_heatmap_cids_municipios.png'}")

# ---------------------------------------------------------------------------
# 6. STACKED BAR CHART — Composição por capítulo CID (top 10 municípios)
# ---------------------------------------------------------------------------
# Mapeamento de capítulos CID → descrição (CID-10)
CID_CAPITULOS = {
    "A": "I.   Infecções/parasitárias",
    "B": "I.   Infecções/parasitárias",
    "C": "II.  Neoplasias",
    "D": "III. Sangue/Imunológicas",
    "E": "IV.  Endócrinas",
    "F": "V.   Mentais",
    "G": "VI.  Nervoso",
    "H": "VII. Olho/Ouvido",
    "I": "VIII. Circulatório",
    "J": "IX.  Respiratório",
    "K": "X.   Digestivo",
    "L": "XI.  Pele",
    "M": "XII. Osteomuscular",
    "N": "XIII. Geniturinário",
    "O": "XIV. Gravidez/Parto",
    "P": "XV.  Perinatal",
    "Q": "XVI. Malformações",
    "R": "XVII. Sintomas/Lab",
    "S": "XVIII. Trauma (S)",
    "T": "XVIII. Trauma (T)",
    "V": "XIX.  Causas externas",
    "W": "XIX.  Causas externas",
    "X": "XIX.  Causas externas",
    "Y": "XIX.  Causas externas",
    "Z": "XX.  Contato saúde",
}

def capitulo_cid(cid: str) -> str:
    letra = cid[0].upper() if isinstance(cid, str) and len(cid) > 0 else "?"
    return CID_CAPITULOS.get(letra, f"Outros ({letra})")

# Top 10 municípios
top10_mun = df_oeste["MUNIC_RES_STR"].value_counts().head(10)

df_cap = df_oeste[df_oeste["MUNIC_RES_STR"].isin(top10_mun.index)].copy()
df_cap["capitulo"] = df_cap["DIAG_PRINC"].apply(capitulo_cid)

# Tabela cruzada (município × capítulo) — em % do total do município
cap_pct = (
    pd.crosstab(df_cap["MUNIC_RES_STR"], df_cap["capitulo"], normalize="index")
    * 100
)

# Ordenar linhas pelo total de internações
cap_pct = cap_pct.reindex(index=top10_mun.index)

# Ordenar colunas por frequência total decrescente
col_order = cap_pct.sum().sort_values(ascending=False).index
cap_pct = cap_pct[col_order]

# Renomear índice
cap_pct.index = [f"{MUNICIPIO_NOME.get(c, c)}" for c in cap_pct.index]

fig, ax = plt.subplots(figsize=(14, 8))
cap_pct.plot(
    kind="barh",
    stacked=True,
    ax=ax,
    colormap="tab20",
    width=0.7,
)
ax.invert_yaxis()  # maior no topo
ax.set_title(
    "Composição da Morbidade por Capítulo CID — Top 10 Municípios\n(% do total de internações de venezuelanos no Oeste de SC)",
    fontsize=14,
    fontweight="bold",
    pad=15,
)
ax.set_xlabel("Percentual do total de internações no município (%)", fontsize=12)
ax.set_ylabel("")
ax.legend(title="Capítulo CID", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=9)
ax.set_xlim(0, 100)

# Adicionar rótulos de total no lado direito
for i, (mun, total) in enumerate(top10_mun.items()):
    ax.text(101, i, f"n={total}", va="center", fontsize=9, color="#333333")

plt.tight_layout()
fig.savefig(OUTPUT_FIGURES / "15_composicao_morbidade_municipios.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print(f"Salvo: {OUTPUT_FIGURES / '15_composicao_morbidade_municipios.png'}")

# ---------------------------------------------------------------------------
# 7. EVOLUÇÃO TEMPORAL — Top 5 CIDs (2018-2025)
# ---------------------------------------------------------------------------
top5_cids = top20_cids.head(5).index.tolist()

df_evo = df_oeste[df_oeste["DIAG_PRINC"].isin(top5_cids)].copy()
# Garantir que ano é numérico
df_evo["ano"] = pd.to_numeric(df_evo["ano"], errors="coerce")

# Agrupar por ano e CID
evo = df_evo.groupby(["ano", "DIAG_PRINC"]).size().unstack(fill_value=0)

# Garantir todos os anos no período
anos = range(2018, 2026)
evo = evo.reindex(anos, fill_value=0)

fig, ax = plt.subplots(figsize=(14, 7))
for cid in top5_cids:
    if cid in evo.columns:
        ax.plot(evo.index, evo[cid], marker="o", linewidth=2.5, markersize=7, label=cid)

ax.set_title(
    "Evolução dos 5 Principais CIDs de Internação — Venezuelanos no Oeste de SC",
    fontsize=14,
    fontweight="bold",
    pad=15,
)
ax.set_xlabel("Ano", fontsize=12)
ax.set_ylabel("Nº de internações", fontsize=12)
ax.set_xticks(anos)
ax.legend(title="CID Principal", loc="upper left")
ax.grid(True, alpha=0.3)

# Adicionar anotação do total geral
total_oeste = len(df_oeste)
ax.annotate(
    f"Total de internações no Oeste SC: {total_oeste:,}",
    xy=(0.98, 0.02),
    xycoords="axes fraction",
    ha="right",
    fontsize=10,
    color="#555555",
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#cccccc"),
)

plt.tight_layout()
fig.savefig(OUTPUT_FIGURES / "16_evolucao_top5_cids.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print(f"Salvo: {OUTPUT_FIGURES / '16_evolucao_top5_cids.png'}")

# ---------------------------------------------------------------------------
# 8. Relatório textual
# ---------------------------------------------------------------------------
report_path = OUTPUT_REPORTS / "top_cids_municipios_oeste_sc.txt"
with open(report_path, "w", encoding="utf-8") as f:
    f.write("=" * 70 + "\n")
    f.write("RELATÓRIO: TOP CIDs E MUNICÍPIOS — OESTE DE SANTA CATARINA\n")
    f.write("Projeto: migração venezuelana na Região Intermediária de Chapecó\n")
    f.write("Fonte: SIH/SUS (2018-2025)\n")
    f.write("=" * 70 + "\n\n")

    f.write(f"Total de internações no Oeste SC: {len(df_oeste):,}\n")
    f.write(f"Municípios do Oeste com registros: {df_oeste['MUNIC_RES_STR'].nunique()}\n")
    f.write(f"CIDs distintos: {df_oeste['DIAG_PRINC'].nunique()}\n\n")

    f.write("-" * 70 + "\n")
    f.write("TOP 20 CIDs (DIAG_PRINC) — FREQUÊNCIA ABSOLUTA\n")
    f.write("-" * 70 + "\n")
    for i, (cid, freq) in enumerate(top20_cids.items(), 1):
        pct = (freq / len(df_oeste)) * 100
        f.write(f"{i:2d}. {cid:8s} {freq:5d} internações  ({pct:5.2f}%)\n")

    f.write("\n" + "-" * 70 + "\n")
    f.write("TOP 15 MUNICÍPIOS — FREQUÊNCIA ABSOLUTA\n")
    f.write("-" * 70 + "\n")
    for i, (cod, freq) in enumerate(top15_mun.items(), 1):
        nome = MUNICIPIO_NOME.get(cod, cod)
        pct = (freq / len(df_oeste)) * 100
        f.write(f"{i:2d}. {nome:25s} ({cod}) {freq:5d} internações  ({pct:5.2f}%)\n")

    f.write("\n" + "-" * 70 + "\n")
    f.write("COMPOSIÇÃO POR CAPÍTULO CID (Top 10 municípios, % do município)\n")
    f.write("-" * 70 + "\n")
    cap_abs = pd.crosstab(df_cap["MUNIC_RES_STR"], df_cap["capitulo"])
    cap_abs = cap_abs.reindex(index=top10_mun.index)
    cap_abs.index = [MUNICIPIO_NOME.get(c, c) for c in cap_abs.index]
    f.write(cap_abs.to_string())

    f.write("\n\n" + "-" * 70 + "\n")
    f.write("EVOLUÇÃO TEMPORAL — TOP 5 CIDs (2018-2025)\n")
    f.write("-" * 70 + "\n")
    for cid in top5_cids:
        f.write(f"\n{cid}:\n")
        for ano in anos:
            val = evo.loc[ano, cid] if cid in evo.columns else 0
            f.write(f"  {ano}: {val}\n")

    f.write("\n" + "=" * 70 + "\n")
    f.write("FIM DO RELATÓRIO\n")
    f.write("=" * 70 + "\n")

print(f"Salvo: {report_path}")
print("\n✅ Todas as visualizações e o relatório foram gerados com sucesso.")
