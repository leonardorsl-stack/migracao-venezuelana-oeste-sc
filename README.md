# Raio X da Migração Venezuelana no Oeste de Santa Catarina

[![Licença: MIT](https://img.shields.io/badge/Licen%C3%A7a-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Licença: CC BY 4.0](https://img.shields.io/badge/Licen%C3%A7a-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Quarto](https://img.shields.io/badge/quarto-%5E1.4-blueviolet)](https://quarto.org)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

> Pipeline computacional reprodutível para análise demográfica, sociológica e histórica da migração venezuelana na região oeste de Santa Catarina, Brasil.

---

## 📋 Descrição

Este repositório contém o pipeline completo de extração, processamento, análise e comunicação de dados relativos à migração venezuelana no oeste catarinense. O projeto adota princípios de ciência aberta (FAIR, CARE, TOP Guidelines) e é inteiramente reprodutível via ambientes Conda e automação via Make.

### Objetivos

1. Mapear a evolução demográfica da população venezuelana nos municípios do oeste de SC.
2. Analisar inserção socioeconômica (mercado de trabalho, saúde, educação).
3. Produzir relatórios, dashboards e artigos científicos a partir de código versionado.

---

## 🏗️ Estrutura de Diretórios

```
migracao-venezuelana-oeste-sc/
├── data/
│   ├── raw/              # Dados brutos (não versionados)
│   ├── interim/          # Dados intermediários
│   ├── processed/        # Dados processados (prontos para análise)
│   └── external/         # Dados de terceiros (shapefiles, etc.)
├── notebooks/            # Notebooks exploratórios Jupyter
├── src/
│   ├── data/             # Scripts de extração e limpeza
│   ├── features/         # Engenharia de features
│   ├── analysis/         # Análises estatísticas e espaciais
│   └── visualization/    # Visualizações e dashboards
├── reports/
│   ├── figures/          # Figuras geradas
│   ├── tables/           # Tabelas geradas
│   └── quarto/           # Documentos Quarto (.qmd)
├── tests/                # Testes automatizados (pytest)
├── docs/                 # Documentação adicional
├── Makefile              # Automação de tarefas
├── environment.yml       # Ambiente Conda
├── requirements.txt      # Dependências pip
├── CITATION.cff          # Metadados de citação
├── references.bib        # Referências bibliográficas
├── LICENSE               # Licenças MIT + CC-BY-4.0
└── README.md             # Este arquivo
```

---

## 🚀 Instalação

### Pré-requisitos

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) ou [Anaconda](https://www.anaconda.com/)
- Make (Linux/macOS nativo; Windows via [Chocolatey](https://chocolatey.org/packages/make) ou WSL)
- Git

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/migracao-venezuelana-oeste-sc.git
cd migracao-venenzuelana-oeste-sc

# 2. Crie o ambiente Conda
make install
# ou manualmente:
# conda env create -f environment.yml

# 3. Ative o ambiente
conda activate migracao-sc

# 4. Copie e configure as variáveis de ambiente
cp .env.example .env
# Edite .env com suas credenciais (nunca versione este arquivo)
```

---

## 🖥️ Uso

### Executar o pipeline completo

```bash
make run-pipeline
```

### Executar análises específicas

```bash
# Dashboard interativo (Streamlit)
make dashboard

# Gerar relatório Quarto
make report

# Limpar arquivos gerados
make clean
```

### Comandos úteis

| Comando | Descrição |
|---------|-----------|
| `make help` | Mostra todos os targets disponíveis |
| `make test` | Executa testes com pytest |
| `make lint` | Executa linter (ruff) |
| `make format` | Formata código (black) |
| `make data-dir` | Cria estrutura de diretórios de dados |

---

## 📊 Fontes de Dados

| Fonte | Descrição | Acesso |
|-------|-----------|--------|
| IBGE | Censo Demográfico, PNAD Contínua | [ibge.gov.br](https://www.ibge.gov.br) |
| DataSUS | SIM, SINASC, SIAB | [datasus.saude.gov.br](https://datasus.saude.gov.br) |
| RAIS | Relação Anual de Informações Sociais | [gov.br/trabalho](https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/rais) |
| CAGED | Cadastro Geral de Empregados e Desempregados | [gov.br/trabalho](https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/caged) |
| Secretarias de Educação de SC | Matrículas por município | Sob demanda |
| Secretarias de Assistência Social de SC | CadÚnico, SUAS | Sob demanda |

---

## 📄 Citação

Se utilizar este projeto ou dados, por favor cite:

```bibtex
@software{migracao_venezuelana_oeste_sc,
  author       = {Santos Leitão, Leonardo Rafael and Neves da Silva Ribeiro, Vicente},
  title        = {Raio X da Migração Venezuelana no Oeste de Santa Catarina},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.XXXXXXX},
  url          = {https://github.com/SEU_USUARIO/migracao-venezuelana-oeste-sc}
}
```

Veja também [`CITATION.cff`](CITATION.cff) para metadados completos no formato CFF.

---

## 👥 Autores

- **Leonardo Rafael Santos Leitão** — [leonardorsl@uffs.edu.br](mailto:leonardorsl@uffs.edu.br) · [ORCID](https://orcid.org/0000-0000-0000-0000) · [Lattes](http://lattes.cnpq.br/)
- **Vicente Neves da Silva Ribeiro** — [Lattes](http://lattes.cnpq.br/)

**Instituição:** Universidade Federal da Fronteira Sul (UFFS) — Campus Chapecó  
**Grupo de Pesquisa:** Inserção e Pertencimento Socioterritorial (IaPS)

---

## 🤝 Ciência Aberta

Este projeto adere aos seguintes frameworks e diretrizes:

- **[FAIR Principles](https://doi.org/10.1038/sdata.2016.18)** — Dados encontráveis, acessíveis, interoperáveis e reutilizáveis.
- **[CARE Principles](https://doi.org/10.1038/s41597-021-00892-0)** — Governança indígena e justa sobre dados.
- **[TOP Guidelines](https://doi.org/10.1126/science.aab2374)** — Transparência e reprodutibilidade em pesquisa.

### Repositórios e Registros

| Serviço | Link | Propósito |
|---------|------|-----------|
| GitHub | [github.com/SEU_USUARIO/migracao-venezuelana-oeste-sc](https://github.com) | Versionamento de código |
| OSF | [osf.io/XXXXX](https://osf.io) | Pré-registro e materiais |
| Zenodo | [doi.org/10.5281/zenodo.XXXXXXX](https://zenodo.org) | Arquivamento com DOI |
| Zotero | [zotero.org/groups/XXXXX](https://www.zotero.org) | Bibliografia colaborativa |

---

## 📜 Licença

- **Código-fonte:** [MIT License](LICENSE) © 2026 Leonardo Rafael Santos Leitão e Vicente Neves da Silva Ribeiro.
- **Dados, relatórios e figuras:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE).

Consulte o arquivo [`LICENSE`](LICENSE) para o texto completo e detalhes de aplicação.

---

> *Este projeto foi desenvolvido no âmbito das atividades de pesquisa do Grupo IaPS/UFFS, com apoio da Universidade Federal da Fronteira Sul.*
