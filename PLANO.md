# PLANO DE EXECUÇÃO — Raio X da Migração Venezuelana no Oeste de SC

## Visão Geral
Este documento detalha o plano operacional rigoroso para execução do projeto, dividido em fases sequenciais e paralelas, com entregáveis mensuráveis, critérios de qualidade e checkpoints de decisão (go/no-go).

## Fase 1: Fundação (Concluída parcialmente)
- [x] Estrutura de diretórios e arquivos base
- [x] Configuração Git + primeiro commit
- [x] Ambiente Conda (environment.yml)
- [x] CI/CD GitHub Actions
- [x] Arquivos de configuração (.env protegido)
- [x] Módulos stubs ETL (extract, transform, analysis, visualization)
- [x] Notebooks exploratórios (01-06)
- [x] Documentação metodológica inicial
- [ ] Validação de credenciais OSF/Zenodo/Zotero
- [ ] Upload inicial dos dados estruturais ao OSF
- [ ] Configuração do grupo/coleção Zotero

## Fase 2: Ingestão de Dados Abertos (Semanas 3-8)
### 2.1 IBGE
- Implementar download automatizado via SIDRA para:
  - População total e estrangeira por município (Censo 2022)
  - Estimativas populacionais 2018-2024
  - PNAD Contínua (anos disponíveis)
- Critério de qualidade: checksum dos arquivos, schema validation
- Entregável: `data/processed/ibge_consolidado.parquet`

### 2.2 DataSUS
- Configurar PySUS e download batch:
  - SIM (2018-2024, SC, filtro nacionalidade/residência)
  - SINASC (2018-2024, SC)
  - AIH (2018-2024, SC)
  - BPA (amostra representativa)
  - SI-PNI (cobertura vacinal)
- Anonimização obrigatória antes de qualquer agregação
- Entregável: `data/processed/datasus_consolidado.parquet`

### 2.3 RAIS
- Download FTP/MTE dos microdados 2018-2023
- Filtro: UF=SC, nacionalidade=Venezuela
- Matching CNAE/CBO com setores da agroindústria
- Entregável: `data/processed/rais_vinculos_sc.parquet`

### 2.4 CAGED
- Download do Novo CAGED (2018-atual)
- Consolidação histórica admissões + desligamentos
- Cálculo de saldo, rotatividade, tempo médio de vínculo
- Entregável: `data/processed/caged_fluxo_sc.parquet`

### 2.5 Dados Subjetivos/Qualitativos
- Elaboração e envio de pedidos LAI para:
  - SED/SC (matrículas por nacionalidade, PARE)
  - SAS/SC (CRAS/CREAS, CadÚnico)
- Documentar respostas e não-respostas

## Fase 3: Integração e Enriquecimento (Semanas 7-12)
- Harmonização de códigos IBGE (6→7 dígitos)
- Geocodificação dos municípios (shapefiles do IBGE)
- Cruzamento temporal por município-ano-mês
- Construção do painel longitudinal:
  - `panel_oeste_sc_2018_2026.parquet`
- Índices sintéticos:
  - Taxa de dependência demográfica
  - Índice de vulnerabilidade laboral
  - Pressão sobre serviços públicos (saúde, educação, assistência)
- Validação: somatórios cruzados, sanity checks

## Fase 4: Análise (Semanas 11-18)
### 4.1 Demografia
- Pirâmides etárias por município e para a região
- Taxas de fecundidade (SINASC)
- Razão de sexos e composição familiar
- Projeções populacionais simplificadas

### 4.2 Mercado de Trabalho
- Análise setorial (CNAE frigorífico vs. outros)
- Desigualdade salarial (venezuelanos vs. brasileiros)
- Análise de sobrevivência (tempo até desligamento)
- Rotatividade e sazonalidade

### 4.3 Espacial
- Mapas coropléticos de densidade/concentração
- Análise de clusters (Moran I, LISA)
- Fluxos migratórios intra-regionais (se dados permitirem)

### 4.4 Temporal
- Séries temporais 2018-2026
- Testes de quebra estrutural (início Operação Acolhida, COVID-19)
- Modelagem ARIMA/ETS para alertas

### 4.5 Qualitativo/Histórico
- Periodização das políticas migratórias
- Entrevistas com gestores e trabalhadores (se aprovado pelo CEP)
- Análise documental (ACNUR, Comitê Gestor OA, imprensa)

## Fase 5: Produtos e Publicação (Semanas 17-24)
### 5.1 Dashboard
- Implementação em Streamlit ou Quarto + Observable
- Filtros: município, ano, tema (demografia, trabalho, saúde, educação)
- Deploy: Streamlit Cloud ou GitHub Pages

### 5.2 Atlas Cartográfico
- Mapas temáticos em alta resolução
- Exportação GeoJSON + PDF
- Publicação no Zenodo com DOI

### 5.3 Relatórios
- Relatório técnico anual (Quarto → PDF/HTML)
- Notas técnicas de alerta (quando indicadores atingirem limiares)

### 5.4 Artigo Científico
- Estrutura: Introduction, Literature, Data & Methods, Results, Discussion
- Submissão com dados e código em anexo (repositório + DOI)
- Pré-print: SciELO Preprints ou OSF Preprints

## Fase 6: Disseminação e Governança (Semanas 22-24+)
- Apresentação para gestores municipais e estaduais
- Seminários acadêmicos (ANPOCS, ANPUH, ABEP)
- Manutenção do repositório e atualização anual dos dados
- Comitê de governança com representantes da comunidade venezuelana (princípio CARE)

## Infraestrutura de Publicação
| Serviço | Função | Status | Próximo passo |
|---------|--------|--------|---------------|
| GitHub | Versionamento, CI/CD, issues | ✅ Configurado | Criar repositório remoto e push |
| OSF | Dados, pré-registro, wiki | ⏳ Pendente | Verificar token e upload inicial |
| Zenodo | DOI persistente, arquivamento | ⏳ Pendente | Verificar token e testar depósito |
| Zotero | Bibliografia compartilhada | ⏳ Pendente | Criar coleção e importar .bib |

## Checklist de Qualidade e Reprodutibilidade
- [ ] Ambiente Conda recriável em outra máquina (< 10 min)
- [ ] `make test` passa 100% (pytest)
- [ ] `make lint` passa sem erros (ruff)
- [ ] Pipeline completo roda com `make run-pipeline`
- [ ] Dados agregados publicados em formato aberto (Parquet/CSV)
- [ ] Dicionário de dados atualizado e versionado
- [ ] DOI ativo no Zenodo para cada release
- [ ] Código com cobertura de testes > 70%
- [ ] Documentação no README atualizada
- [ ] Licenças claras (MIT para código, CC-BY-4.0 para dados)

## Riscos e Mitigações
| Risco | Prob. | Impacto | Mitigação |
|-------|-------|---------|-----------|
| Indisponibilidade de dados (RAIS/CAGED) | Média | Alto | Cache local, snapshots anuais, fallback SIDRA |
| Mudança de schema do CAGED/Novo CAGED | Alta | Médio | Documentação de schemas, testes de schema validation |
| Não-resposta à LAI (SED/SAS) | Alta | Médio | Triangulação com dados federais, documentar omissão |
| Violação de dados sensíveis (LGPD) | Baixa | Muito alto | Anonimização hash, agregação prévia, acesso controlado |
| Dependência de bibliotecas não mantidas | Média | Médio | Ambiente Conda fixo, Docker opcional, pin de versões |

## Critérios de Sucesso
1. Painel longitudinal publicado com DOI e documentação completa
2. Dashboard acessível online com atualização anual
3. Pelo menos 1 artigo científico submetto com dados e código
4. Reprodutibilidade comprovada por execução em máquina externa
5. Impacto na formulação de políticas públicas (indicadores utilizados por gestores)

---
**Data do plano:** 2026-04-27  
**Versão:** 1.0  
**Responsável:** Leonardo Rafael Santos Leitão  
**Revisor:** Vicente Neves da Silva Ribeiro
