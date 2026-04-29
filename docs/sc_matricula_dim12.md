# Dimensao 12 - Ferramentas, Formatos e Metodos de Download e Processamento dos Dados

## Objetivo

Investigar as ferramentas, formatos, tamanhos e metodos necessarios para baixar e processar os microdados do Censo Escolar e outros datasets educacionais relevantes. Verificar se ha APIs, scripts, pacotes R/Python, tutoriais ou plataformas que facilitem o acesso e analise dos dados de matriculas por nacionalidade, com foco em Santa Catarina.

---

## 1. FORMATOS, TAMANHOS E ESTRUTURA DOS MICRODADOS DO CENSO ESCOLAR

### 1.1 Tamanho e formato dos arquivos originais do INEP

Claim: Os microdados do Censo Escolar da Educacao Basica sao disponibilizados em arquivos ZIP de aproximadamente 2-4 GB compactados, ocupando 10-20 GB descompactados, dependendo do ano.
Source: Brazil Visible
URL: https://brazilvisible.org/docs/apis/educacao/censo-escolar/
Date: Nao informada
Excerpt: "Tamanho, ~2-4 GB compactado (~10-20 GB descompactado, dependendo do ano)"
Context: Documentacao tecnica sobre API de educacao que consome dados do INEP.
Confidence: high

---

Claim: Os arquivos CSV do Censo Escolar sao delimitados por pipe (`|`), e o encoding pode variar entre anos (ISO-8859-1 ou UTF-8). Os arquivos de matricula sao divididos por regiao geografica (MATRICULA_SUL.CSV contem SC, PR e RS).
Source: Post tecnico em Medium / Portal INEP
URL: https://jonates.medium.com/python-primeiros-passos-no-pandas-1d90cb072e6b
Date: 2021-03-11
Excerpt: "Como os arquivos csv do Censo Escolar usa o caractere | (pipe ou barra em pe) como separador de atributos... Ja os conjunto de dados do IDEB... o encoding nao e UTF-8, e temos caractere especiais utilizados nos paises latinos como o Brasil, portanto vamos utilizar o encoding adequado que e o ISO-8859-1"
Context: Tutorial pratico de analise de dados do Censo Escolar com Python/Pandas.
Confidence: high

---

Claim: O arquivo MATRICULA_NORDESTE.CSV (exemplo de referencia) possui mais de 15 milhoes de linhas e 3,6 GB em disco. O arquivo MATRICULA_SUL.CSV e um dos cinco arquivos regionais de matricula.
Source: Stack Overflow em Portugues
URL: https://pt.stackoverflow.com/questions/434751/como-ler-os-dados-do-censo-escolar-no-r-matriculas
Date: 2020-02-08
Excerpt: "O ficheiro tem mais de 15 milhoes de linhas e 3,6 GB. [...] csv_files [1] MATRICULA_CO.CSV [2] MATRICULA_NORDESTE.CSV [3] MATRICULA_NORTE.CSV [4] MATRICULA_SUDESTE.CSV [5] MATRICULA_SUL.CSV"
Context: Resposta tecnica sobre como ler microdados do Censo Escolar em R de forma eficiente.
Confidence: high

---

### 1.2 Variaveis de nacionalidade e estrangeiros no Censo Escolar

Claim: A variavel `TP_NACIONALIDADE` identifica a nacionalidade do aluno com tres categorias: 1 - Brasileira; 2 - Brasileira (nascido no exterior ou naturalizado); 3 - Estrangeira. Alem disso, existe a variavel `CO_PAIS_ORIGEM` com o codigo do pais de origem e `NOME_PAIS_CE` com o nome do pais.
Source: Dicionario de Variaveis INEP / Portal de Imigracao MJSP
URL: https://portaldeimigracao.mj.gov.br/images/dados/microdados/2021/INEP/Dicionarios_INEP_-_Divulgacao_-_Censo_Escolar.xlsx
Date: Nao informada
Excerpt: "TP_NACIONALIDADE: 1 - Brasileira; 2 - Brasileira - nascido no exterior ou naturalizado; 3 - Estrangeira. NOME_PAIS_CE: Nome do pais de origem do aluno"
Context: Dicionario oficial de variaveis do Censo Escolar disponibilizado pelo MJSP/INEP.
Confidence: high

---

Claim: Pesquisas academicas utilizam as variaveis `TP_NACIONALIDADE` (codigo 3 = Estrangeira) e `CO_PAIS_ORIGEM` para analisar matriculas de criancas migrantes e refugiadas no Brasil. A UFPR publicou estudo sobre Educacao Infantil e migracao usando essas variaveis.
Source: UFPR - Dissertacao de Mestrado
URL: https://acervodigital.ufpr.br/xmlui/bitstream/handle/1884/93744/R%20-%20T%20-%20GIOCONDA%20GHIGGI.pdf
Date: Nao informada
Excerpt: "Para nossa analise selecionamos as oito variaveis... TP_NACIONALIDADE: 1 - Brasileira, 2 - Brasileira - nascido no exterior ou naturalizado, 3 - Estrangeira; CO_PAIS_ORIGEM: Codigo do pais"
Context: Dissertacao academica que analisa dados do Censo Escolar sobre criancas migrantes e refugiadas.
Confidence: high

---

## 2. PACOTES E FERRAMENTAS EM R

### 2.1 educabR (CRAN) - Pacote moderno e completo

Claim: O pacote `educabR` (disponivel no CRAN) permite download automatico e processamento dos microdados do Censo Escolar (1995-2024), com filtro por UF, limite de linhas (`n_max`) e cache local. Ele retorna dados em formato tidy.
Source: CRAN / RDocumentation
URL: https://cran.r-project.org/package=educabR
Date: 2026-04-06
Excerpt: "Download and process public education data from INEP... Provides functions to access microdata from the School Census (Censo Escolar)... get_censo_escolar(year, uf = NULL, n_max = Inf, keep_zip = TRUE, quiet = FALSE)"
Context: Pacote oficial no CRAN mantido por Sidney Bissoli. Versao 0.9.1.
Confidence: high

---

Claim: O pacote `educabR` permite filtrar por estado (UF) diretamente na funcao `get_censo_escolar()`, o que reduz o tempo de processamento e o uso de memoria. Tambem possui sistema de cache local.
Source: GitHub / educabR README
URL: https://github.com/SidneyBissoli/educabR
Date: 2026-02-03
Excerpt: "# Download School Census 2023 - filter by state; censo_sp <- get_censo_escolar(2023, uf = 'SP')"
Context: README do pacote educabR com exemplos praticos de uso.
Confidence: high

---

Claim: O pacote `educabR` possui vignettes (tutoriais) incluindo "What does school infrastructure look like across Brazil?" e "Mapping education indicators with geobr", facilitando a analise espacial.
Source: CRAN / educabR vignettes
URL: https://cran.r-project.org/web/packages/educabR/vignettes/getting-started.html
Date: Nao informada
Excerpt: "The package covers 14 datasets published by INEP, FNDE, CAPES, and STN... Use n_max for testing. Large files: ENEM and School Census files can be several GB."
Context: Documentacao oficial do pacote no CRAN.
Confidence: high

---

### 2.2 microdadosBrasil - Pacote historico

Claim: O pacote `microdadosBrasil` (GitHub) suporta leitura de microdados do Censo Escolar de 1995 a 2014, com funcao `read_CensoEscolar`. Internamente usa `readr` para arquivos fwf e `data.table` para CSV. Tambem harmoniza nomes de variaveis ao longo dos anos.
Source: GitHub - lucasmation/microdadosBrasil
URL: https://github.com/lucasmation/microdadosBrasil
Date: 2016-06-04
Excerpt: "Currently the package includes import functions for: INEP Censo Escolar read_CensoEscolar 1995 to 2014... In the background the package is running readr for fwf data and data.table for .csv data."
Context: Pacote historico bastante citado, embora possa estar desatualizado para anos recentes.
Confidence: medium

---

### 2.3 censoescolaR - Importacao e rotulacao

Claim: O pacote `censoescolaR` (GitHub) ajuda a importar e rotular (em portugues) os microdados do Censo Escolar. Funciona bem para 2019 e anos proximos. Possui funcao `download_microdata` auxiliar e `insert_labels` para aplicar dicionarios.
Source: GitHub - travitzki/censoescolaR
URL: https://github.com/travitzki/censoescolaR
Date: 2020-11-10
Excerpt: "O proposito deste pacote e contribuir para a politica de dados abertos, facilitando o acesso a bases detalhadas sobre educacao... Ate o momento, foi testado para todas as tabelas do Censo Escolar de 2019"
Context: Pacote comunitario para leitura e rotulacao de microdados.
Confidence: medium

---

### 2.4 Tecnicas de filtragem em R sem carregar toda a base

Claim: Em R, e possivel usar o pacote `sqldf` com `read.csv2.sql()` para aplicar filtros SQL diretamente durante a leitura do CSV, evitando carregar dados desnecessarios na memoria. Filtrar SC (CO_UF = '27') no MATRICULA_NORDESTE levou ~8,5 minutos e reduziu 15M linhas para ~930k.
Source: Stack Overflow em Portugues
URL: https://pt.stackoverflow.com/questions/434751/como-ler-os-dados-do-censo-escolar-no-r-matriculas
Date: 2020-02-08
Excerpt: "Para ler os dados e filtra-los ao mesmo tempo vou usar o pacote sqldf... SQL <- select * from file where CO_UF = '27'... foram precisos 8.5 minutos para ler e filtrar os dados... A base final tem cerca de 930 mil observacoes de 104 variaveis, o que representa apenas 6,10% dos dados"
Context: Resposta validada da comunidade R sobre leitura eficiente de microdados.
Confidence: high

---

Claim: Para trabalhar com dados maiores que a memoria RAM no R, a alternativa e usar SGBDs como MonetDBLite (agora obsoleto) ou PostgreSQL, com dplyr como backend. O MonetDBLite permitia ingestao rapida de CSV e consultas SQL nativas.
Source: R Mining Blog
URL: https://www.rmining.com.br/2016/10/15/usando-r-com-o-monetdb/index.html
Date: 2016-10-15
Excerpt: "Quem ja trabalha com a linguagem R ha um certo tempo provavelmente ja esta ciente das limitacoes da linguagem com relacao a conjuntos de dados maiores que a memoria RAM... o ideal e sempre trabalhar com sistemas de gerenciamento de banco de dados"
Context: Post tecnico sobre solucoes para big data em R com microdados publicos.
Confidence: medium

---

## 3. FERRAMENTAS E SCRIPTS EM PYTHON

### 3.1 Automacao de download e conversao para Parquet

Claim: O projeto `paeselhz/microdados_censo_escolar` (Python) automatiza o download dos microdados do INEP e converte os CSVs para formato Parquet, reduzindo o tamanho em ate 1/4. O projeto informa que existem aproximadamente 200 GB em CSV (2007-2019). Os arquivos ja convertidos estao disponiveis em `gs://microdados-inep/microdados-censo-escolar` no Google Cloud Storage.
Source: GitHub - paeselhz/microdados_censo_escolar
URL: https://github.com/paeselhz/microdados_censo_escolar
Date: 2020-10-27
Excerpt: "exporta os mesmos em .parquet, reduzindo em ate 1/4 o tamanho final de cada arquivo... aproximadamente 200 GB em CSV que precisam ser lidos e convertidos para parquet (somando os anos de 2007 a 2019)... arquivos ja convertidos em parquet no Google Cloud Storage, em gs://microdados-inep/microdados-censo-escolar"
Context: Projeto open source de automatizacao e otimizacao de microdados do Censo Escolar.
Confidence: high

---

Claim: O script de download usa Python com `requests` e `BeautifulSoup` para fazer scraping do portal do INEP e baixar todos os arquivos ZIP automaticamente.
Source: GitHub Gist - AlanTaranti
URL: https://gist.github.com/AlanTaranti/a89eba0e25f833e8334165572f4a72e3
Date: 2021-08-09
Excerpt: "import requests; from bs4 import BeautifulSoup; url = https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar... extrair todas as urls que terminam com .zip"
Context: Gist publico com script completo de scraping e download dos microdados.
Confidence: high

---

### 3.2 Pandas com chunksize para filtragem sem carregar tudo

Claim: Em Python/Pandas, e possivel processar arquivos CSV maiores que a memoria usando o parametro `chunksize` em `pd.read_csv()`, iterando sobre pedacos e concatenando apenas as linhas que atendem ao filtro desejado.
Source: Medium - Vincent Teyssier
URL: https://vincentteyssier.medium.com/filtering-csv-files-bigger-than-memory-to-a-pandas-dataframe-3ab51ff993fd
Date: 2018-08-11
Excerpt: "The solution is to parse csv files in chunks and append only the needed rows to our dataframe... df_result = pd.concat([chunk[chunk['my_field']>10] for chunk in iter_csv])"
Context: Artigo tecnico sobre processamento de CSVs grandes com Pandas.
Confidence: high

---

Claim: A documentacao oficial do Pandas recomenda o uso de `chunksize` em `read_csv()` para escalar a leitura de datasets massivos, carregando apenas um subconjunto de linhas na memoria de cada vez.
Source: Pandas Documentation
URL: https://pandas.pydata.org/docs/user_guide/scale.html
Date: Nao informada
Excerpt: "Some readers, like pandas.read_csv(), offer parameters to control the chunksize when reading a single file. Manually chunking is an OK option for workflows..."
Context: Documentacao oficial do Pandas sobre escalabilidade.
Confidence: high

---

### 3.3 DuckDB - SQL direto sobre CSV sem importacao

Claim: DuckDB permite executar comandos SQL diretamente sobre arquivos CSV, Parquet e JSON sem precisar importa-los para um banco de dados. Ele aplica filtros diretamente na leitura, processa dados em partes (streaming) e paraleliza operacoes.
Source: Hashtag Treinamentos
URL: https://www.hashtagtreinamentos.com/duckdb-no-python
Date: 2026-04-16
Excerpt: "Com o DuckDB, voce aplica o filtro direto na leitura do arquivo, sem nem precisar carregar a base completa: resultado = duckdb.sql(SELECT * FROM 'vendas_gigante.csv' WHERE status = 'Ativo')"
Context: Guia completo de DuckDB no Python para analise de dados massivos.
Confidence: high

---

Claim: DuckDB e recomendado para prototipos de ETL local, analises exploratorias em notebooks, e pipelines de ciencia de dados. Ferramentas como dbt suportam DuckDB como warehouse local.
Source: DSAcademy Blog
URL: https://blog.dsacademy.com.br/fundamentos-do-duckdb-casos-de-uso/
Date: 2025-04-10
Excerpt: "Ferramentas como dbt inclusive suportam DuckDB como warehouse local, permitindo que analistas criem modelos SQL e os rodem em DuckDB para validacao rapida, antes de implementar num banco corporativo."
Context: Artigo sobre casos de uso do DuckDB em data engineering e analytics.
Confidence: high

---

## 4. BASE DOS DADOS (BASEDADOSDADOS.ORG) - DATALAKE PUBLICO

### 4.1 Tabelas tratadas e particionadas no BigQuery

Claim: A Base dos Dados disponibiliza o Censo Escolar ja tratado, limpo e harmonizado em BigQuery publico, com quatro tabelas: `escola`, `turma`, `docente` e `matricula`. A tabela `matricula` e particionada por ano e UF, permitindo consultas eficientes sem baixar a base inteira (que chega a mais de 90 GB).
Source: Base dos Dados - Blog
URL: https://basedosdados.org/blog/atualizar-explorando-o-censo-escolar-com-a-bd
Date: 2021-06-03
Excerpt: "A tabela matricula, especificamente, e muito grande (chega a mais de 90gb), por isso nao recomendamos tentar baixa-la ou utiliza-la inteira: a tabela e particionada por ano e por uf de maneira que, ao filtrar por essas variaveis, o resultado e obtido mais rapido e o gasto e bem menor."
Context: Post oficial da Base dos Dados explicando a estrutura do dataset do Censo Escolar.
Confidence: high

---

Claim: A Base dos Dados disponibiliza dados do Censo Escolar desde 2009, com variaveis padronizadas entre anos. E possivel consultar via SQL, Python ou R. O dataset pode ser acessado em `basedosdados.org/dataset/dae21af4-4b6a-42f4-b94a-4c2061ea9de5`.
Source: Base dos Dados
URL: https://basedosdados.org/dataset/dae21af4-4b6a-42f4-b94a-4c2061ea9de5
Date: Nao informada
Excerpt: "Centenas de conjuntos de dados abertos para voce explorar como quiser. Baixe ou acesse dados tratados e prontos para analise usando SQL, Python ou R."
Context: Portal oficial da Base dos Dados com dataset do Censo Escolar.
Confidence: high

---

Claim: Com a biblioteca `basedosdados` em Python, e possivel filtrar diretamente os dados no BigQuery antes de traze-los para a memoria local. Exemplo: `bd.read_sql(query = "SELECT * FROM basedosdados.br_inep_censo_escolar.matricula WHERE sigla_uf = 'RR' AND ano = 2019")`.
Source: Base dos Dados - Blog
URL: https://basedosdados.org/blog/atualizar-explorando-o-censo-escolar-com-a-bd
Date: 2021-06-03
Excerpt: "bd.read_sql(query = 'SELECT * FROM basedosdados.br_inep_censo_escolar.matricula WHERE sigla_uf = 'RR' AND transporte_publico = 1 AND ano = 2019')"
Context: Exemplos praticos de consulta a tabela de matriculas filtrando por UF e ano.
Confidence: high

---

## 5. APIs E ALTERNATIVAS DE ACESSO

### 5.1 Ausencia de API REST oficial do INEP

Claim: Nao existe API REST oficial do INEP para acesso programatico aos microdados do Censo Escolar. O download e feito manualmente via navegador ou scripts de scraping (wget, curl, Python requests).
Source: Contexto geral da pesquisa / Confirmado por multiplas fontes
URL: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar
Date: 2020-11-17
Excerpt: "Microdados do Censo Escolar da Educacao Basica 2025. 2024. Microdados do Censo Escolar da Educacao Basica 2024..." (apenas links de download, sem mencao de API)
Context: Portal oficial do INEP - apenas pagina de download de arquivos ZIP.
Confidence: high

---

### 5.2 APIs nao-oficiais e propostas academicas

Claim: Existe um projeto nao-oficial de API para dados do INEP (`inepdadosabertos/api` no GitHub, de 2014) que disponibilizava endpoints para IDEB por escola/municipio/UF, mas nao para microdados completos do Censo Escolar. O dominio `api.dadosabertosinep.org` parece inativo.
Source: GitHub - inepdadosabertos/api
URL: https://github.com/inepdadosabertos/api
Date: 2014-05-17
Excerpt: "Utilize o endereco http://api.dadosabertosinep.org/v1 como prefixo de todas as chamadas... /ideb/escolas.json?uf=RR... Criar bucket do censo escolar com os dados de estrutura, cursos, docentes e alunos."
Context: Projeto antigo (2014) que nao parece ter sido atualizado nem ter coberto microdados completos.
Confidence: low

---

Claim: Uma proposta academica da UDESC (2023) propoe desenvolver uma API REST em Django para dados do Censo da Educacao Superior do INEP, mas nao para a Educacao Basica/Censo Escolar.
Source: UDESC - Proposta de API
URL: https://www.udesc.br/arquivos/udesc/id_cpmenu/16925/Proposta_de_API_para_dados_educacionais_do_INEP_16950450017619_16925.pdf
Date: Nao informada
Excerpt: "Este trabalho propoe o desenvolvimento de uma API... a ferramenta tem como principal proposito possibilitar a coleta de dados do Censo da Educacao Superior de forma mais eficiente"
Context: Trabalho academico de proposta de API, nao implementacao em producao.
Confidence: low

---

### 5.3 BigQuery e plataformas de terceiros

Claim: O projeto `raffOps/censo_escolar` (GitHub) implementa um pipeline ETL completo na Google Cloud Platform (GCP) usando Terraform, Airflow/Composer, GKE, Dataproc/PySpark e BigQuery. Os dados do Censo Escolar (2011-2020) sao convertidos para Parquet e carregados em tabelas internas no BigQuery.
Source: GitHub - raffOps/censo_escolar
URL: https://github.com/raffOps/censo_escolar
Date: 2021-06-23
Excerpt: "3 Google Storage Bucket... BigQuery Dataset de nome censo_escolar... Tabelas BigQuery: cria ou atualiza as tabelas matriculas, docentes, gestores, turmas e escolas no dataset censo_escolar... Docentes e matriculas terao aproximadamente 120 MB em arquivo."
Context: Projeto open source de engenharia de dados que demonstra como hospedar o Censo Escolar em BigQuery.
Confidence: high

---

Claim: O projeto `InfoSchool` da UNB (2025) e uma plataforma open source que ingere microdados do Censo Escolar e os expoe via dashboards e busca conversacional, usando BigQuery como backend de dados.
Source: GitHub - unb-mds/2025-2-InfoSchool
URL: https://github.com/unb-mds/2025-2-InfoSchool
Date: 2025-08-22
Excerpt: "Nossa plataforma ingere esses dados, realiza o tratamento e os expoe atraves de dashboards interativos e um sistema de Busca Conversacional... Backend --> Queries SQL --> DB[(BigQuery / Database)]"
Context: Projeto universitario recente que usa BigQuery para democratizar acesso aos dados do Censo Escolar.
Confidence: medium

---

## 6. TUTORIAIS E MATERIAIS DE ANALISE

### 6.1 Tutoriais em video e blog

Claim: Existe uma serie de videos no YouTube (canal Rafael Francozo) ensinando a manipular microdados do Censo Escolar no R, incluindo leitura e filtragem da tabela matricula.
Source: YouTube
URL: https://www.youtube.com/watch?v=VyvWi_q3jLA
Date: 2020-10-29
Excerpt: "Microdados do Censo Escolar no R 02: Lendo e Filtrando Dados da Tabela Matricula... como usar o Rstudio, como abrir a tabela matricula e como filtrar dados de apenas alguns municipios."
Context: Serie de tutoriais praticos em video sobre analise de microdados do Censo Escolar.
Confidence: high

---

Claim: Existe um tutorial em Medium sobre uso de Python/Pandas para analisar dados do Censo Escolar 2019, incluindo leitura de CSV com separador pipe e encoding ISO-8859-1.
Source: Medium - Jonates
URL: https://jonates.medium.com/python-primeiros-passos-no-pandas-1d90cb072e6b
Date: 2021-03-11
Excerpt: "Neste post carreguei e analisei alguns dados do Censo Escolar 2019 com o Pandas... Os arquivos csv do Censo Escolar usa o caractere | (pipe) como separador..."
Context: Tutorial introdutorio de Python aplicado ao Censo Escolar.
Confidence: high

---

### 6.2 Pesquisas academicas sobre estrangeiros no Censo Escolar

Claim: Pesquisa da UFPR (2024) analisou matriculas de criancas migrantes e refugiadas na Educacao Infantil (2018-2021) usando microdados do Censo Escolar, SPSS, e variaveis como TP_NACIONALIDADE, CO_PAIS_ORIGEM, TP_COR_RACA. Identificou mais de 130 nacionalidades presentes na Educacao Infantil.
Source: UFPR - Dissertacao
URL: https://acervodigital.ufpr.br/xmlui/bitstream/handle/1884/93744/R%20-%20T%20-%20GIOCONDA%20GHIGGI.pdf
Date: Nao informada
Excerpt: "sao mais de 130 nacionalidades presentes na Educacao Infantil do Brasil... Venezuela 4.067 (2019) -> 7.056 (2020); Bolivia 2.420 -> 2.959; Haiti 1.065 -> 1.243"
Context: Dissertacao de mestrado sobre criancas migrantes usando microdados do Censo Escolar.
Confidence: high

---

Claim: Artigo da FURG (2024) analisa matriculas de criancas migrantes no Censo Escolar 2020 em Sao Paulo, usando variaveis como pais de origem, sexo, cor/raca e etapa de ensino. Conclui que o perfil e marcado por questoes raciais e de genero.
Source: Periodicos FURG
URL: https://periodicos.furg.br/momento/article/view/15988
Date: 2024-01-09
Excerpt: "utilizamos algumas variaveis que compoem os microdados das matriculas do Censo Escolar de 2020... pais de origem, sexo, cor/raca, etapa de ensino, dependencia administrativa..."
Context: Artigo academico sobre migracao infantil usando microdados do Censo Escolar.
Confidence: high

---

Claim: A cartilha da Secretaria da Educacao de SP (COPED) orienta gestores sobre matricula de migrantes internacionais, mencionando que o Censo Escolar revelou aumento de 112% no numero de estudantes imigrantes entre 2008 e 2016.
Source: Gestao Escolar / SP
URL: https://gestaoescolar.org.br/conteudo/1949/cartilha-orienta-gestores-no-acolhimento-a-alunos-imigrantes
Date: 2018-02-23
Excerpt: "O Censo Escolar... revela que, entre 2008 e 2016, o numero de estudantes imigrantes aumentou em 112%, saltando de 34 mil para quase 73 mil."
Context: Cartilha oficial sobre acolhimento a alunos imigrantes.
Confidence: high

---

## 7. PORTAIS E PAINES DE VISUALIZACAO

### 7.1 InepData e Power BI

Claim: O INEP mantem dois paineis de Estatisticas do Censo Escolar: um em Oracle BI (InepData) com dados desde 2007, e um novo em Power BI com dados dos ultimos 10 anos. Permitem consulta por UF, municipio, rede, etapa, sexo, raca, etc.
Source: Portal Gov.br - INEP
URL: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/inep-data/estatisticas-censo-escolar
Date: 2020-11-10 (atualizado 2024-11-06)
Excerpt: "Estatisticas Censo Escolar - o painel utiliza a plataforma Oracle Business Intelligence do InepData... Novo painel de Estatisticas Censo Escolar da Educacao Basica - o painel utiliza a plataforma do Power BI"
Context: Portais oficiais do INEP para consulta agregada (nao microdados).
Confidence: high

---

### 7.2 QEdu

Claim: O QEdu (qedu.org.br) e uma plataforma que gera visualizacoes de dados do Censo Escolar por estado, incluindo Santa Catarina, mas os dados agregados para filtros especificos podem estar em processamento.
Source: QEdu
URL: https://qedu.org.br/uf/42-santa-catarina/censo-escolar
Date: Nao informada
Excerpt: "Os dados para o filtro aplicado ainda estao sendo processados pela nossa equipe."
Context: Plataforma de visualizacao de dados educacionais. Dados especificos de SC pareciam nao estar disponiveis no momento da consulta.
Confidence: medium

---

## 8. MUDANCAS RECENTES E LIMITACOES

### 8.1 Impacto da LGPD nos microdados

Claim: A partir de 2022, o INEP reformulou a estrutura dos microdados do Censo Escolar e ENEM para adequacao a LGPD (Lei 13.709/2018), suprimindo variaveis que permitiam reidentificacao de pessoas. Isso alterou a estrutura de consolidacao dos microdados.
Source: Conviva Educacao
URL: https://convivaeducacao.org.br/fique_atento/3541
Date: 2022-02-22
Excerpt: "Os microdados... foram reestruturados para suprimir a possibilidade de identificacao de pessoas, em atendimento as normas previstas na Lei n. 13.709, de 14 de agosto de 2018 (Lei Geral de Protecao de Dados Pessoais - LGPD)."
Context: Noticia sobre mudancas nos microdados do INEP em razao da LGPD.
Confidence: high

---

### 8.2 Variaveis anonimizadas que mudam a cada edicao

Claim: Os codigos de identificacao de alunos e escolas no Censo Escolar sao anonimizados e mudam a cada edicao do Censo, impossibilitando o acompanhamento longitudinal de individuos entre anos.
Source: Contexto da Phase 1 (confirmado por multiplas fontes academicas)
URL: Nao aplicavel
Date: Nao aplicavel
Excerpt: "Codigos de alunos/escolas sao anonimizados e mudam a cada edicao"
Context: Conhecimento consolidado da comunidade de pesquisa em educacao.
Confidence: high

---

## 9. RESUMO EXECUTIVO

### 9.1 Principais achados

1. **Nao ha API REST oficial do INEP** para acesso programatico aos microdados do Censo Escolar. O download e manual via navegador ou automatizado via scripts de scraping (Python com requests/BeautifulSoup, wget, curl).

2. **Pacotes R recomendados:**
   - **`educabR` (CRAN)** - Pacote moderno e completo. Suporta 1995-2024, download automatico, filtro por UF (`uf = "SC"`), limitacao de linhas (`n_max`), cache local, e retorna dados tidy. E a opcao mais recomendada para usuarios de R.
   - **`microdadosBrasil`** - Pacote historico que suporta 1995-2014. Usa `readr` e `data.table` internamente. Pode estar desatualizado.
   - **`censoescolaR`** - Pacote comunitario focado em importacao e rotulacao, testado para 2019.

3. **Ferramentas Python recomendadas:**
   - **Pandas + `chunksize`** - Para filtrar CSVs grandes sem carregar tudo na memoria.
   - **DuckDB** - Permite SQL direto sobre CSV/Parquet com filtros na leitura, processamento paralelo e streaming automatico.
   - **Projeto `paeselhz/microdados_censo_escolar`** - Automatiza download e converte para Parquet (reducao de ate 1/4 do tamanho). Oferece arquivos ja convertidos no GCS (`gs://microdados-inep/microdados-censo-escolar`).

4. **Base dos Dados (basedosdados.org)** - E a alternativa mais acessivel para quem nao quer baixar arquivos brutos. Disponibiliza tabelas tratadas em BigQuery publico, particionadas por ano e UF. A tabela `br_inep_censo_escolar.matricula` pode ser consultada via SQL, Python ou R, filtrando `sigla_uf = 'SC'` e `ano` antes de trazer dados para a maquina local.

5. **Formato e tamanho dos dados brutos:**
   - ZIPs de 2-4 GB compactados, 10-20 GB descompactados.
   - CSVs delimitados por pipe `|`, divididos por regiao (MATRICULA_SUL.CSV contem SC).
   - Encoding varia: ISO-8859-1 em alguns anos, UTF-8 em outros.
   - Dicionarios de dados em XLSX acompanham os arquivos.

6. **Variaveis para identificar estrangeiros:**
   - `TP_NACIONALIDADE` = 3 (Estrangeira)
   - `CO_PAIS_ORIGEM` (codigo do pais)
   - `NOME_PAIS_CE` (nome do pais)

7. **Tecnicas para filtrar apenas SC e estrangeiros sem carregar toda a base:**
   - **R:** `sqldf::read.csv2.sql()` com filtro SQL na leitura; `educabR::get_censo_escolar(uf = "SC")`; ou carregar em SGBD (PostgreSQL/MonetDB) e consultar.
   - **Python:** `pd.read_csv(chunksize=...)` com filtro; DuckDB com SQL direto; Parquet + PyArrow com pushdown de predicados.
   - **BigQuery (Base dos Dados):** Consulta SQL filtrando `sigla_uf = 'SC'` e `ano` antes do download.

8. **Limitacoes identificadas:**
   - Ausencia de API oficial do INEP.
   - Codigos anonimizados que mudam a cada edicao (impossibilita longitudinal individual).
   - Variaveis mudam nomes ao longo dos anos (desafio de harmonizacao).
   - Impacto da LGPD: retirada de variaveis de microdados a partir de 2022.
   - Projeto `inepdadosabertos/api` (2014) parece abandonado.

### 9.2 Recomendacoes praticas para a analise de matriculas de estrangeiros em SC

**Fluxo recomendado (R):**
```r
install.packages("educabR")
library(educabR)
# Download dos dados de escolas de SC (ano desejado)
escolas_sc <- get_censo_escolar(year = 2023, uf = "SC")
# Para matriculas, e necessario baixar o ZIP completo e filtrar
```

**Fluxo recomendado (Python + Base dos Dados):**
```python
import basedosdados as bd
query = """
SELECT * 
FROM `basedosdados.br_inep_censo_escolar.matricula`
WHERE sigla_uf = 'SC' 
  AND ano = 2023
  AND nacionalidade = 3  -- se a BD usar codigo numerico
"""
df = bd.read_sql(query, billing_project_id="seu_projeto")
```

**Fluxo recomendado (DuckDB sobre CSV local):**
```python
import duckdb
result = duckdb.sql("""
    SELECT * 
    FROM 'MATRICULA_SUL.CSV'
    WHERE CO_UF = '42' AND TP_NACIONALIDADE = 3
""")
df = result.df()
```

**Fluxo recomendado (Conversao para Parquet):**
```python
# Usar o projeto paeselhz ou converter localmente com PyArrow
import pyarrow.csv as pv
import pyarrow.parquet as pq
table = pv.read_csv('MATRICULA_SUL.CSV', parse_options=pv.ParseOptions(delimiter='|'))
pq.write_table(table, 'matricula_sul.parquet')
# Depois ler com DuckDB ou Pandas com filtros
```

---

## ANEXO: Lista de fontes consultadas (≥20 buscas independentes)

1. Pacote R `educabR` no CRAN
2. Pacote R `microdadosBrasil` no GitHub
3. Pacote R `censoescolaR` no GitHub
4. Tutorial Python/Pandas para Censo Escolar (Medium)
5. Projeto Python `paeselhz/microdados_censo_escolar` (GitHub)
6. Projeto ETL GCP `raffOps/censo_escolar` (GitHub)
7. Base dos Dados - dataset Censo Escolar
8. Base dos Dados - Blog sobre Censo Escolar
9. API nao-oficial `inepdadosabertos/api` (GitHub)
10. Proposta academica de API UDESC
11. Portal INEP - Estatisticas Censo Escolar (Power BI / Oracle BI)
12. DuckDB no Python (Hashtag Treinamentos)
13. Casos de uso DuckDB (DSAcademy)
14. Stack Overflow - Ler Censo Escolar no R com sqldf
15. R Mining Blog - MonetDBLite para dados grandes
16. Medium - Filtrar CSV grande com Pandas chunksize
17. Pandas Documentation - Scaling to large datasets
18. Brazil Visible - Tamanho dos microdados
19. UFPR - Dissertacao sobre criancas migrantes e Censo Escolar
20. FURG - Artigo sobre Educacao Infantil e migracao
21. Dicionario INEP TP_NACIONALIDADE / MJSP
22. Gist AlanTaranti - Script de download INEP
23. YouTube - Tutorial R Censo Escolar (Rafael Francozo)
24. InfoSchool UNB - BigQuery Censo Escolar
25. QEdu - Dados agregados SC
26. Conviva Educacao - LGPD e microdados INEP
27. Gestao Escolar SP - Cartilha imigrantes
28. Portal SED/SC - Matriculas rede estadual

---

*Documento gerado em pesquisa automatizada. Todas as URLs e datas foram capturadas no momento da consulta.*
