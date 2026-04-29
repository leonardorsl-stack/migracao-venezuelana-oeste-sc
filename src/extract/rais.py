#!/usr/bin/env python3
"""Download e processamento de RAIS para SC — filtro Venezuela.

STATUS: Pendente download real dos microdados.
Os microdados RAIS estão disponíveis em:
  ftp://ftp.mtps.gov.br/pdet/microdados/RAIS/

Requer acesso ao FTP do MTE e descompactação de arquivos .7z
"""
import logging
from pathlib import Path

import pandas as pd

from src.config import Settings

logger = logging.getLogger(__name__)
settings = Settings()

RAIS_YEARS = list(range(2018, 2024))

def fetch_rais_vinculos(year: int, uf: str = "SC") -> pd.DataFrame | None:
    """Stub para download de RAIS.
    
    TODO: Implementar download via FTP do MTE, descompactar .7z,
    filtrar por UF=SC e nacionalidade=Venezuela, e salvar em Parquet.
    """
    logger.warning("RAIS %d: download não implementado. Use FTP manual.", year)
    return None


def process_rais_sc(output_dir: Path = None) -> pd.DataFrame | None:
    """Processa todos os anos de RAIS disponíveis para SC."""
    if output_dir is None:
        output_dir = settings.DATA_RAW / "rais"
    output_dir.mkdir(parents=True, exist_ok=True)

    all_data = []
    for year in RAIS_YEARS:
        df = fetch_rais_vinculos(year)
        if df is not None:
            all_data.append(df)

    if not all_data:
        logger.warning("Nenhum dado RAIS disponível. Execute download manual via FTP.")
        return None

    combined = pd.concat(all_data, ignore_index=True)
    combined.to_parquet(output_dir / "rais_vinculos_sc_venezuela.parquet", compression="zstd")
    logger.info("RAIS processado: %d registros", len(combined))
    return combined


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    process_rais_sc()
