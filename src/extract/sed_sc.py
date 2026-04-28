"""Stub para extração de dados da Secretaria de Estado da Educação de SC.

Este módulo define a interface esperada para acesso aos dados educacionais do
Estado de Santa Catarina, mantidos pela Secretaria de Estado da Educação (SED/SC)
e, em parte, pelo INEP (Censo Escolar).

Atenção:
    Os microdados individuais de matrículas (nome, CPF, data de nascimento,
    nacionalidade, etc.) **não são publicados abertamente** pela SED/SC.
    O acesso a esses dados requer:

    1. Protocolo de solicitação via Lei de Acesso à Informação (LAI);
    2. Termo de compromisso de sigilo;
    3. Aprovação do Conselho Estadual de Proteção de Dados Pessoais de SC;
    4. Justificativa de interesse público da pesquisa.

    Dados agregados por escola e município estão disponíveis via:
    - Portal QEdu (https://qedu.org.br/)
    - Portal do INEP > Censo Escolar (https://www.gov.br/inep/pt-br)
    - Portal da Transparência de SC (dados consolidados)

    A implementação completa deste extrator depende de autorização formal da
    SED/SC e da assinatura de termos de uso.

Example:
    >>> from src.extract.sed_sc import load_matriculas
    >>> # Após obter os dados via LAI:
    >>> df = load_matriculas("/caminho/para/dados_sed_sc.csv")
"""

from __future__ import annotations

import logging
import warnings
from pathlib import Path
from typing import Optional

import pandas as pd

from src.config import SETTINGS

logger = logging.getLogger(__name__)


def load_matriculas(
    filepath: Optional[Path] = None,
    ano: Optional[int] = None,
    municipios_ibge: Optional[list] = None,
) -> pd.DataFrame:
    """Carrega microdados de matrículas da rede estadual/municipal de SC.

    Esta função é um *stub*. Ela documenta a interface esperada e verifica
    se o arquivo fornecido existe, mas **não realiza download automático**
    pois os dados não são públicos.

    Args:
        filepath: Caminho para o arquivo CSV/Parquet fornecido pela SED/SC
            após solicitação LAI. Se ``None``, procura em ``data/external/``
            por um arquivo padrão.
        ano: Ano de referência das matrículas (ex: 2023).
        municipios_ibge: Lista de códigos IBGE para filtrar. Padrão:
            ``REGIAO_OESTE_SC``.

    Returns:
        DataFrame com dados de matrículas.

    Raises:
        FileNotFoundError: Se o arquivo não for encontrado.
        NotImplementedError: Sempre, para reforçar que é um stub.
    """
    warnings.warn(
        "load_matriculas é um stub. Os dados da SED/SC requerem solicitação LAI."
    )

    if filepath is None:
        if ano is None:
            ano = max(SETTINGS.PERIODO_ANALISE)
        filepath = SETTINGS.DATA_EXTERNAL / f"sed_sc_matriculas_{ano}.csv"

    if not filepath.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {filepath}. "
            "É necessário solicitar os dados à SED/SC via LAI."
        )

    logger.info("Lendo matrículas de %s...", filepath)
    df = pd.read_csv(filepath, dtype=str, low_memory=False)

    if municipios_ibge is None:
        municipios_ibge = SETTINGS.REGIAO_OESTE_SC

    col_mun = "CO_MUNICIPIO" if "CO_MUNICIPIO" in df.columns else "COD_MUNICIPIO"
    if col_mun in df.columns:
        df = df[df[col_mun].astype(str).isin([str(m) for m in municipios_ibge])]

    return df


def load_pare(
    filepath: Optional[Path] = None,
    ano: Optional[int] = None,
    municipios_ibge: Optional[list] = None,
) -> pd.DataFrame:
    """Carrega dados do PARE (Programa de Avaliação de Rendimento Escolar) de SC.

    O PARE contém informações de avaliação e fluxo escolar dos estudantes.
    Assim como as matrículas, os microdados individuais não são públicos e
    requerem solicitação formal à SED/SC.

    Args:
        filepath: Caminho para o arquivo fornecido pela SED/SC.
        ano: Ano de referência.
        municipios_ibge: Lista de códigos IBGE para filtrar.

    Returns:
        DataFrame com dados do PARE.

    Raises:
        FileNotFoundError: Se o arquivo não for encontrado.
        NotImplementedError: Sempre, como reforço de stub.
    """
    warnings.warn(
        "load_pare é um stub. Os dados da SED/SC requerem solicitação LAI."
    )

    if filepath is None:
        if ano is None:
            ano = max(SETTINGS.PERIODO_ANALISE)
        filepath = SETTINGS.DATA_EXTERNAL / f"sed_sc_pare_{ano}.csv"

    if not filepath.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {filepath}. "
            "É necessário solicitar os dados à SED/SC via LAI."
        )

    logger.info("Lendo PARE de %s...", filepath)
    df = pd.read_csv(filepath, dtype=str, low_memory=False)

    if municipios_ibge is None:
        municipios_ibge = SETTINGS.REGIAO_OESTE_SC

    col_mun = "CO_MUNICIPIO" if "CO_MUNICIPIO" in df.columns else "COD_MUNICIPIO"
    if col_mun in df.columns:
        df = df[df[col_mun].astype(str).isin([str(m) for m in municipios_ibge])]

    return df
