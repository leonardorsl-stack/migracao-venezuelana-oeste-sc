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
    REGIAO_OESTE_SC: List[int] = field(
        default_factory=lambda: [
            4204202,  # Chapecó
            4204301,  # Concórdia
            4216800,  # Seara
            4217250,  # São Miguel do Oeste
            4207684,  # Itapiranga
            4206607,  # Guatambú
            4219507,  # Xanxerê
            4209003,  # Joaçaba
            4206706,  # Herval d'Oeste
            4219705,  # Xaxim
            4203808,  # Cunha Porã
            4204004,  # Cunhataí
            4206656,  # Guaraciaba
            4208906,  # Jupiá
            4216107,  # Riqueza
            4219358,  # Vargeão
            4201273,  # Águas de Chapecó
            4204152,  # Bom Jesus do Oeste
            4205373,  # Coronel Freitas
            4205431,  # Caxambu do Sul
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
