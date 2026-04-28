"""Funções de harmonização geográfica e temporal para integração de datasets.

Este módulo padroniza códigos geográficos do IBGE (6 vs 7 dígitos), datas em
formato ``YYYY-MM``, e realiza merge (consolidação) de múltiplas fontes de
dados sobre uma chave comum.

Example:
    >>> from src.transform.harmonizacao import harmonize_geocodes, standardize_dates
    >>> df["cod_ibge"] = harmonize_geocodes(df["cod_municipio"])
    >>> df["ano_mes"] = standardize_dates(df["data"])
"""

from __future__ import annotations

import logging
import re
from typing import List, Optional, Sequence, Union

import pandas as pd

from src.config import SETTINGS

logger = logging.getLogger(__name__)


def harmonize_geocodes(
    series: pd.Series,
    target_length: int = 7,
    invalid_fill: Optional[str] = None,
) -> pd.Series:
    """Harmoniza códigos geográficos do IBGE para comprimento padrão.

    A série de entrada pode conter códigos com 6 dígitos (município sem
    dígito verificador) ou 7 dígitos (com dígito verificador). Esta função
    garante que todos os códigos tenham o comprimento alvo.

    Args:
        series: Série pandas com códigos IBGE (tipo ``str`` ou ``int``).
        target_length: Comprimento desejado (``6`` ou ``7``).
        invalid_fill: Valor para preencher códigos inválidos/nulos.
            Se ``None``, mantém ``NaN``.

    Returns:
        Série pandas com códigos padronizados como string.

    Raises:
        ValueError: Se ``target_length`` não for ``6`` ou ``7``.
    """
    if target_length not in (6, 7):
        raise ValueError("target_length deve ser 6 ou 7.")

    s = series.astype(str).str.strip()
    # Remove possíveis pontos/decimais de conversão float
    s = s.str.replace(r"\.0$", "", regex=True)

    def _adjust_code(code) -> Optional[str]:
        if pd.isna(code):
            return invalid_fill
        code_str = str(code).strip()
        if code_str in ("nan", "None", "", "<NA>"):
            return invalid_fill
        digits = re.sub(r"\D", "", code_str)
        if len(digits) == target_length:
            return digits
        if len(digits) == 6 and target_length == 7:
            # Acrescenta dígito verificador zero (simplificado)
            return digits + "0"
        if len(digits) == 7 and target_length == 6:
            return digits[:-1]
        logger.warning("Código IBGE inválido ignorado: %s", code_str)
        return invalid_fill

    return s.apply(_adjust_code)


def standardize_dates(
    series: pd.Series,
    input_format: Optional[str] = None,
    output_format: str = "%Y-%m",
    errors: str = "coerce",
) -> pd.Series:
    """Padroniza uma série de datas para formato ``YYYY-MM``.

    Args:
        series: Série com datas em formato misto (string, datetime, etc.).
        input_format: Formato de entrada (ex: ``%d/%m/%Y``). Se ``None``,
            tenta inferir automaticamente via ``pd.to_datetime``.
        output_format: Formato de saída desejado. Padrão ``%Y-%m``.
        errors: Comportamento em caso de erro (``raise``, ``coerce``,
            ``ignore``).

    Returns:
        Série de strings no formato padronizado, ou ``NaT`` para inválidos
        quando ``errors='coerce'``.
    """
    dt = pd.to_datetime(series, format=input_format, errors=errors)
    return dt.dt.strftime(output_format).where(dt.notna())


def merge_datasets(
    datasets: Sequence[pd.DataFrame],
    on: Union[str, List[str]],
    how: str = "outer",
    validate: Optional[str] = None,
    indicator: Union[bool, str] = False,
) -> pd.DataFrame:
    """Consolida múltiplos DataFrames em um único dataset.

    Realiza merge sequencial sobre uma ou mais colunas-chave, garantindo
    compatibilidade de tipos antes da operação.

    Args:
        datasets: Sequência de DataFrames a serem unidos.
        on: Nome(s) da(s) coluna(s) chave para o merge.
        how: Tipo de merge (``left``, ``right``, ``outer``, ``inner``).
        validate: Validação de cardinalidade (``1:1``, ``1:m``, ``m:1``,
            ``m:m``). ``None`` desativa.
        indicator: Se ``True``, adiciona coluna ``_merge`` indicando origem.
            Também aceita string como nome da coluna.

    Returns:
        DataFrame consolidado.

    Raises:
        ValueError: Se a lista de datasets estiver vazia ou ``on`` não
            existir em algum DataFrame.
        KeyError: Se colunas obrigatórias estiverem ausentes.
    """
    if not datasets:
        raise ValueError("A sequência de datasets não pode estar vazia.")

    keys: List[str] = [on] if isinstance(on, str) else list(on)

    # Garante que todas as chaves existem
    for i, df in enumerate(datasets):
        missing = [k for k in keys if k not in df.columns]
        if missing:
            raise KeyError(
                f"DataFrame {i} não contém as colunas {missing}"
            )

    # Converte chaves para string para evitar problemas de tipo misto
    normalized = []
    for df in datasets:
        df_copy = df.copy()
        for k in keys:
            df_copy[k] = df_copy[k].astype(str)
        normalized.append(df_copy)

    result = normalized[0]
    for i, df_next in enumerate(normalized[1:], start=1):
        logger.info(
            "Merging dataset %s (%s rows) com resultado acumulado (%s rows) "
            "on=%s how=%s",
            i + 1,
            len(df_next),
            len(result),
            keys,
            how,
        )
        result = pd.merge(
            result,
            df_next,
            on=keys,
            how=how,
            validate=validate,
            indicator=indicator if isinstance(indicator, bool) else indicator,
        )

    logger.info("Merge concluído. Resultado: %s linhas x %s colunas.", *result.shape)
    return result
