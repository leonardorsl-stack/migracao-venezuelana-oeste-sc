"""
Gera painel longitudinal consolidado (município × ano) para a Região Oeste de SC,
combinando dados de população (IBGE), vínculos empregatícios (RAIS) e internações
hospitalares (SIH/SUS) de venezuelanos, além dos indicadores antigos (SIM/SINASC).

Saídas:
    - data/processed/painel_oeste_sc_2018_2024.parquet
    - data/processed/painel_oeste_sc_2018_2024.csv
    - output/resumo_painel_longitudinal.md
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Adiciona src/ ao path para importar config
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from config import SETTINGS  # noqa: E402


def main() -> None:
    # ------------------------------------------------------------------
    # 1. Esqueleto do painel: 109 municípios × 7 anos (2018-2024)
    # ------------------------------------------------------------------
    codigos_7d = sorted(SETTINGS.REGIAO_OESTE_SC)
    codigos_6d = [int(str(c)[:6]) for c in codigos_7d]
    anos = list(range(2018, 2025))

    esqueleto = pd.DataFrame(
        [(c7, c6, a) for c7, c6 in zip(codigos_7d, codigos_6d, strict=False) for a in anos],
        columns=["codigo_ibge_7d", "codigo_ibge_6d", "ano"],
    )

    # Nome do município virá do IBGE; criamos mapping a partir do parquet de população
    pop = pd.read_parquet(SETTINGS.DATA_PROCESSED / "ibge_populacao_estimada_oeste_sc.parquet")
    nome_map = (
        pop.groupby("codigo_ibge_7d")["municipio"]
        .first()
        .to_dict()
    )
    esqueleto["municipio"] = esqueleto["codigo_ibge_7d"].map(nome_map)

    # ------------------------------------------------------------------
    # 2. População IBGE
    # ------------------------------------------------------------------
    pop = pop.rename(columns={"populacao": "populacao_total"})
    painel = esqueleto.merge(
        pop[["codigo_ibge_7d", "ano", "populacao_total"]],
        on=["codigo_ibge_7d", "ano"],
        how="left",
    )

    # ------------------------------------------------------------------
    # 3. RAIS – vínculos empregatícios de venezuelanos
    # ------------------------------------------------------------------
    rais_frames = []
    for ano in anos:
        arquivo = SETTINGS.DATA_PROCESSED / f"rais_vinculos_sc_venezuela_{ano}.parquet"
        if not arquivo.exists():
            continue
        df = pd.read_parquet(arquivo)
        # municipio na RAIS é string de 6 dígitos
        df["codigo_ibge_6d"] = df["municipio"].astype(int)
        contagem = (
            df.groupby("codigo_ibge_6d")
            .size()
            .reset_index(name="total_vinculos_rais")
        )
        contagem["ano"] = ano
        rais_frames.append(contagem)

    if rais_frames:
        rais_agg = pd.concat(rais_frames, ignore_index=True)
        painel = painel.merge(
            rais_agg, on=["codigo_ibge_6d", "ano"], how="left"
        )
    else:
        painel["total_vinculos_rais"] = np.nan

    painel["total_vinculos_rais"] = painel["total_vinculos_rais"].fillna(0).astype(int)

    # ------------------------------------------------------------------
    # 4. SIH/SUS – internações de venezuelanos
    # ------------------------------------------------------------------
    sih = pd.read_parquet(
        SETTINGS.DATA_RAW / "datasus" / "sih_sus_sc_venezuela_2018_2025.parquet"
    )
    sih = sih[sih["ano"].isin(anos)].copy()
    # Remove duplicatas de N_AIH para evitar contagem dupla de internações
    sih = sih.drop_duplicates(subset="N_AIH", keep="first")
    sih["codigo_ibge_6d"] = sih["MUNIC_RES"].astype(int)

    sih_agg = (
        sih.groupby(["codigo_ibge_6d", "ano"])
        .agg(
            total_internacoes_sih=("N_AIH", "count"),
            dias_permanencia_sih=("DIAS_PERM", "sum"),
            valor_total_sih=("VAL_TOT", "sum"),
            obitos_hospitalares_sih=("MORTE", lambda x: (x == 1).sum()),
        )
        .reset_index()
    )

    painel = painel.merge(
        sih_agg, on=["codigo_ibge_6d", "ano"], how="left"
    )
    for col in [
        "total_internacoes_sih",
        "dias_permanencia_sih",
        "obitos_hospitalares_sih",
    ]:
        painel[col] = painel[col].fillna(0).astype(int)
    painel["valor_total_sih"] = painel["valor_total_sih"].fillna(0.0)

    # ------------------------------------------------------------------
    # 5. Indicadores antigos (SIM/SINASC) – merge com painel 2018-2023
    # ------------------------------------------------------------------
    painel_antigo = pd.read_parquet(
        SETTINGS.DATA_PROCESSED / "painel_oeste_sc_2018_2023.parquet"
    )
    painel = painel.merge(
        painel_antigo[
            [
                "codigo_ibge_7d",
                "ano",
                "total_obitos",
                "total_nascimentos",
                "taxa_mortalidade",
                "taxa_natalidade",
            ]
        ],
        on=["codigo_ibge_7d", "ano"],
        how="left",
    )

    # ------------------------------------------------------------------
    # 6. Garantir NaN para anos sem dados SINASC/SIM
    # ------------------------------------------------------------------
    # SINASC só tem dados até 2022; SIM só tem dados até 2023
    painel.loc[painel["ano"] >= 2023, "total_nascimentos"] = pd.NA
    painel.loc[painel["ano"] >= 2023, "taxa_natalidade"] = pd.NA
    painel.loc[painel["ano"] >= 2024, "total_obitos"] = pd.NA
    painel.loc[painel["ano"] >= 2024, "taxa_mortalidade"] = pd.NA

    # ------------------------------------------------------------------
    # 7. Taxas por mil habitantes
    # ------------------------------------------------------------------
    pop_safe = painel["populacao_total"].replace(0, pd.NA)

    painel["taxa_vinculos_por_mil"] = (
        painel["total_vinculos_rais"] / pop_safe * 1000
    ).round(4)
    painel["taxa_internacoes_por_mil"] = (
        painel["total_internacoes_sih"] / pop_safe * 1000
    ).round(4)

    # ------------------------------------------------------------------
    # 8. Reordenar colunas
    # ------------------------------------------------------------------
    colunas = [
        "codigo_ibge_7d",
        "codigo_ibge_6d",
        "municipio",
        "ano",
        "populacao_total",
        "total_vinculos_rais",
        "total_internacoes_sih",
        "dias_permanencia_sih",
        "valor_total_sih",
        "obitos_hospitalares_sih",
        "taxa_vinculos_por_mil",
        "taxa_internacoes_por_mil",
        "total_obitos",
        "total_nascimentos",
        "taxa_mortalidade",
        "taxa_natalidade",
    ]
    painel = painel[colunas]

    # ------------------------------------------------------------------
    # 9. Salvar
    # ------------------------------------------------------------------
    painel.to_parquet(
        SETTINGS.DATA_PROCESSED / "painel_oeste_sc_2018_2024.parquet",
        compression="zstd",
        index=False,
    )
    painel.to_csv(
        SETTINGS.DATA_PROCESSED / "painel_oeste_sc_2018_2024.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # ------------------------------------------------------------------
    # 10. Relatório Markdown
    # ------------------------------------------------------------------
    output_dir = PROJECT_ROOT / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Top 10 municípios por vínculos RAIS em 2024
    top_vinc = (
        painel[painel["ano"] == 2024]
        .nlargest(10, "total_vinculos_rais")[
            ["municipio", "total_vinculos_rais", "taxa_vinculos_por_mil"]
        ]
        .reset_index(drop=True)
    )
    top_vinc.index = top_vinc.index + 1

    # Top 10 municípios por internações SIH em 2024
    top_int = (
        painel[painel["ano"] == 2024]
        .nlargest(10, "total_internacoes_sih")[
            ["municipio", "total_internacoes_sih", "taxa_internacoes_por_mil"]
        ]
        .reset_index(drop=True)
    )
    top_int.index = top_int.index + 1

    # Evolução temporal – taxa de vínculos por mil na região
    evo = (
        painel.groupby("ano")
        .apply(
            lambda df: pd.Series(
                {
                    "vinculos": df["total_vinculos_rais"].sum(),
                    "populacao": df["populacao_total"].sum(),
                    "taxa_vinculos_por_mil": (
                        df["total_vinculos_rais"].sum()
                        / df["populacao_total"].sum()
                        * 1000
                    ),
                }
            ),
            include_groups=False,
        )
        .reset_index()
    )

    # Municípios com maior concentração relativa (taxa_vinculos_por_mil) em 2024
    top_conc = (
        painel[painel["ano"] == 2024]
        .nlargest(10, "taxa_vinculos_por_mil")[
            ["municipio", "total_vinculos_rais", "populacao_total", "taxa_vinculos_por_mil"]
        ]
        .reset_index(drop=True)
    )
    top_conc.index = top_conc.index + 1

    md = f"""# Resumo do Painel Longitudinal – Oeste SC (2018-2024)

## Geral
- **Total de registros:** {len(painel):,}
- **Municípios:** {painel['codigo_ibge_7d'].nunique()}
- **Anos:** {painel['ano'].min()}–{painel['ano'].max()}
- **Vínculos RAIS (2018-2024):** {painel['total_vinculos_rais'].sum():,}
- **Internações SIH (2018-2024):** {painel['total_internacoes_sih'].sum():,}
- **Óbitos hospitalares SIH (2018-2024):** {painel['obitos_hospitalares_sih'].sum():,}

## Top 10 Municípios – Vínculos RAIS (2024)

{top_vinc.to_markdown()}

## Top 10 Municípios – Internações SIH (2024)

{top_int.to_markdown()}

## Evolução Temporal – Taxa de Vínculos por Mil Habitantes (Região Oeste)

{evo.to_markdown(index=False)}

## Maior Concentração Relativa – Taxa de Vínculos por Mil (2024)

{top_conc.to_markdown()}

## Notas Metodológicas
- A taxa é calculada como `(indicador / população total) × 1.000`.
- Municípios sem vínculos ou internações aparecem com valor zero (não ausente) para essas variáveis.
- Dados de óbitos gerais (`total_obitos`) e nascimentos (`total_nascimentos`) estão disponíveis até 2023 (SIM) e 2022 (SINASC), respectivamente, conforme limitação das bases originais.
- O arquivo consolidado está disponível em:
  - `data/processed/painel_oeste_sc_2018_2024.parquet` (compressão zstd)
  - `data/processed/painel_oeste_sc_2018_2024.csv`
"""

    (output_dir / "resumo_painel_longitudinal.md").write_text(md, encoding="utf-8")
    print("Painel e relatório gerados com sucesso.")


if __name__ == "__main__":
    main()
