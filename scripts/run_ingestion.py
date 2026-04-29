#!/usr/bin/env python3
"""Script de ingestão unificado do projeto migracao-venezuelana-oeste-sc.

Executa o pipeline de download de dados brutos (IBGE e DataSUS),
cria diretórios necessários e gera um relatório de ingestão com
arquivos baixados, tamanhos e schemas.

Uso:
    python scripts/run_ingestion.py [--force]
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Garante que o diretório raiz do projeto está no PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import SETTINGS
from src.extract.datasus import download_sim_sc, download_sinasc_sc
from src.extract.ibge import fetch_censo_2022_migrantes, fetch_populacao_estimada

logger = logging.getLogger("run_ingestion")


def setup_logging(level: int = logging.INFO) -> None:
    """Configura logging para console e arquivo."""
    SETTINGS.DATA_RAW.mkdir(parents=True, exist_ok=True)
    log_file = SETTINGS.DATA_RAW / "ingestion.log"

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file, encoding="utf-8"),
        ],
    )
    logger.info("Logging configurado. Arquivo: %s", log_file)


def collect_file_info(pattern: str) -> list[dict[str, Any]]:
    """Coleta metadados de arquivos que casam com o padrão glob."""
    files: list[dict[str, Any]] = []
    for path in SETTINGS.DATA_RAW.rglob(pattern):
        if path.is_file():
            stat = path.stat()
            files.append({
                "path": str(path.relative_to(PROJECT_ROOT)),
                "size_bytes": stat.st_size,
                "size_human": _human_readable_size(stat.st_size),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            })
    return files


def _human_readable_size(size_bytes: int) -> str:
    """Converte bytes para formato legível."""
    for unit in ["B", "KB", "MB", "GB"]:
        if abs(size_bytes) < 1024.0:
            return f"{size_bytes:3.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def generate_report(report_data: dict[str, Any], output_path: Path) -> None:
    """Gera relatório de ingestão em JSON e texto simples."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # JSON
    json_path = output_path.with_suffix(".json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False, default=str)
    logger.info("Relatório JSON salvo em %s", json_path)

    # Texto simples
    txt_path = output_path.with_suffix(".txt")
    lines = [
        "=" * 70,
        " RELATÓRIO DE INGESTÃO – migracao-venezuelana-oeste-sc ",
        "=" * 70,
        f"Gerado em: {report_data['timestamp']}",
        f"Forçar re-download: {report_data['force']}",
        "",
        "--- ETAPAS ---",
    ]
    for step in report_data.get("steps", []):
        status_icon = "✓" if step.get("success") else "✗"
        lines.append(f"{status_icon} {step['name']}: {step['message']}")
        if "records" in step:
            lines.append(f"   registros: {step['records']}")
        if "files" in step:
            for f in step["files"]:
                lines.append(f"   - {f['path']} ({f['size_human']})")
        lines.append("")

    lines.append("--- RESUMO DE ARQUIVOS ---")
    for f in report_data.get("all_files", []):
        lines.append(f"{f['path']:<60} {f['size_human']:>10}")

    lines.append("")
    lines.append("=" * 70)
    lines.append(f"Total de arquivos: {len(report_data.get('all_files', []))}")
    lines.append("=" * 70)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    logger.info("Relatório TXT salvo em %s", txt_path)


def run(force: bool = False) -> int:
    """Executa o pipeline de ingestão.

    Returns:
        Código de saída (0 = sucesso, 1 = erro).
    """
    setup_logging()
    logger.info("Iniciando pipeline de ingestão (force=%s)", force)

    report: dict[str, Any] = {
        "timestamp": datetime.now().isoformat(),
        "force": force,
        "steps": [],
        "all_files": [],
    }
    success = True

    # --- 1. Cria diretórios ---
    dirs_to_create = [
        SETTINGS.DATA_RAW / "ibge",
        SETTINGS.DATA_RAW / "datasus" / "SIM",
        SETTINGS.DATA_RAW / "datasus" / "SINASC",
        SETTINGS.DATA_PROCESSED,
    ]
    for d in dirs_to_create:
        d.mkdir(parents=True, exist_ok=True)
    logger.info("Diretórios criados/verificados: %s", [str(d) for d in dirs_to_create])

    # --- 2. IBGE – População estimada ---
    try:
        df_pop = fetch_populacao_estimada(force=force)
        report["steps"].append({
            "name": "IBGE - População Estimada",
            "success": True,
            "message": f"Download concluído. Registros: {len(df_pop)}",
            "records": len(df_pop),
            "files": collect_file_info("ibge/populacao_estimada*"),
        })
        logger.info("IBGE População Estimada: %s registros", len(df_pop))
    except Exception as exc:
        logger.exception("Falha em IBGE População Estimada")
        report["steps"].append({
            "name": "IBGE - População Estimada",
            "success": False,
            "message": str(exc),
        })
        success = False

    # --- 3. IBGE – Censo 2022 Migrantes (stub) ---
    try:
        df_mig = fetch_censo_2022_migrantes(force=force)
        report["steps"].append({
            "name": "IBGE - Censo 2022 Migrantes",
            "success": True,
            "message": f"Stub gerado. Registros: {len(df_mig)}",
            "records": len(df_mig),
            "files": collect_file_info("ibge/censo2022*"),
        })
        logger.info("IBGE Censo 2022 Migrantes: %s registros", len(df_mig))
    except Exception as exc:
        logger.exception("Falha em IBGE Censo 2022 Migrantes")
        report["steps"].append({
            "name": "IBGE - Censo 2022 Migrantes",
            "success": False,
            "message": str(exc),
        })
        success = False

    # --- 4. DataSUS – SIM ---
    try:
        df_sim = download_sim_sc(force=force)
        report["steps"].append({
            "name": "DataSUS - SIM SC",
            "success": True,
            "message": f"Download concluído. Registros: {len(df_sim)}",
            "records": len(df_sim),
            "files": collect_file_info("datasus/SIM/*.parquet"),
        })
        logger.info("DataSUS SIM: %s registros", len(df_sim))
    except Exception as exc:
        logger.exception("Falha em DataSUS SIM")
        report["steps"].append({
            "name": "DataSUS - SIM SC",
            "success": False,
            "message": str(exc),
        })
        success = False

    # --- 5. DataSUS – SINASC ---
    try:
        df_sinasc = download_sinasc_sc(force=force)
        report["steps"].append({
            "name": "DataSUS - SINASC SC",
            "success": True,
            "message": f"Download concluído. Registros: {len(df_sinasc)}",
            "records": len(df_sinasc),
            "files": collect_file_info("datasus/SINASC/*.parquet"),
        })
        logger.info("DataSUS SINASC: %s registros", len(df_sinasc))
    except Exception as exc:
        logger.exception("Falha em DataSUS SINASC")
        report["steps"].append({
            "name": "DataSUS - SINASC SC",
            "success": False,
            "message": str(exc),
        })
        success = False

    # --- 6. Relatório final ---
    report["all_files"] = collect_file_info("*")
    report_path = SETTINGS.DATA_RAW / "ingestion_report"
    generate_report(report, report_path)

    if success:
        logger.info("Pipeline de ingestão concluído com sucesso.")
        return 0
    else:
        logger.error("Pipeline de ingestão concluído com erros. Verifique os logs.")
        return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Pipeline de ingestão de dados brutos do projeto."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Força re-download de todos os dados, ignorando cache.",
    )
    args = parser.parse_args()
    sys.exit(run(force=args.force))
