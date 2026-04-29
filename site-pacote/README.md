# Crise, Migração e Trabalho: Trajetórias Migrantes de Venezuelanos no Oeste de Santa Catarina

> **Projeto de Pesquisa** coordenado pelos Professores **Vicente Neves da Silva Ribeiro** e **Leonardo Rafael Santos Leitão**, docentes da Universidade Federal da Fronteira Sul (UFFS), Campus Chapecó.

---

## 📌 Sobre o Projeto

Este projeto investiga as trajetórias migratórias de venezuelanos na **Região Intermediária de Chapecó**, Oeste de Santa Catarina — composta por **109 municípios** que abrigam aproximadamente 1,3 milhão de habitantes. A região tornou-se um dos principais polos de absorção da migração venezuelana no Sul do Brasil, impulsionada pela expansão do agronegócio, frigoríficos e serviços urbanos.

### Objetivos

1. Mapear a evolução espacial e temporal da presença venezuelana no Oeste SC (2018–2024)
2. Analisar o perfil sociodemográfico e ocupacional dos trabalhadores venezuelanos (RAIS)
3. Investigar o perfil de morbidade hospitalar da população venezuelana (SIH/SUS)
4. Produzir indicadores comparativos entre municípios para subsidiar políticas públicas

---

## 📊 Base de Dados Utilizadas

| Fonte | Sistema | Período | Registros | Filtro Aplicado |
|-------|---------|---------|-----------|-----------------|
| **RAIS** | Ministério do Trabalho | 2018–2024 | 226.945 vínculos | Nacionalidade = Venezuela (`NACIONAL` = '092') |
| **SIH/SUS** | DataSUS | 2018–2025 | 14.661 internações | Nacionalidade = Venezuela (`NACIONAL` = '092') |
| **SIM** | DataSUS | 2024 | 52.224 óbitos (SC) | Convertido; sem filtro de nacionalidade viável |
| **SINASC** | DataSUS | — | — | Sem campo de nacionalidade utilizável |
| **IBGE** | Censo/Estimativas | 2022/2025 | 109 municípios | Região Intermediária de Chapecó |

> **Nota metodológica:** Após verificação exaustiva, confirmou-se que apenas a RAIS e o SIH/SUS possuem campos de nacionalidade funcionais para filtrar venezuelanos. Os sistemas SIM, SINASC, SIA/SUS e CAGED não dispõem de variável de nacionalidade operacional para esse fim.

---

## 🗺️ Região de Estudo

**Região Intermediária de Chapecó (IBGE)** — 109 municípios do Oeste catarinense, incluindo:

- **Chapecó** — principal polo urbano e econômico (~230 mil hab.)
- **Concórdia, Joaçaba, São Miguel do Oeste** — polos secundários
- **Municípios do Extremo-Oeste** — Guatambú, Itapiranga, Seara, Nova Erechim

A região é caracterizada por:
- Intensa atividade agroindustrial (soja, milho, avicultura, suinocultura)
- Grande concentração de frigoríficos e cooperativas agrícolas
- Demanda crescente por mão de obra em setores de baixa qualificação

---

## 📁 Estrutura do Pacote

```
site-pacote/
├── README.md                          # Este arquivo
├── PROMPT_KIMI_DESKTOP.md             # Instruções para criação do site
├── DADOS_E_RESUMO.md                  # Dados tabulares e resumos
├── figuras/                           # 17 visualizações + 2 GIFs
│   ├── 01_evolucao_vinculos_regional.png
│   ├── 02_mapa_taxa_vinculos_2024.png
│   ├── 03_top15_municipios_volume_2024.png
│   ├── 04_dispersao_populacao_vs_vinculos.png
│   ├── 05_evolucao_internacoes_sih.png
│   ├── 06_comparativo_rais_vs_sih_2024.png
│   ├── 07_taxa_internacoes_vs_vinculos.png
│   ├── 08_mapa_coropletico_oeste_sc_2024.png
│   ├── 09_mapa_coropletico_volume_2024.png
│   ├── 10_animacao_evolucao_2018_2024.gif
│   ├── 11_bar_chart_race_2018_2024.gif
│   ├── 12_piramide_etaria_venezuelanos_vs_total.png
│   ├── 13_comparativo_faixa_etaria_percentual.png
│   ├── 14_heatmap_cids_municipios.png
│   ├── 15_composicao_morbidade_municipios.png
│   ├── 16_evolucao_top5_cids.png
│   └── 17_indice_concentracao_etaria.png
└── dados/
    ├── painel_oeste_sc_2018_2024.csv       # Painel longitudinal (763 linhas)
    └── top_cids_municipios_oeste_sc.txt    # Relatório de CIDs
```

---

## 🏛️ Instituição

**Universidade Federal da Fronteira Sul (UFFS)**  
Campus Chapecó — Centro de Ciências Humanas e Linguagens  
Grupo de Pesquisa em Sociologia e Antropologia da Migração

---

## 📅 Atualização

**Última atualização:** Abril de 2026  
**Dados mais recentes:** RAIS 2024, SIH/SUS 2025 (parcial)
