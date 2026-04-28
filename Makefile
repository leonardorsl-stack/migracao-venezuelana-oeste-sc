# =============================================================================
# Makefile — Raio X da Migração Venezuelana no Oeste de SC
# =============================================================================
# Autores: Leonardo Rafael Santos Leitão, Vicente Neves da Silva Ribeiro
# Instituição: UFFS — Campus Chapecó
# =============================================================================

.PHONY: help install test lint format clean data-dir run-pipeline dashboard report

# ---------------------------------------------------------------------------
# Configurações
# ---------------------------------------------------------------------------
PYTHON := python
CONDA_ENV := migracao-sc
SRC_DIR := src
TESTS_DIR := tests
NOTEBOOKS_DIR := notebooks
REPORTS_DIR := reports
DATA_DIR := data

# ---------------------------------------------------------------------------
# Target padrão
# ---------------------------------------------------------------------------
help:
	@echo "============================================================================="
	@echo "  Raio X da Migração Venezuelana no Oeste de SC — Targets disponíveis"
	@echo "============================================================================="
	@echo ""
	@echo "  make install       Cria/atualiza o ambiente Conda e instala dependências"
	@echo "  make test          Executa a suite de testes com pytest"
	@echo "  make lint          Executa linter (ruff) no código-fonte"
	@echo "  make format        Formata código com black e isort"
	@echo "  make clean         Remove artefatos gerados (__pycache__, .pyc, etc.)"
	@echo "  make data-dir      Cria a estrutura de diretórios de dados"
	@echo "  make run-pipeline  Executa o pipeline completo de ETL e análise"
	@echo "  make dashboard     Inicia o dashboard interativo (Streamlit)"
	@echo "  make report        Gera relatórios Quarto (HTML/PDF)"
	@echo "  make all           Instala + testa + formata + executa pipeline"
	@echo ""
	@echo "============================================================================="

# ---------------------------------------------------------------------------
# Instalação
# ---------------------------------------------------------------------------
install:
	@echo "==> Criando ambiente Conda '$(CONDA_ENV)'..."
	conda env create -f environment.yml || conda env update -f environment.yml
	@echo "==> Ambiente criado/atualizado. Ative com: conda activate $(CONDA_ENV)"
	@echo "==> Instalando pacotes adicionais via pip..."
	$(PYTHON) -m pip install -e . --no-deps || true
	@echo "==> Instalação concluída."

# ---------------------------------------------------------------------------
# Testes
# ---------------------------------------------------------------------------
test:
	@echo "==> Executando testes com pytest..."
	$(PYTHON) -m pytest $(TESTS_DIR) \
		--verbose \
		--cov=$(SRC_DIR) \
		--cov-report=term-missing \
		--cov-report=html:htmlcov \
		--cov-report=xml:coverage.xml

# ---------------------------------------------------------------------------
# Qualidade de código
# ---------------------------------------------------------------------------
lint:
	@echo "==> Executando ruff linter..."
	ruff check $(SRC_DIR) $(TESTS_DIR) $(NOTEBOOKS_DIR)
	@echo "==> Executando ruff format check..."
	ruff format --check $(SRC_DIR) $(TESTS_DIR) $(NOTEBOOKS_DIR)
	@echo "==> Executando mypy..."
	mypy $(SRC_DIR)

format:
	@echo "==> Formatando código com black..."
	black $(SRC_DIR) $(TESTS_DIR) $(NOTEBOOKS_DIR)
	@echo "==> Organizando imports com isort..."
	isort $(SRC_DIR) $(TESTS_DIR) $(NOTEBOOKS_DIR)
	@echo "==> Auto-corrigindo com ruff..."
	ruff check --fix $(SRC_DIR) $(TESTS_DIR) $(NOTEBOOKS_DIR)
	@echo "==> Formatação concluída."

# ---------------------------------------------------------------------------
# Limpeza
# ---------------------------------------------------------------------------
clean:
	@echo "==> Removendo artefatos Python..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.py[cod]" -delete 2>/dev/null || true
	find . -type f -name "*~" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
	@echo "==> Removendo relatórios de cobertura..."
	rm -rf htmlcov coverage.xml .coverage 2>/dev/null || true
	@echo "==> Removendo diretórios Quarto intermediários..."
	rm -rf $(REPORTS_DIR)/*_files $(REPORTS_DIR)/*_cache .quarto 2>/dev/null || true
	@echo "==> Limpeza concluída."

# ---------------------------------------------------------------------------
# Estrutura de dados
# ---------------------------------------------------------------------------
data-dir:
	@echo "==> Criando estrutura de diretórios de dados..."
	mkdir -p $(DATA_DIR)/raw
	mkdir -p $(DATA_DIR)/interim
	mkdir -p $(DATA_DIR)/processed
	mkdir -p $(DATA_DIR)/external
	@touch $(DATA_DIR)/raw/.gitkeep
	@touch $(DATA_DIR)/interim/.gitkeep
	@touch $(DATA_DIR)/processed/.gitkeep
	@touch $(DATA_DIR)/external/.gitkeep
	@echo "==> Estrutura criada."

# ---------------------------------------------------------------------------
# Pipeline principal
# ---------------------------------------------------------------------------
run-pipeline:
	@echo "==> Executando pipeline de extração de dados..."
	$(PYTHON) -m $(SRC_DIR).data.extract
	@echo "==> Executando pipeline de transformação..."
	$(PYTHON) -m $(SRC_DIR).data.transform
	@echo "==> Executando análises..."
	$(PYTHON) -m $(SRC_DIR).analysis.descriptive
	$(PYTHON) -m $(SRC_DIR).analysis.spatial
	@echo "==> Gerando visualizações..."
	$(PYTHON) -m $(SRC_DIR).visualization.figures
	@echo "==> Pipeline concluído."

# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
dashboard:
	@echo "==> Iniciando dashboard Streamlit..."
	streamlit run $(SRC_DIR)/visualization/dashboard.py

# ---------------------------------------------------------------------------
# Relatórios Quarto
# ---------------------------------------------------------------------------
report:
	@echo "==> Renderizando relatórios Quarto..."
	quarto render $(REPORTS_DIR)/quarto/index.qmd --to html
	quarto render $(REPORTS_DIR)/quarto/index.qmd --to pdf || echo "PDF requer LaTeX instalado."
	@echo "==> Relatórios gerados em $(REPORTS_DIR)/"

# ---------------------------------------------------------------------------
# Target combinado
# ---------------------------------------------------------------------------
all: install format test run-pipeline report
	@echo "==> Execução completa finalizada."
