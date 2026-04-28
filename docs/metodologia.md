# Metodologia: Raio X da Migração Venezuelana no Oeste de Santa Catarina

**Projeto:** `migracao-venezuelana-oeste-sc`  
**Autores:** Leonardo Rafael Santos Leitão e Vicente Neves da Silva Ribeiro (Universidade Federal da Fronteira Sul – UFFS)  
**Repositório:** GitHub / OSF / Zenodo / Zotero  
**Data:** Abril de 2026

---

## 1. Resumo Executivo

O presente projeto propõe uma investigação quantitativa e qualitativa sobre os fluxos migratórios provenientes da Venezuela para o Oeste de Santa Catarina (Brasil), com ênfase nas dimensões demográfica, laboral, de saúde, educação e assistência social. Por meio da integração de múltiplas fontes administrativas — IBGE, DataSUS, RAIS, CAGED, Secretarias Estaduais de Desenvolvimento Social e de Assistência Social de SC — busca-se construir um retrato abrangente e atualizado da população venezuelana residente na região. A metodologia adota princípios de ciência aberta (FAIR, CARE, TOP Guidelines), garantindo reprodutibilidade, transparência e cuidado ético no manejo de dados sensíveis sobre populações migrantes.

---

## 2. Problema de Pesquisa

A crise humanitária venezuelana, iniciada no início da década de 2010, desencadeou um dos maiores êxodos contemporâneos das Américas. O Brasil, particularmente os estados de fronteira, tornou-se destino significativo para deslocados em busca de refúgio, segurança e oportunidades econômicas. No entanto, a região Oeste de Santa Catarina — compreendendo os municípios de Chapecó, Xanxerê, Concórdia, Joaçaba, São Miguel do Oeste, entre outros — carece de estudos sistemáticos que quantifiquem e qualifiquem a presença venezuelana em suas múltiplas dimensões.

**Questão central:** Quais são as características demográficas, socioeconômicas e territoriais da população venezuelana no Oeste de Santa Catarina, e de que modo esses padrões diferem entre municípios e ao longo do tempo (2018–2024)?

**Questões subsidiárias:**
- Quais são os perfis etário, de gênero e de fecundidade da população migrante?
- Em quais setores econômicos e ocupações os venezuelanos estão concentrados?
- Como se distribuem os eventos de saúde (óbitos, nascimentos, hospitalizações) nessa população?
- Quais são os padrões espaciais de concentração e segregação dos migrantes?
- De que forma as políticas públicas locais respondem às demandas dessa população?

---

## 3. Hipóteses

1. **Concentração espacial:** A população venezuelana concentra-se em municípios de médio porte com atividade econômica ligada ao agronegócio e à indústria de carnes (CNAE 10.1), notadamente Chapecó, Xanxerê e Concórdia.

2. **Perfil laboral:** Há sobre-representação de venezuelanos em ocupações de baixa qualificação e alta rotatividade, com remuneração média inferior à dos trabalhadores brasileiros nos mesmos setores.

3. **Perfil demográfico:** A população apresenta pirâmide etária jovem (concentração na faixa 20–39 anos), com razão de sexos masculina elevada, refletindo a migração econômica de homens adultos.

4. **Sazonalidade e saúde:** Os eventos de saúde (óbitos, nascimentos) apresentam correlação com a dinâmica de inserção laboral e condições de moradia precárias, com taxas superiores às da população local em indicadores sensíveis.

5. **Segregação residencial:** O Índice de Moran I para a proporção de venezuelanos por município sugere aglomeração espacial positiva, indicando padrões de concentração em bairros e municípios específicos.

---

## 4. Interdisciplinaridade

A pesquisa articula contribuições de múltiplas disciplinas, conforme sintetizado na tabela abaixo.

| Disciplina | Contribuição Teórica | Contribuição Metodológica | Variáveis-Chave |
|:---|:---|:---|:---|
| **Sociologia** | Teorias da migração (Portes, Massey, Sayad); incorporação ao mercado de trabalho; vulnerabilidade social. | Análise de redes e trajetórias ocupacionais; entrevistas qualitativas. | Ocupação, setor, vínculo empregatício, condições de moradia. |
| **História** | Contextualização da crise venezuelana; história migratória do Oeste de SC; memória e trajetórias. | História oral; análise documental de registros administrativos como fontes históricas. | Ano de chegada, município de destino anterior, fluxos migratórios. |
| **Demografia** | Transição migratória; estruturas etárias; taxas de fecundidade e mortalidade; projeções populacionais. | Métodos de estimativa de população; pirâmides etárias; taxas brutas e específicas; análise de sobrevivência. | Idade, sexo, cor/raça, estado civil, fecundidade, óbitos, nascimentos. |

A integração interdisciplinar permite superar abordagens unidimensionais, articulando estruturas macro (crise político-econômica venezuelana, dinâmica regional do agronegócio) com trajetórias micro (individuais e familiares).

---

## 5. Objetivos

### 5.1 Objetivo Geral

Caracterizar a população venezuelana residente no Oeste de Santa Catarina nas dimensões demográfica, laboral, de saúde, educação e assistência social, identificando padrões de concentração espacial, desigualdades e vulnerabilidades no período 2018–2024.

### 5.2 Objetivos Específicos

1. Estimar o tamanho e a composição demográfica (sexo, idade, cor/raça, estado civil) da população venezuelana por município do Oeste de SC, com base em dados do IBGE (Censos e PNAD Contínua) e registros administrativos.

2. Analisar a inserção no mercado de trabalho formal, por meio da RAIS e CAGED, identificando setores de atuação, ocupações, salários e padrões de rotatividade.

3. Avaliar a dinâmica de saúde da população venezuelana a partir dos sistemas DataSUS (SIM, SINASC, SIH/AIH, BPA), calculando indicadores de mortalidade, natalidade e morbidade hospitalar.

4. Mapear a distribuição espacial da população venezuelana no território, empregando técnicas de análise espacial (Moran I, LISA) para identificar padrões de aglomeração e segregação.

5. Documentar a inserção da população venezuelana nos sistemas de educação e assistência social, por meio de dados das Secretarias Estaduais de Educação e de Assistência Social de SC.

6. Construir uma infraestrutura de dados abertos e reprodutível, alinhada aos princípios FAIR, CARE e TOP Guidelines, garantindo acessibilidade e cuidado ético.

---

## 6. Recorte Espacial e Temporal

### 6.1 Recorte Espacial

O Oeste de Santa Catarina compreende 32 municípios organizados em sete microrregiões geográficas (IBGE):

| Microrregião | Municípios Principais |
|:---|:---|
| Chapecó | Chapecó, Guatambú, Seara |
| Concórdia | Concórdia, Ipumirim, Irani |
| Joaçaba | Joaçaba, Herval d'Oeste, Luzerna |
| São Miguel do Oeste | São Miguel do Oeste, Descanso, Bom Jesus do Oeste |
| Xanxerê | Xanxerê, Xaxim, Abelardo Luz |
| Maravilha | Maravilha, Cunha Porã, São João do Oeste |
| São Lourenço do Oeste | São Lourenço do Oeste, Campo Erê, Nova Itaberaba |

> **Nota:** A delimitação exata dos 32 municípios segue a classificação oficial do IBGE para a Mesorregião do Oeste Catarinense.

### 6.2 Recorte Temporal

- **Período primário:** 2018–2024 (dados administrativos e censitários).
- **Período contextual:** 2010–2024 (para análise de tendências de longo prazo).
- **Corte transversal prioritário:** 2022 (Censo Demográfico mais recente).

---

## 7. Fontes de Dados e Metodologia

### 7.1 IBGE — Instituto Brasileiro de Geografia e Estatística

| Aspecto | Descrição |
|:---|:---|
| **Bases utilizadas** | Censo Demográfico 2010 e 2022; PNAD Contínua (2018–2024); Projeções da População; Malhas municipais. |
| **Variáveis** | Sexo, idade, cor/raça, estado civil, país de nascimento, município de residência, escolaridade, condição de atividade. |
| **Metodologia** | Extração via API SIDRA e bases microdados; tabulação cruzada por município e país de nascimento; construção de pirâmides etárias e razões demográficas. |
| **Limitações** | Subenumeração de populações migrantes em situação de irregularidade; sub-registro de naturalização; desatualização entre Censos. |

### 7.2 DataSUS — Departamento de Informática do SUS

| Sistema | Dados | Variáveis-Chave | Aplicação |
|:---|:---|:---|:---|
| **SIM** | Sistema de Informação sobre Mortalidade | Causa básica (CID-10), data do óbito, idade, sexo, cor/raça, município de residência, país de nascimento. | Cálculo de taxas de mortalidade; análise de causas evitáveis. |
| **SINASC** | Sistema de Informação sobre Nascidos Vivos | Data do nascimento, idade da mãe, sexo do recém-nascido, cor/raça, município de residência, país de nascimento da mãe. | Cálculo de taxas de fecundidade; análise de condições de nascimento. |
| **SIH/AIH** | Sistema de Informações Hospitalares / Autorização de Internação Hospitalar | Diagnóstico principal (CID-10), procedimento, valor, idade, sexo, município de residência, dias de permanência. | Análise de morbidade hospitalar; custos e perfil de internações. |
| **BPA** | Boletim de Produção Ambulatorial | Procedimentos ambulatoriais, especialidade, município. | Acesso a serviços de saúde primária e especializada. |

**Metodologia DataSUS:** Download de arquivos DBC via FTP oficial; descompressão e conversão para Parquet/CSV com `pysus`; vinculação por município de residência e, quando disponível, por país de nascimento. Cálculo de taxas brutas padronizadas por idade, utilizando como referência a população brasileira do IBGE.

### 7.3 RAIS — Relação Anual de Informações Sociais

| Aspecto | Descrição |
|:---|:---|
| **Fonte** | Ministério do Trabalho e Emprego (MTE) — bases públicas. |
| **Cobertura** | Vínculos empregatícios formais ativos em 31/12 de cada ano (2018–2023). |
| **Variáveis** | CNPJ do estabelecimento, CNAE 2.0, CBO 2002, salário de dezembro, escolaridade, sexo, idade, município do estabelecimento, data de admissão/demissão. |
| **Metodologia** | Filtragem por nacionalidade venezuelana (quando disponível) ou inferência por nome e/ou CPF (com validação); análise descritiva de salários medianos e médios; concentração setorial (CNAE); análise de Gini salarial. |
| **Limitações** | Não identifica nacionalidade de forma explícita em todas as edições; sub-representa trabalho informal e precário. |

### 7.4 CAGED — Cadastro Geral de Empregados e Desempregados

| Aspecto | Descrição |
|:---|:---|
| **Fonte** | Ministério do Trabalho e Emprego (MTE). |
| **Cobertura** | Movimentações (admissões e desligamentos) no mercado de trabalho formal (2018–2024). |
| **Variáveis** | Tipo de movimentação, CBO, CNAE, salário, sexo, idade, grau de instrução, município do trabalho, saldo de emprego. |
| **Metodologia** | Cálculo de saldo de emprego por município, setor e trimestre; análise de rotatividade (taxa de turnover); análise de sobrevivência no emprego (Kaplan-Meier). |

### 7.5 Secretaria de Estado da Educação de SC (SED/SC)

| Aspecto | Descrição |
|:---|:---|
| **Dados** | Matrículas por município, etapa de ensino, cor/raça, país de nascimento (quando disponível). |
| **Acesso** | Solicitação via LAI (Lei de Acesso à Informação); dados agregados no portal QEdu ou similares. |
| **Metodologia** | Taxas de matrícula, evasão escolar e distorção idade-série por município; análise comparativa entre população venezuelana e brasileira. |

### 7.6 Secretaria de Estado da Assistência Social de SC (SAS/SC)

| Aspecto | Descrição |
|:---|:---|
| **Dados** | Atendimentos nos Centro de Referência de Assistência Social (CRAS) e Centro Especializado (CREAS); famílias atendidas pelo Bolsa Família; Cadastro Único (CadÚnico). |
| **Acesso** | Solicitação via LAI; bases do MDS (Ministério do Desenvolvimento Social) quando disponíveis. |
| **Metodologia** | Proporção de famílias venezuelanas no CadÚnico; perfil de atendimento por tipo de serviço; análise de vulnerabilidade social. |

---

## 8. Pipeline Computacional

O projeto adota uma arquitetura de dados em camadas, orientada ao processo ELT (Extract-Load-Transform), implementada predominantemente em Python e com versionamento via Git.

### 8.1 Camada 1 — Ingestão (Raw)

Os dados brutos são obtidos diretamente das fontes oficiais e armazenados em formato original (DBC, CSV, XLSX, JSON) no diretório `data/raw/`. Cada fonte possui um subdiretório próprio (`data/raw/ibge/`, `data/raw/datasus/`, `data/raw/rais/`, etc.). Um arquivo `hash.sha256` acompanha cada conjunto de dados para garantir integridade.

### 8.2 Camada 2 — Limpeza e Harmonização (Bronze)

Scripts Python em `src/pipeline/` realizam a limpeza inicial: remoção de duplicatas, padronização de nomes de colunas, tratamento de valores ausentes, conversão de tipos e criação de identificadores únicos. Os dados são salvos em formato Parquet (`data/bronze/`), otimizado para leitura e compressão.

### 8.3 Camada 3 — Integração e Enriquecimento (Silver)

Nesta camada, os dados de diferentes fontes são integrados por chaves comuns (município, ano, sexo, faixa etária). Adicionam-se variáveis derivadas: taxas demográficas, indicadores socioeconômicos, classificações setoriais. O resultado é salvo em `data/silver/`.

### 8.4 Camada 4 — Análise e Modelagem (Gold)

Tabelas analíticas prontas para visualização, modelagem estatística e publicação. Incluem agregações municipais, séries temporais e matrizes de vizinhança espacial. Armazenadas em `data/gold/`.

### 8.5 Ferramentas e Dependências

| Camada | Ferramentas |
|:---|:---|
| Ingestão | `pysus`, `sidrapy`, `requests`, `ftplib`, `pandas` |
| Limpeza | `pandas`, `numpy`, `polars` (opcional), `pandera` (validação) |
| Integração | `pandas`, `sqlalchemy`, `duckdb` |
| Análise | `statsmodels`, `scipy`, `pysal` (espaçial), `lifelines` (sobrevivência) |
| Visualização | `matplotlib`, `seaborn`, `plotly`, `geopandas`, `folium` |
| Dashboard | `streamlit` |
| Reprodutibilidade | `poetry`, `conda`, `docker` (opcional), `git`, `dvc` (opcional) |

---

## 9. Ciência Aberta e Reprodutibilidade

### 9.1 Princípios FAIR

Os dados e códigos do projeto seguem os princípios FAIR (Findable, Accessible, Interoperable, Reusable):

- **Findable:** Identificadores DOI via Zenodo; metadados descritivos no OSF; catalogação no repositório institucional da UFFS.
- **Accessible:** Código-fonte aberto no GitHub; dados agregados publicados em formato aberto (CSV, Parquet); dados individuais sensíveis armazenados em repositório controlado, com termo de uso.
- **Interoperable:** Uso de vocabulários controlados (CID-10, CBO, CNAE, geocódigos IBGE); formato Parquet para compatibilidade entre linguagens.
- **Reusable:** Licença MIT para código; CC-BY 4.0 para dados agregados; documentação completa de variáveis e metodologia.

### 9.2 Princípios CARE

Considerando que a pesquisa envolve dados sobre populações indígenas e migrantes em situação de vulnerabilidade, adotamos os princípios CARE (Collective benefit, Authority to control, Responsibility, Ethics):

- **Benefício coletivo:** Os resultados devem subsidiar políticas públicas que melhorem as condições de vida dos migrantes venezuelanos, e não apenas gerar capital acadêmico.
- **Autoridade de controle:** Em fases qualitativas, os participantes têm direito de revisar, aprovar ou retirar suas contribuições.
- **Responsabilidade:** Os pesquisadores assumem compromisso de devolver os resultados à comunidade migrante e aos gestores públicos locais.
- **Ética:** Dados sensíveis são anonimizados ou agregados; nenhuma informação individual é publicada sem consentimento.

### 9.3 TOP Guidelines

O projeto adota o nível 2 do Transparency and Openness Promotion (TOP) Guidelines:

- **Citação de dados:** Todos os conjuntos de dados utilizados são citados com DOI ou URL de acesso.
- **Transparência de código:** Código de análise disponível no GitHub; notebooks reprodutíveis.
- **Pré-registro:** Protocolo de pesquisa registrado no OSF (em andamento).
- **Reprodução:** Instruções de instalação e execução documentadas em `README.md` e `pyproject.toml`.

### 9.4 Infraestrutura

| Plataforma | Uso |
|:---|:---|
| **GitHub** | Versionamento de código, issues, pull requests, GitHub Actions (CI/CD). |
| **OSF** | Pré-registro de hipóteses, armazenamento de documentos, wiki colaborativa. |
| **Zenodo** | Publicação de datasets com DOI, vinculação a releases do GitHub. |
| **Zotero** | Gestão bibliográfica compartilhada, integração com LaTeX/Overleaf. |

---

## 10. Cronograma

O projeto tem duração prevista de **24 meses**, divididos em quatro trimestres por ano.

| Etapa | Mês 1–3 | Mês 4–6 | Mês 7–9 | Mês 10–12 | Mês 13–15 | Mês 16–18 | Mês 19–21 | Mês 22–24 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Revisão bibliográfica** | ■ | ■ | ■ | □ | □ | □ | □ | □ |
| **Levantamento de dados** | □ | ■ | ■ | ■ | □ | □ | □ | □ |
| **Limpeza e integração** | □ | □ | ■ | ■ | ■ | □ | □ | □ |
| **Análise demográfica** | □ | □ | □ | ■ | ■ | ■ | □ | □ |
| **Análise laboral** | □ | □ | □ | □ | ■ | ■ | ■ | □ |
| **Análise de saúde** | □ | □ | □ | □ | ■ | ■ | ■ | □ |
| **Análise espacial** | □ | □ | □ | □ | □ | ■ | ■ | ■ |
| **Análise educação/assistência** | □ | □ | □ | □ | □ | □ | ■ | ■ |
| **Redação de artigos** | □ | □ | □ | □ | □ | ■ | ■ | ■ |
| **Ciência aberta / publicação** | □ | □ | □ | □ | □ | □ | ■ | ■ |
| **Defesa / finalização** | □ | □ | □ | □ | □ | □ | □ | ■ |

> **Legenda:** ■ = atividade em execução; □ = não iniciada ou concluída.

---

## 11. Produtos Esperados

1. **Artigo científico** em periódico indexado (ex.: *Revista Brasileira de Estudos de População*, *Dados*, *Cadernos Saúde Pública*).
2. **Relatório técnico** para gestores públicos do Oeste de SC (Secretarias de Saúde, Assistência Social, Trabalho).
3. **Dashboard interativo** online (Streamlit) com filtros por município, ano e tema.
4. **Repositório de dados** no Zenodo, com DOI, contendo bases agregadas e dicionário de dados.
5. **Código-fonte** no GitHub, com notebooks reprodutíveis e módulos Python documentados.
6. **Apresentações em eventos** científicos (ABEP, ANPOCS, SBS, etc.).
7. **Material didático** para cursos de extensão e formação de agentes públicos sobre migração e dados.

---

## 12. Desafios e Cuidados Metodológicos

1. **Sub-registro e subenumeração:** Populações migrantes em situação irregular ou temporária frequentemente escapam aos registros administrativos e censitários. Estratégia: uso de múltiplas fontes (triangulação) e ajustes estatísticos.

2. **Identificação de nacionalidade:** Nem todas as bases identificam "Venezuela" de forma consistente (ex.: "naturalizado brasileiro", "apátrida", "outros países da América do Sul"). Estratégia: cruzamento de bases e validação por amostragem.

3. **Dados sensíveis:** Informações de saúde e assistência social exigem anonimização e agregação antes da publicação. Estratégia: aplicação de técnicas de k-anonimato e publicação apenas de estatísticas agregadas.

4. **Vieses de seleção:** Trabalhadores formais (RAIS/CAGED) não representam a totalidade da população economicamente ativa. Estratégia: contextualização explícita dos limites de cada fonte.

5. **Ecologia espacial:** A análise de Moran I por município pode sofrer do problema da unidade de área modificável (MAUP). Estratégia: sensibilidade a diferentes escalas e comparação com dados de setores censitários, quando disponíveis.

6. **Mudanças de classificação:** CBO e CNAE sofreram revisões no período. Estratégia: uso de correspondências oficiais do IBGE para harmonização temporal.

---

## 13. Checklist Ciência Aberta

| Item | Status | Responsável | Prazo |
|:---|:---:|:---|:---:|
| Repositório GitHub criado e configurado | ⬜ | Leonardo | Mês 2 |
| Estrutura de diretórios (`data/`, `src/`, `docs/`, `notebooks/`) definida | ⬜ | Leonardo | Mês 2 |
| `README.md` com instruções de instalação e reprodução | ⬜ | Leonardo | Mês 3 |
| `pyproject.toml` / `poetry.lock` com dependências versionadas | ⬜ | Leonardo | Mês 3 |
| `LICENSE` (MIT para código, CC-BY para dados) incluída | ⬜ | Leonardo | Mês 3 |
| Dicionário de dados (`docs/dicionario_dados.md`) completo | ⬜ | Leonardo | Mês 4 |
| Documentação metodológica (`docs/metodologia.md`) atualizada | ⬜ | Leonardo/Vicente | Mês 4 |
| Dados brutos armazenados com checksum (SHA-256) | ⬜ | Leonardo | Mês 5 |
| Pipeline de limpeza versionado e reprodutível | ⬜ | Leonardo | Mês 6 |
| Notebooks reprodutíveis com saídas limpas | ⬜ | Leonardo | Mês 8 |
| Pré-registro no OSF | ⬜ | Vicente | Mês 6 |
| Zenodo vinculado ao GitHub (auto-DOI por release) | ⬜ | Leonardo | Mês 10 |
| Zotero compartilhado com bibliografia completa | ⬜ | Vicente | Mês 3 |
| Dados agregados publicados com DOI | ⬜ | Leonardo | Mês 20 |
| Artigo submetido com link para repositório | ⬜ | Leonardo/Vicente | Mês 22 |
| Material didático disponível em licença aberta | ⬜ | Leonardo/Vicente | Mês 24 |

> **Legenda:** ⬜ = pendente; 🟡 = em andamento; ✅ = concluído.

---

*Documento elaborado em conformidade com as diretrizes de ciência aberta FAIR, CARE e TOP Guidelines. Para dúvidas ou sugestões, abra uma issue no repositório GitHub do projeto.*
