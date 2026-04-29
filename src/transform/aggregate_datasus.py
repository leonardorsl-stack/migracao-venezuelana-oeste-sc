"""Agregação municipal dos dados DataSUS (SIM e SINASC) para a Região Oeste de SC.

Este módulo processa arquivos Parquet brutos do DataSUS, filtra municípios da
REGIAO_OESTE_SC e produz agregações por município/ano, além de indicadores
demográficos cruzados com população estimada do IBGE.

Example:
    >>> from src.transform.aggregate_datasus import run_all
    >>> run_all()
"""

from __future__ import annotations

import logging
from pathlib import Path

import polars as pl

from src.config import SETTINGS

logger = logging.getLogger(__name__)


def _get_codigos_oeste_6d() -> list[str]:
    """Retorna códigos IBGE de 6 dígitos dos municípios da Região Oeste de SC."""
    return [str(c)[:6] for c in SETTINGS.REGIAO_OESTE_SC]


def _parse_idade_datasus(idade_series: pl.Series) -> pl.Series:
    """Converte coluna IDADE do DataSIM para idade em anos completos.

    O formato do DataSUS usa o primeiro dígito como unidade e os demais como valor:
      - 0XX = minutos (considerado 0 anos)
      - 1XX = horas (considerado 0 anos)
      - 2XX = dias (considerado 0 anos)
      - 3XX = meses (considerado 0 anos, para fins de faixa etária infantil)
      - 4XX = anos
      - 5XX = 100+ anos

    Args:
        idade_series: Série Polars com os códigos de idade do DataSUS.

    Returns:
        Série Polars com idade em anos (inteiro).
    """
    # Garante string com 3 dígitos, preenchendo com zeros à esquerda
    idade_str = idade_series.cast(pl.Utf8).str.zfill(3)
    unidade = idade_str.str.slice(0, 1).cast(pl.Int32)
    valor = idade_str.str.slice(1, 2).cast(pl.Int32)

    return pl.when(unidade == 4).then(valor).when(unidade == 5).then(100 + valor).otherwise(0)


def _classifica_faixa_etaria(idade_anos: pl.Series) -> pl.Series:
    """Classifica idade em anos em faixas etárias padronizadas.

    Args:
        idade_anos: Série Polars com idade em anos.

    Returns:
        Série categórica com faixas etárias.
    """
    return (
        pl.when(idade_anos < 1)
        .then(pl.lit("0-1"))
        .when(idade_anos < 5)
        .then(pl.lit("1-4"))
        .when(idade_anos < 15)
        .then(pl.lit("5-14"))
        .when(idade_anos < 30)
        .then(pl.lit("15-29"))
        .when(idade_anos < 40)
        .then(pl.lit("30-39"))
        .when(idade_anos < 60)
        .then(pl.lit("40-59"))
        .otherwise(pl.lit("60+"))
    )


def _classifica_cid10_cap(causabas: pl.Series) -> pl.Series:
    """Extrai o capítulo CID-10 a partir dos 3 primeiros caracteres de CAUSABAS.

    Args:
        causabas: Série Polars com código CAUSABAS.

    Returns:
        Série com capítulo CID-10 (ex: 'C00-C97', 'I00-I99', etc.).
    """
    cod = causabas.str.to_uppercase().str.slice(0, 3)
    letra = cod.str.slice(0, 1)
    num_str = cod.str.slice(1, 2).cast(pl.Int32, strict=False)
    num = pl.when(num_str.is_null()).then(-1).otherwise(num_str)

    return (
        pl.when((letra == "A") | (letra == "B"))
        .then(pl.lit("A00-B99"))
        .when((letra == "C") | ((letra == "D") & (num >= 0) & (num <= 4)))
        .then(pl.lit("C00-D48"))
        .when((letra == "D") & (num >= 5) & (num <= 8))
        .then(pl.lit("D50-D89"))
        .when(letra == "E")
        .then(pl.lit("E00-E90"))
        .when(letra == "F")
        .then(pl.lit("F00-F99"))
        .when(letra == "G")
        .then(pl.lit("G00-G99"))
        .when(letra == "H")
        .then(pl.lit("H00-H59"))
        .when(letra == "I")
        .then(pl.lit("I00-I99"))
        .when(letra == "J")
        .then(pl.lit("J00-J99"))
        .when(letra == "K")
        .then(pl.lit("K00-K93"))
        .when(letra == "L")
        .then(pl.lit("L00-L99"))
        .when(letra == "M")
        .then(pl.lit("M00-M99"))
        .when(letra == "N")
        .then(pl.lit("N00-N99"))
        .when(letra == "O")
        .then(pl.lit("O00-O99"))
        .when(letra == "P")
        .then(pl.lit("P00-P96"))
        .when(letra == "Q")
        .then(pl.lit("Q00-Q99"))
        .when(letra == "R")
        .then(pl.lit("R00-R99"))
        .when((letra == "S") | (letra == "T"))
        .then(pl.lit("S00-T98"))
        .when((letra == "V") | (letra == "W") | (letra == "X") | (letra == "Y"))
        .then(pl.lit("V01-Y98"))
        .when(letra == "Z")
        .then(pl.lit("Z00-Z99"))
        .otherwise(pl.lit("OUTROS"))
    )


def _extrai_ano_datasus(data_series: pl.Series) -> pl.Series:
    """Extrai o ano de uma data no formato DDMMAAAA ou similar.

    Assume que os 4 últimos caracteres representam o ano.

    Args:
        data_series: Série com datas como string.

    Returns:
        Série Int32 com o ano.
    """
    return data_series.cast(pl.Utf8).str.slice(-4).cast(pl.Int32)


# ───────────────────────────────────────────────────────────────
# SIM
# ───────────────────────────────────────────────────────────────

def process_sim(
    raw_dir: Path | None = None,
    output_path: Path | None = None,
) -> pl.DataFrame:
    """Processa arquivos DO_SC_*.parquet (óbitos) e gera agregação municipal.

    Filtros aplicados:
      - CODMUNRES nos primeiros 6 dígitos da REGIAO_OESTE_SC.
      - Ano extraído de DTOBITO entre 2018 e 2023.

    Agregações:
      - total_obitos
      - obitos_masculino, obitos_feminino, obitos_sexo_ignorado
      - obitos por faixa etária (0-1, 1-4, 5-14, 15-29, 30-39, 40-59, 60+)
      - obitos por capítulo CID-10 (top causas)

    Args:
        raw_dir: Diretório com os arquivos DO_SC_*.parquet.
        output_path: Caminho para salvar o resultado (Parquet).

    Returns:
        DataFrame Polars com agregação por município e ano.
    """
    if raw_dir is None:
        raw_dir = SETTINGS.DATA_RAW / "datasus" / "SIM"
    if output_path is None:
        output_path = SETTINGS.DATA_PROCESSED / "datasus" / "sim_agregado_oeste_sc.parquet"

    codigos_oeste = _get_codigos_oeste_6d()
    arquivos = sorted(raw_dir.glob("DO_SC_20*.parquet"))

    if not arquivos:
        raise FileNotFoundError(f"Nenhum arquivo DO_SC_*.parquet encontrado em {raw_dir}")

    logger.info("Processando %d arquivos SIM...", len(arquivos))

    partes: list[pl.DataFrame] = []
    for arq in arquivos:
        df = pl.read_parquet(arq)
        # Padroniza CODMUNRES para 6 dígitos
        df = df.with_columns(pl.col("CODMUNRES").cast(pl.Utf8).str.zfill(6).alias("CODMUNRES_6"))
        # Filtra municípios da região Oeste
        df = df.filter(pl.col("CODMUNRES_6").is_in(codigos_oeste))
        if df.is_empty():
            continue
        # Extrai ano
        df = df.with_columns(_extrai_ano_datasus(pl.col("DTOBITO")).alias("ano"))
        # Calcula idade em anos
        df = df.with_columns(_parse_idade_datasus(pl.col("IDADE")).alias("idade_anos"))
        # Faixa etária
        df = df.with_columns(_classifica_faixa_etaria(pl.col("idade_anos")).alias("faixa_etaria"))
        # Capítulo CID-10
        df = df.with_columns(_classifica_cid10_cap(pl.col("CAUSABAS")).alias("cap_cid10"))
        partes.append(df)

    if not partes:
        raise ValueError("Nenhum registro SIM encontrado para a Região Oeste de SC.")

    df_all = pl.concat(partes, how="diagonal")

    # ── agregações ──
    agg_total = df_all.group_by(["CODMUNRES_6", "ano"]).agg(pl.len().alias("total_obitos"))

    agg_sexo = (
        df_all.with_columns(
            pl.when(pl.col("SEXO") == "1")
            .then(1)
            .when(pl.col("SEXO") == "2")
            .then(2)
            .otherwise(0)
            .alias("sexo_pad")
        )
        .group_by(["CODMUNRES_6", "ano"])
        .agg(
            pl.col("sexo_pad").eq(1).sum().alias("obitos_masculino"),
            pl.col("sexo_pad").eq(2).sum().alias("obitos_feminino"),
            pl.col("sexo_pad").eq(0).sum().alias("obitos_sexo_ignorado"),
        )
    )

    agg_faixa = (
        df_all.group_by(["CODMUNRES_6", "ano", "faixa_etaria"])
        .agg(pl.len().alias("n"))
        .pivot(values="n", index=["CODMUNRES_6", "ano"], on="faixa_etaria", aggregate_function="sum")
        .fill_null(0)
    )
    # Renomeia colunas de faixa etária para prefixo obitos_
    for col in agg_faixa.columns:
        if col not in ("CODMUNRES_6", "ano"):
            agg_faixa = agg_faixa.rename({col: f"obitos_faixa_{col}"})

    agg_causas = (
        df_all.group_by(["CODMUNRES_6", "ano", "cap_cid10"])
        .agg(pl.len().alias("n"))
        .sort(["CODMUNRES_6", "ano", "n"], descending=[False, False, True])
        .group_by(["CODMUNRES_6", "ano"])
        .agg(pl.col("cap_cid10").head(3).alias("top3_causas"), pl.col("n").head(3).alias("top3_causas_n"))
    )

    # Junta tudo
    resultado = agg_total.join(agg_sexo, on=["CODMUNRES_6", "ano"], how="left")
    resultado = resultado.join(agg_faixa, on=["CODMUNRES_6", "ano"], how="left")
    resultado = resultado.join(agg_causas, on=["CODMUNRES_6", "ano"], how="left")

    # Mapeia código 6 -> 7 dígitos e nome do município
    mapa_codigos = {str(c)[:6]: {"codigo_7": str(c), "nome": nome} for c, nome in zip(SETTINGS.REGIAO_OESTE_SC, _nomes_municipios(), strict=False)}
    resultado = resultado.with_columns(
        pl.col("CODMUNRES_6").replace({k: v["codigo_7"] for k, v in mapa_codigos.items()}).alias("codigo_ibge_7d"),
        pl.col("CODMUNRES_6").replace({k: v["nome"] for k, v in mapa_codigos.items()}).alias("municipio"),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    resultado.write_parquet(output_path, compression="zstd")
    logger.info("SIM agregado salvo em %s (%d registros)", output_path, resultado.height)
    return resultado


# ───────────────────────────────────────────────────────────────
# SINASC
# ───────────────────────────────────────────────────────────────

def process_sinasc(
    raw_dir: Path | None = None,
    output_path: Path | None = None,
) -> pl.DataFrame:
    """Processa arquivos DN_SC_*.parquet (nascimentos) e gera agregação municipal.

    Filtros aplicados:
      - CODMUNRES nos primeiros 6 dígitos da REGIAO_OESTE_SC.
      - Ano extraído de DTNASC entre 2018 e 2022 (2023 está corrompido/vazio).

    Agregações:
      - total_nascimentos
      - nascimentos_masculino, nascimentos_feminino, nascimentos_sexo_ignorado
      - nascimentos_peso_baixo (< 2500g)
      - nascimentos_peso_normal (2500g+)
      - nascimentos_mae_adolescente (< 20 anos)
      - partos_cesarea, partos_normal, partos_ignorado

    Args:
        raw_dir: Diretório com os arquivos DN_SC_*.parquet.
        output_path: Caminho para salvar o resultado (Parquet).

    Returns:
        DataFrame Polars com agregação por município e ano.
    """
    if raw_dir is None:
        raw_dir = SETTINGS.DATA_RAW / "datasus" / "SINASC"
    if output_path is None:
        output_path = SETTINGS.DATA_PROCESSED / "datasus" / "sinasc_agregado_oeste_sc.parquet"

    codigos_oeste = _get_codigos_oeste_6d()
    arquivos = sorted(raw_dir.glob("DN_SC_20*.parquet"))

    logger.info("Processando %d arquivos SINASC...", len(arquivos))

    partes: list[pl.DataFrame] = []
    for arq in arquivos:
        # Pula arquivo corrompido de 2023
        if "2023" in arq.name:
            logger.warning("Pulando arquivo corrompido: %s", arq.name)
            continue

        df = pl.read_parquet(arq)
        # Padroniza CODMUNRES
        df = df.with_columns(pl.col("CODMUNRES").cast(pl.Utf8).str.zfill(6).alias("CODMUNRES_6"))
        df = df.filter(pl.col("CODMUNRES_6").is_in(codigos_oeste))
        if df.is_empty():
            continue
        # Extrai ano
        df = df.with_columns(_extrai_ano_datasus(pl.col("DTNASC")).alias("ano"))
        # Padroniza sexo
        df = df.with_columns(
            pl.when(pl.col("SEXO") == "1")
            .then(1)
            .when(pl.col("SEXO") == "2")
            .then(2)
            .otherwise(0)
            .alias("sexo_pad")
        )
        # Peso ao nascer
        df = df.with_columns(pl.col("PESO").cast(pl.Float64, strict=False).fill_null(0).alias("peso_num"))
        # Idade da mãe
        df = df.with_columns(pl.col("IDADEMAE").cast(pl.Int32, strict=False).fill_null(-1).alias("idademaen_num"))
        # Tipo de parto
        df = df.with_columns(
            pl.when(pl.col("PARTO") == "1")
            .then(pl.lit("normal"))
            .when(pl.col("PARTO") == "2")
            .then(pl.lit("cesarea"))
            .otherwise(pl.lit("ignorado"))
            .alias("parto_pad")
        )
        partes.append(df)

    if not partes:
        raise ValueError("Nenhum registro SINASC encontrado para a Região Oeste de SC.")

    df_all = pl.concat(partes, how="diagonal")

    # ── agregações ──
    agg_total = df_all.group_by(["CODMUNRES_6", "ano"]).agg(pl.len().alias("total_nascimentos"))

    agg_sexo = df_all.group_by(["CODMUNRES_6", "ano"]).agg(
        pl.col("sexo_pad").eq(1).sum().alias("nascimentos_masculino"),
        pl.col("sexo_pad").eq(2).sum().alias("nascimentos_feminino"),
        pl.col("sexo_pad").eq(0).sum().alias("nascimentos_sexo_ignorado"),
    )

    agg_peso = df_all.group_by(["CODMUNRES_6", "ano"]).agg(
        pl.col("peso_num").lt(2500).sum().alias("nascimentos_peso_baixo"),
        pl.col("peso_num").ge(2500).sum().alias("nascimentos_peso_normal"),
    )

    agg_mae = df_all.group_by(["CODMUNRES_6", "ano"]).agg(
        pl.col("idademaen_num").lt(20).sum().alias("nascimentos_mae_adolescente"),
    )

    agg_parto = (
        df_all.group_by(["CODMUNRES_6", "ano", "parto_pad"])
        .agg(pl.len().alias("n"))
        .pivot(values="n", index=["CODMUNRES_6", "ano"], on="parto_pad", aggregate_function="sum")
        .fill_null(0)
        .rename({"cesarea": "partos_cesarea", "normal": "partos_normal", "ignorado": "partos_ignorado"})
    )

    resultado = agg_total.join(agg_sexo, on=["CODMUNRES_6", "ano"], how="left")
    resultado = resultado.join(agg_peso, on=["CODMUNRES_6", "ano"], how="left")
    resultado = resultado.join(agg_mae, on=["CODMUNRES_6", "ano"], how="left")
    resultado = resultado.join(agg_parto, on=["CODMUNRES_6", "ano"], how="left")

    # Mapeia código 6 -> 7 dígitos e nome
    mapa_codigos = {str(c)[:6]: {"codigo_7": str(c), "nome": nome} for c, nome in zip(SETTINGS.REGIAO_OESTE_SC, _nomes_municipios(), strict=False)}
    resultado = resultado.with_columns(
        pl.col("CODMUNRES_6").replace({k: v["codigo_7"] for k, v in mapa_codigos.items()}).alias("codigo_ibge_7d"),
        pl.col("CODMUNRES_6").replace({k: v["nome"] for k, v in mapa_codigos.items()}).alias("municipio"),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    resultado.write_parquet(output_path, compression="zstd")
    logger.info("SINASC agregado salvo em %s (%d registros)", output_path, resultado.height)
    return resultado


# ───────────────────────────────────────────────────────────────
# População estimada
# ───────────────────────────────────────────────────────────────

def _carrega_populacao() -> pl.DataFrame:
    """Carrega e prepara população estimada do IBGE para a Região Oeste de SC.

    Como os dados não possuem 2023, realiza interpolação linear entre 2022 e 2024.

    Returns:
        DataFrame com colunas: codigo_ibge_7d, ano, populacao.
    """
    path = SETTINGS.DATA_RAW / "ibge" / "populacao_estimada_2018_2024.parquet"
    codigos_7 = [str(c) for c in SETTINGS.REGIAO_OESTE_SC]

    df = pl.read_parquet(path)
    df = df.filter(pl.col("municipio_codigo").is_in(codigos_7))
    df = df.select([
        pl.col("municipio_codigo").alias("codigo_ibge_7d"),
        pl.col("ano").cast(pl.Int32),
        pl.col("populacao").cast(pl.Float64),
    ])

    # Gera 2023 via interpolação linear
    df_2022 = df.filter(pl.col("ano") == 2022).select(["codigo_ibge_7d", pl.col("populacao").alias("pop_2022")])
    df_2024 = df.filter(pl.col("ano") == 2024).select(["codigo_ibge_7d", pl.col("populacao").alias("pop_2024")])

    df_interp = df_2022.join(df_2024, on="codigo_ibge_7d", how="inner")
    df_interp = df_interp.with_columns(
        ((pl.col("pop_2022") + pl.col("pop_2024")) / 2).alias("populacao")
    ).with_columns(pl.lit(2023).cast(pl.Int32).alias("ano"))
    df_interp = df_interp.select(["codigo_ibge_7d", "ano", "populacao"])

    df = pl.concat([df, df_interp], how="vertical")
    return df.filter(pl.col("ano").is_between(2018, 2023))


# ───────────────────────────────────────────────────────────────
# Indicadores demográficos
# ───────────────────────────────────────────────────────────────

def process_indicadores(
    sim_path: Path | None = None,
    sinasc_path: Path | None = None,
    output_path: Path | None = None,
) -> pl.DataFrame:
    """Calcula indicadores demográficos cruzando SIM, SINASC e população IBGE.

    Indicadores calculados:
      - taxa_bruta_mortalidade (óbitos / população * 1000)
      - taxa_bruta_natalidade (nascimentos / população * 1000)
      - taxa_mortalidade_infantil (< 1 ano / nascimentos vivos * 1000)

    Args:
        sim_path: Parquet agregado do SIM.
        sinasc_path: Parquet agregado do SINASC.
        output_path: Caminho para salvar o resultado.

    Returns:
        DataFrame Polars com indicadores por município e ano.
    """
    if sim_path is None:
        sim_path = SETTINGS.DATA_PROCESSED / "datasus" / "sim_agregado_oeste_sc.parquet"
    if sinasc_path is None:
        sinasc_path = SETTINGS.DATA_PROCESSED / "datasus" / "sinasc_agregado_oeste_sc.parquet"
    if output_path is None:
        output_path = SETTINGS.DATA_PROCESSED / "indicadores_demograficos_oeste_sc.parquet"

    df_sim = pl.read_parquet(sim_path)
    df_sin = pl.read_parquet(sinasc_path)
    df_pop = _carrega_populacao()

    # Cruza SIM + população
    df_ind = df_sim.join(df_pop, left_on=["codigo_ibge_7d", "ano"], right_on=["codigo_ibge_7d", "ano"], how="left")
    # Cruza SINASC
    df_ind = df_ind.join(df_sin, left_on=["codigo_ibge_7d", "ano"], right_on=["codigo_ibge_7d", "ano"], how="left", suffix="_sinasc")

    # Renomeia colunas duplicadas de município
    if "municipio_sinasc" in df_ind.columns:
        df_ind = df_ind.drop("municipio_sinasc")
    if "CODMUNRES_6_sinasc" in df_ind.columns:
        df_ind = df_ind.drop("CODMUNRES_6_sinasc")

    # Calcula indicadores
    df_ind = df_ind.with_columns(
        (pl.col("total_obitos") / pl.col("populacao") * 1000).round(3).alias("taxa_bruta_mortalidade"),
        (pl.col("total_nascimentos") / pl.col("populacao") * 1000).round(3).alias("taxa_bruta_natalidade"),
        pl.when(pl.col("total_nascimentos") > 0)
        .then((pl.col("obitos_faixa_0-1") / pl.col("total_nascimentos") * 1000).round(3))
        .otherwise(None)
        .alias("taxa_mortalidade_infantil"),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_ind.write_parquet(output_path, compression="zstd")
    logger.info("Indicadores demográficos salvos em %s (%d registros)", output_path, df_ind.height)
    return df_ind


# ───────────────────────────────────────────────────────────────
# Utilitários
# ───────────────────────────────────────────────────────────────

NOMES_MUNICIPIOS: dict[int, str] = {
    4204202: "Chapecó",
    4204301: "Concórdia",
    4216800: "Seara",
    4217204: "São Miguel do Oeste",
    4207684: "Itapiranga",
    4206652: "Guatambú",
    4219507: "Xanxerê",
    4209003: "Joaçaba",
    4206702: "Herval d'Oeste",
    4219705: "Xaxim",
    4203808: "Cunha Porã",
    4204004: "Cunhataí",
    4206405: "Guaraciaba",
    4208906: "Jupiá",
    4216107: "Riqueza",
    4219358: "Vargeão",
    4201273: "Águas de Chapecó",
    4204152: "Bom Jesus do Oeste",
    4204400: "Coronel Freitas",
    4205431: "Caxambu do Sul",
}


def _nomes_municipios() -> list[str]:
    """Retorna nomes dos municípios na mesma ordem de REGIAO_OESTE_SC."""
    return [NOMES_MUNICIPIOS[c] for c in SETTINGS.REGIAO_OESTE_SC]


# ───────────────────────────────────────────────────────────────
# Orquestrador
# ───────────────────────────────────────────────────────────────

def run_all() -> tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame]:
    """Executa todo o pipeline de agregação DataSUS.

    Returns:
        Tupla com (DataFrame SIM, DataFrame SINASC, DataFrame indicadores).
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    df_sim = process_sim()
    df_sin = process_sinasc()
    df_ind = process_indicadores()
    return df_sim, df_sin, df_ind


if __name__ == "__main__":
    run_all()
