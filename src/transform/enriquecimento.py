"""Funções de enriquecimento de dados para análise de migração.

Este módulo adiciona variáveis derivadas aos datasets processados,
como classificações de microrregião, setores econômicos (CNAE),
faixas etárias e índices compostos.

Example:
    >>> from src.transform.enriquecimento import cut_age_bins, cnae_to_sector
    >>> df["faixa_etaria"] = cut_age_bins(df["idade"])
    >>> df["setor"] = df["cnae"].apply(cnae_to_sector)
"""

from __future__ import annotations

import logging
from collections.abc import Sequence

import pandas as pd

logger = logging.getLogger(__name__)

# Mapeamento CNAE 2.0 -> setores agregados (nível seção)
_CNAE_SECAO_MAP: dict[str, str] = {
    "01": "Agricultura, pecuária, produção florestal, pesca e aquicultura",
    "02": "Agricultura, pecuária, produção florestal, pesca e aquicultura",
    "03": "Agricultura, pecuária, produção florestal, pesca e aquicultura",
    "05": "Indústrias extrativas",
    "06": "Indústrias extrativas",
    "07": "Indústrias extrativas",
    "08": "Indústrias extrativas",
    "09": "Indústrias extrativas",
    "10": "Indústrias de transformação",
    "11": "Indústrias de transformação",
    "12": "Indústrias de transformação",
    "13": "Indústrias de transformação",
    "14": "Indústrias de transformação",
    "15": "Indústrias de transformação",
    "16": "Indústrias de transformação",
    "17": "Indústrias de transformação",
    "18": "Indústrias de transformação",
    "19": "Indústrias de transformação",
    "20": "Indústrias de transformação",
    "21": "Indústrias de transformação",
    "22": "Indústrias de transformação",
    "23": "Indústrias de transformação",
    "24": "Indústrias de transformação",
    "25": "Indústrias de transformação",
    "26": "Indústrias de transformação",
    "27": "Indústrias de transformação",
    "28": "Indústrias de transformação",
    "29": "Indústrias de transformação",
    "30": "Indústrias de transformação",
    "31": "Indústrias de transformação",
    "32": "Indústrias de transformação",
    "33": "Indústrias de transformação",
    "35": "Eletricidade e gás",
    "36": "Água, esgoto, atividades de gestão de resíduos",
    "37": "Água, esgoto, atividades de gestão de resíduos",
    "38": "Água, esgoto, atividades de gestão de resíduos",
    "39": "Água, esgoto, atividades de gestão de resíduos",
    "41": "Construção",
    "42": "Construção",
    "43": "Construção",
    "45": "Comércio; reparação de veículos automotores",
    "46": "Comércio; reparação de veículos automotores",
    "47": "Comércio; reparação de veículos automotores",
    "49": "Transporte, armazenagem e correio",
    "50": "Transporte, armazenagem e correio",
    "51": "Transporte, armazenagem e correio",
    "52": "Transporte, armazenagem e correio",
    "53": "Transporte, armazenagem e correio",
    "55": "Alojamento e alimentação",
    "56": "Alojamento e alimentação",
    "58": "Informação e comunicação",
    "59": "Informação e comunicação",
    "60": "Informação e comunicação",
    "61": "Informação e comunicação",
    "62": "Informação e comunicação",
    "63": "Informação e comunicação",
    "64": "Atividades financeiras, de seguros e serviços relacionados",
    "65": "Atividades financeiras, de seguros e serviços relacionados",
    "66": "Atividades financeiras, de seguros e serviços relacionados",
    "68": "Atividades imobiliárias",
    "69": "Atividades profissionais, científicas e técnicas",
    "70": "Atividades profissionais, científicas e técnicas",
    "71": "Atividades profissionais, científicas e técnicas",
    "72": "Atividades profissionais, científicas e técnicas",
    "73": "Atividades profissionais, científicas e técnicas",
    "74": "Atividades profissionais, científicas e técnicas",
    "75": "Atividades administrativas e serviços complementares",
    "77": "Atividades administrativas e serviços complementares",
    "78": "Atividades administrativas e serviços complementares",
    "79": "Atividades administrativas e serviços complementares",
    "80": "Atividades administrativas e serviços complementares",
    "81": "Atividades administrativas e serviços complementares",
    "82": "Atividades administrativas e serviços complementares",
    "84": "Administração pública, defesa e seguridade social",
    "85": "Educação",
    "86": "Saúde humana e serviços sociais",
    "87": "Saúde humana e serviços sociais",
    "88": "Saúde humana e serviços sociais",
    "90": "Artes, cultura, esporte e recreação",
    "91": "Artes, cultura, esporte e recreação",
    "92": "Artes, cultura, esporte e recreação",
    "93": "Artes, cultura, esporte e recreação",
    "94": "Outras atividades de serviços",
    "95": "Outras atividades de serviços",
    "96": "Outras atividades de serviços",
    "97": "Serviços domésticos",
    "99": "Organismos internacionais e outras instituições extraterritoriais",
}

# Microrregiões do Oeste de SC (codigos IBGE das microrregiões)
_MICROREGIAO_MAP: dict[str, str] = {
    "42001": "Chapecó",
    "42002": "Concórdia",
    "42003": "Joaçaba",
    "42004": "São Miguel do Oeste",
    "42005": "Xanxerê",
}

# Mapeamento município -> microrregião (simplificado; parcial)
_MUN_TO_MICRO: dict[int, str] = {
    4204202: "Chapecó",
    4204301: "Concórdia",
    4216800: "Seara",
    4217250: "São Miguel do Oeste",
    4207684: "Itapiranga",
    4206607: "Guatambú",
    4219507: "Xanxerê",
    4209003: "Joaçaba",
    4206706: "Herval d'Oeste",
    4219705: "Xaxim",
    4203808: "São Miguel do Oeste",
    4204004: "São Miguel do Oeste",
    4206656: "São Miguel do Oeste",
    4208906: "Joaçaba",
    4216107: "Seara",
    4219358: "Xanxerê",
    4201273: "Chapecó",
    4204152: "Chapecó",
    4205373: "Chapecó",
    4205431: "Chapecó",
}


def classify_microregion(
    series: pd.Series,
    codigo_ibge: bool = True,
) -> pd.Series:
    """Classifica municípios do Oeste SC em microrregiões.

    Args:
        series: Série com códigos IBGE (7 dígitos) ou nomes de municípios.
        codigo_ibge: Se ``True``, interpreta a série como códigos numéricos.

    Returns:
        Série com o nome da microrregião ou ``"Fora da região"``.
    """
    if codigo_ibge:
        # Converte para int para lookup
        def _lookup(code) -> str:
            try:
                return _MUN_TO_MICRO.get(int(code), "Fora da região")
            except (ValueError, TypeError):
                return "Fora da região"

        return series.apply(_lookup)

    # Caso seja nome de município (fallback simples)
    nome_to_micro = {
        "Chapecó": "Chapecó",
        "Concórdia": "Concórdia",
        "Seara": "Seara",
        "São Miguel do Oeste": "São Miguel do Oeste",
        "Itapiranga": "São Miguel do Oeste",
        "Guatambú": "São Miguel do Oeste",
        "Xanxerê": "Xanxerê",
        "Joaçaba": "Joaçaba",
        "Herval d'Oeste": "Joaçaba",
        "Xaxim": "Chapecó",
    }
    return series.apply(
        lambda x: nome_to_micro.get(str(x).strip(), "Fora da região")
    )


def cnae_to_sector(cnae_code: str) -> str:
    """Converte código CNAE 2.0 (7 dígitos ou subclasse) para setor agregado.

    Args:
        cnae_code: String com o código CNAE (ex: ``"1011201"``, ``"47.11-3/01"``).

    Returns:
        Nome do setor econômico agregado ou ``"Desconhecido"``.
    """
    if pd.isna(cnae_code) or str(cnae_code).strip() == "":
        return "Desconhecido"

    code_str = str(cnae_code).strip().replace(".", "").replace("-", "").replace("/", "")
    # Extrai os dois primeiros dígitos (seção CNAE)
    secao = code_str[:2]
    return _CNAE_SECAO_MAP.get(secao, "Desconhecido")


def cut_age_bins(
    series: pd.Series,
    bins: Sequence[int] | None = None,
    labels: Sequence[str] | None = None,
    right: bool = True,
) -> pd.Series:
    """Classifica idades em faixas etárias.

    Args:
        series: Série numérica com idades.
        bins: Limites dos intervalos. Padrão:
            ``[0, 5, 10, 15, 18, 25, 35, 45, 55, 65, 100]``.
        labels: Rótulos para cada intervalo. Padrão gera automaticamente.
        right: Se ``True``, os intervalos são fechados à direita (a, b].

    Returns:
        Série categórica com faixas etárias.
    """
    if bins is None:
        bins = [0, 5, 10, 15, 18, 25, 35, 45, 55, 65, 100]

    if labels is None:
        labels = [
            f"{bins[i]}-{bins[i+1]-1}" for i in range(len(bins) - 1)
        ]

    # Converte para numérico, forçando erros para NaN
    ages = pd.to_numeric(series, errors="coerce")
    return pd.cut(ages, bins=bins, labels=labels, right=right, include_lowest=True)


def compute_indices(
    df: pd.DataFrame,
    group_col: str = "cod_ibge",
    pop_col: str | None = None,
    vinculos_col: str | None = None,
    mortes_col: str | None = None,
    nascimentos_col: str | None = None,
) -> pd.DataFrame:
    """Calcula índices municipais a partir de indicadores agregados.

    Os índices calculados incluem:
        - **Taxa de vínculos por habitante**: ``vinculos / pop * 1000``
        - **Taxa de mortalidade infantil** (aproximada): ``mortes / nascimentos * 1000``
        - **Razão de dependência** (se colunas de faixa etária existirem)

    Args:
        df: DataFrame agregado por município.
        group_col: Coluna de agrupamento (código IBGE).
        pop_col: Nome da coluna de população.
        vinculos_col: Nome da coluna de total de vínculos empregatícios.
        mortes_col: Nome da coluna de óbitos.
        nascimentos_col: Nome da coluna de nascimentos.

    Returns:
        DataFrame com colunas adicionais de índices.
    """
    df_out = df.copy()

    if pop_col and vinculos_col:
        if pop_col in df_out.columns and vinculos_col in df_out.columns:
            df_out["taxa_vinculos_1000hab"] = (
                df_out[vinculos_col] / df_out[pop_col] * 1000
            )
            logger.info("Índice taxa_vinculos_1000hab calculado.")

    if mortes_col and nascimentos_col:
        if mortes_col in df_out.columns and nascimentos_col in df_out.columns:
            df_out["taxa_mortalidade_infantil_1000"] = (
                df_out[mortes_col] / df_out[nascimentos_col].replace(0, pd.NA) * 1000
            )
            logger.info("Índice taxa_mortalidade_infantil_1000 calculado.")

    # Razão de dependência simples (0-14 e 65+ / 15-64) se colunas existirem
    col_jovem = [c for c in df_out.columns if "0-14" in c or "0-4" in c or "5-9" in c]
    col_idoso = [c for c in df_out.columns if "65+" in c or "65-" in c]
    col_adulto = [c for c in df_out.columns if "15-64" in c or "25-54" in c]

    if col_jovem and col_idoso and col_adulto:
        df_out["razao_dependencia"] = (
            df_out[col_jovem].sum(axis=1) + df_out[col_idoso].sum(axis=1)
        ) / df_out[col_adulto].sum(axis=1).replace(0, pd.NA)
        logger.info("Índice razao_dependencia calculado.")

    return df_out
