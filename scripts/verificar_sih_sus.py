#!/usr/bin/env python3
"""Verificacao rapida da integridade dos dados SIH/SUS."""

import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from config import SETTINGS

DATA_DIR = Path("/Users/leonardosantos/Documents/raio_x_migraçao/data/raw/datasus")


def main() -> None:
    df = pd.read_parquet(DATA_DIR / "sih_sus_sc_venezuela_2018_2025.parquet")

    assert (
        df["NACIONAL"].astype(str).str.strip().eq("092").all()
    ), "FALHA: NACIONAL inconsistente"
    assert df.duplicated().sum() == 0, "FALHA: Duplicatas totais encontradas"

    codigos_oeste_6d = [int(str(c)[:6]) for c in SETTINGS.REGIAO_OESTE_SC]
    df["mun_res_num"] = pd.to_numeric(df["MUNIC_RES"], errors="coerce")
    oeste = df[df["mun_res_num"].isin(codigos_oeste_6d)]

    print(f"Total SC: {len(df):,}")
    print(f"Total Oeste SC: {len(oeste):,} ({len(oeste)/len(df)*100:.1f}%)")
    print(f"Municipios Oeste com registros: {oeste['MUNIC_RES'].nunique()}")
    print(f"N_AIH duplicados: {len(df) - df['N_AIH'].nunique()}")
    print("✅ Verificacao concluida com sucesso")


if __name__ == "__main__":
    main()
