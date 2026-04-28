"""Configuração centralizada do pipeline de ETL.

Este módulo centraliza paths, constantes e variáveis de ambiente utilizados
por todo o pipeline. As configurações podem ser sobrescritas via arquivo ``.env``
na raiz do projeto.

Example:
    >>> from src.config import Settings
    >>> cfg = Settings()
    >>> print(cfg.DATA_RAW)
    PosixPath('/Users/.../raio_x_migraçao/data/raw')
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env, se existir
load_dotenv(Path(__file__).resolve().parents[2] / ".env")


@dataclass(frozen=True)
class Settings:
    """Configurações imutáveis do pipeline.

    Attributes:
        PROJECT_ROOT: Diretório raiz do projeto (detectado automaticamente).
        DATA_RAW: Diretório para dados brutos extraídos das fontes.
        DATA_PROCESSED: Diretório para dados processados e limpos.
        DATA_EXTERNAL: Diretório para dados externos de referência.
        OUTPUTS: Diretório para artefatos finais (tabelas, gráficos, relatórios).
        LOG_LEVEL: Nível de logging padrão.
        REGIAO_OESTE_SC: Lista de códigos IBGE (7 dígitos) dos municípios do Oeste SC.
        PERIODO_ANALISE: Anos cobertos pela análise.
        NACIONALIDADE_VENEZUELA: Variantes textuais de nacionalidade venezuelana.
    """

    PROJECT_ROOT: Path = field(
        default_factory=lambda: Path(__file__).resolve().parents[1]
    )
    DATA_RAW: Path = field(
        default_factory=lambda: Path(os.getenv("DATA_RAW", "data/raw"))
    )
    DATA_PROCESSED: Path = field(
        default_factory=lambda: Path(os.getenv("DATA_PROCESSED", "data/processed"))
    )
    DATA_EXTERNAL: Path = field(
        default_factory=lambda: Path(os.getenv("DATA_EXTERNAL", "data/external"))
    )
    OUTPUTS: Path = field(
        default_factory=lambda: Path(os.getenv("OUTPUTS", "outputs"))
    )
    LOG_LEVEL: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

    # Constantes do domínio
    # Região Geográfica Intermediária de Chapecó (IBGE) — 109 municípios
    REGIAO_OESTE_SC: List[int] = field(
        default_factory=lambda: [
            4200051, 4200101, 4200408, 4200507, 4200556, 4200754, 4200804,
            4201273, 4201653, 4202081, 4202099, 4202156, 4202537, 4202578,
            4203105, 4203501, 4203600, 4203907, 4204004, 4204103, 4204152,
            4204202, 4204301, 4204350, 4204400, 4204459, 4204707, 4204756,
            4204905, 4205001, 4205175, 4205209, 4205308, 4205357, 4205431,
            4205605, 4206405, 4206603, 4206652, 4206702, 4206801, 4207601,
            4207650, 4207684, 4207700, 4207759, 4207809, 4207858, 4208005,
            4208401, 4208609, 4208955, 4209003, 4209177, 4209201, 4209458,
            4209854, 4210035, 4210506, 4210555, 4210902, 4211009, 4211405,
            4211454, 4211652, 4211801, 4211850, 4211876, 4212007, 4212106,
            4212239, 4212270, 4212601, 4212908, 4213104, 4213153, 4213401,
            4213906, 4214151, 4214201, 4215075, 4215208, 4215356, 4215554,
            4215687, 4215695, 4215752, 4216008, 4216107, 4216255, 4216701,
            4216909, 4217154, 4217204, 4217303, 4217501, 4217550, 4217758,
            4217956, 4218509, 4218756, 4218855, 4219101, 4219150, 4219176,
            4219507, 4219606, 4219705, 4219853,
        ]
    )

    PERIODO_ANALISE: range = field(
        default_factory=lambda: range(2018, 2027)
    )

    NACIONALIDADE_VENEZUELA: List[str] = field(
        default_factory=lambda: [
            "VENEZUELA",
            "VENEZUELANO",
            "VENEZUELANA",
            "VEN",
        ]
    )

    def __post_init__(self) -> None:
        """Resolve paths relativos ao PROJECT_ROOT, se necessário."""
        object.__setattr__(
            self, "DATA_RAW", self._resolve(self.DATA_RAW)
        )
        object.__setattr__(
            self, "DATA_PROCESSED", self._resolve(self.DATA_PROCESSED)
        )
        object.__setattr__(
            self, "DATA_EXTERNAL", self._resolve(self.DATA_EXTERNAL)
        )
        object.__setattr__(
            self, "OUTPUTS", self._resolve(self.OUTPUTS)
        )
        # Garante que os diretórios existam
        self.DATA_RAW.mkdir(parents=True, exist_ok=True)
        self.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
        self.DATA_EXTERNAL.mkdir(parents=True, exist_ok=True)
        self.OUTPUTS.mkdir(parents=True, exist_ok=True)

    def _resolve(self, path: Path) -> Path:
        """Resolve path relativo ao PROJECT_ROOT quando não for absoluto."""
        if path.is_absolute():
            return path
        return self.PROJECT_ROOT / path


# Instância padrão importável
SETTINGS = Settings()
