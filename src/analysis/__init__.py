"""
Pacote de analise do projeto migracao-venezuelana-oeste-sc.

Autores: Leonardo Rafael Santos Leitao e Vicente Neves da Silva Ribeiro (UFFS)
"""

from .demografia import build_pyramid, calc_taxa_dependencia, calc_razao_sexos
from .mercado_trabalho import analise_rotatividade, analise_salarial, survival_analysis
from .espacial import calc_morani, calc_lisa, plot_mapa

__all__ = [
    "build_pyramid",
    "calc_taxa_dependencia",
    "calc_razao_sexos",
    "analise_rotatividade",
    "analise_salarial",
    "survival_analysis",
    "calc_morani",
    "calc_lisa",
    "plot_mapa",
]
