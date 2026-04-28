"""Módulo de extração de dados do pipeline ETL.

Este pacote agrupa funções de extração de diversas fontes públicas,
exportando as interfaces principais para uso no pipeline.

As funções exportadas cobrem:
    - IBGE (SIDRA, Censo, Estimativas Populacionais, PNAD)
    - DataSUS (SIM, SINASC, AIH, BPA, SIPNI) via PySUS
    - RAIS (vínculos empregatícios)
    - CAGED (admissões e desligamentos)
    - Secretaria de Educação de SC (stubs)
"""

from src.extract.ibge import (
    fetch_censo_2022,
    fetch_estimativas_populacionais,
    fetch_pnad,
    fetch_sidra,
)
from src.extract.datasus import (
    download_aih,
    download_bpa,
    download_sim,
    download_sinasc,
    download_sipni,
)
from src.extract.rais import fetch_rais_vinculos
from src.extract.caged import (
    concatena_historica,
    fetch_caged_admissoes,
    fetch_caged_desligamentos,
)
from src.extract.sed_sc import load_matriculas, load_pare

__all__ = [
    "fetch_sidra",
    "fetch_censo_2022",
    "fetch_estimativas_populacionais",
    "fetch_pnad",
    "download_sim",
    "download_sinasc",
    "download_aih",
    "download_bpa",
    "download_sipni",
    "fetch_rais_vinculos",
    "fetch_caged_admissoes",
    "fetch_caged_desligamentos",
    "concatena_historica",
    "load_matriculas",
    "load_pare",
]
