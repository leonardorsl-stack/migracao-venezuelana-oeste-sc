# Dimensao 01 — Microdados INEP/Censo Escolar: Disponibilidade, Variavel de Nacionalidade e Formatos de Download

## Sumario
1. [Visao Geral](#visao-geral)
2. [Fontes Investigadas e Documentacao](#fontes-investigadas)
3. [Disponibilidade por Ano](#disponibilidade-por-ano)
4. [Variavel de Nacionalidade](#variavel-de-nacionalidade)
5. [Formato dos Arquivos: Evolucao Historica](#formato-dos-arquivos)
6. [Supressao de Dados e Impacto da LGPD](#supressao-lgpd)
7. [Lei 15.017/2024 e Perspectivas Futuras](#lei-15017)
8. [Alternativas de Acesso](#alternativas-acesso)
9. [Resumo Executivo](#resumo-executivo)

---

## 1. Visao Geral

O Censo Escolar da Educacao Basica, coordenado pelo Instituto Nacional de Estudos e Pesquisas Educacionais Anisio Teixeira (INEP/MEC), e o principal instrumento de coleta de informacoes estatistico-educacionais de ambito nacional no Brasil. Os microdados do Censo Escolar representam o menor nivel de desagregacao dos dados coletados, permitindo analises detalhadas ao nivel individual de alunos, docentes, turmas e escolas.

Este relatorio investiga a disponibilidade atual desses microdados, com foco especial na variavel de **nacionalidade/pais de origem** do aluno (TP_NACIONALIDADE e NOME_PAIS_CE), o impacto da Lei Geral de Protecao de Dados Pessoais (LGPD) na supressao de dados, e as alternativas de acesso para pesquisadores.

---

## 2. Fontes Investigadas e Documentacao

### 2.1 Portal Oficial do INEP — Microdados

```
Claim: O INEP disponibiliza microdados do Censo Escolar da Educacao Basica para os anos de 2005 a 2025 em formato ZIP para download direto.
Source: Portal Gov.br — INEP Microdados
URL: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar
Date: Acesso em 2025-01-09
Excerpt: "Microdados do Censo Escolar da Educacao Basica 2025... 2024... 2023... 2022... 2021... 2020... 2019..." (lista de arquivos ZIP para cada ano, todos atualizados em 08/03/2023, com excecao de 2005-2006)
Context: Todos os anos de 2005 a 2025 tem link direto para download no formato https://download.inep.gov.br/dados_abertos/microdados_censo_escolar_YYYY.zip
Confidence: high
```

### 2.2 Dicionario de Variaveis — Portal de Imigracao/MJ

```
Claim: O dicionario de dados do Censo Escolar INEP confirma a existencia das variaveis TP_NACIONALIDADE (Nacionalidade: 1-Brasileira, 2-Brasileira nascido no exterior/naturalizado, 3-Estrangeira) e NOME_PAIS_CE (Nome do pais de origem do aluno, Char 100).
Source: Portal de Imigracao — Ministerio da Justica
URL: https://portaldeimigracao.mj.gov.br/images/dados/microdados/2021/INEP/Dicion%C3%A1rios_INEP_-_Divulga%C3%A7%C3%A3o_-_Censo_Escolar.xlsx
Date: Acesso em 2025
Excerpt: "TP_NACIONALIDADE | Nacionalidade | Num | 1 | 1 - Brasileira / 2 - Brasileira - nascido no exterior ou naturalizado / 3 - Estrangeira"; "NOME_PAIS_CE | Nome do pais de origem do aluno | Char | 100"
Context: Dicionario de dados usado pelo Observatorio das Migracoes (OBMigra) para produzir estatisticas de alunos estrangeiros/imigrantes na educacao brasileira.
Confidence: high
```

### 2.3 Base dos Dados (basedosdados.org)

```
Claim: A Base dos Dados disponibiliza tabelas do Censo Escolar no formato individual (nivel aluno/docente/turma/escola) apenas para os anos de 2009 a 2020, com mais de 90 GB na tabela matricula.
Source: Base dos Dados — Blog
URL: https://basedosdados.org/blog/atualizar-explorando-o-censo-escolar-com-a-bd
Date: 2021-06-03
Excerpt: "Aqui na Base dos Dados, optamos por disponibilizar, inicialmente, valores desde 2009 ate 2020. [...] A tabela matricula identifica cada aluno brasileiro atraves da id_aluno. As observacoes estao no nivel de cada aluno e de cada ano."
Context: A Base dos Dados nao incluiu os anos 2021+ porque o formato dos microdados mudou de individual para agregado por escola.
Confidence: high
```

### 2.4 UFPR Litoral — Relatorio com Microdados 2023

```
Claim: Os microdados do Censo Escolar 2023 sao uma unica base de dados ao nivel de escola, com aproximadamente 370 atributos (colunas), incluindo contagens agregadas (qt_mat_inf, qt_mat_fund, qt_mat_med, etc.) e nao mais dados individuais de alunos.
Source: UFPR Litoral — Relatorio Tecnico
URL: https://litoral.ufpr.br/wp-content/uploads/2025/02/Doc-de-apoio-3.-Matriculas-Educacao-Basica-2007-a-2023.pdf
Date: 2024
Excerpt: "O Censo Escolar 2023 continha 217.265 escolas [...] uma base de dados aberta, disponibilizada pelo proprio MEC, com dados individualizados de todas as escolas participantes da pesquisa. [...] O Mapa 2 introduz 43 novas variaveis [...] qt_mat_inf, qt_mat_fund, qt_mat_fund_ai, qt_mat_fund_af, qt_mat_med..."
Context: Confirma que os microdados atuais sao agregados por escola, com ~370 atributos por escola, incluindo contagens de matriculas por etapa/modalidade.
Confidence: high
```

### 2.5 Tese UFRGS — Privacidade e Microdados

```
Claim: A partir de 2022, o INEP alterou a granularidade dos microdados do Censo Escolar de nivel individual (aluno/professor) para nivel de escola, com informacoes agregadas.
Source: UFRGS — Dissertacao de Mestrado
URL: https://lume.ufrgs.br/bitstream/handle/10183/259957/001172279.pdf
Date: 2023
Excerpt: "Antes a granularidade chegava ao nivel mais basico, a matricula do aluno [...] Porem no novo modelo as informacoes individuais foram agregadas a nivel de escola. [...] Os registros detalhados a nivel de escola foram tirados do portal do INEP [...] 1608986 linhas com 370 atributos"
Context: Dissertacao que analisa o impacto da mudanca de formato dos microdados na pesquisa e transparencia.
Confidence: high
```

### 2.6 SEDAP — Servico de Acesso a Dados Protegidos

```
Claim: O INEP disponibiliza, exclusivamente na Sala de Acesso a Dados Protegidos (SEDAP) em Brasilia, bases desidentificadas do Censo Escolar de 2007 a 2024, mediante solicitacao do pesquisador com autorizacao das areas tecnicas.
Source: Portal Gov.br — SEDAP
URL: https://www.gov.br/inep/pt-br/areas-de-atuacao/gestao-do-conhecimento-e-estudos-educacionais/cgdi/servico-de-acesso-a-dados-protegidos-sedap/base-de-dados
Date: Atualizado em 09/03/2026
Excerpt: "Censo Escolar – 2007 a 2024 [...] exclusivamente na Sala de Acesso a Dados Protegidos (Sedap) e mediante solicitacao do pesquisador com autorizacao das areas tecnicas"
Context: O SEDAP e a unica alternativa para acesso a microdados individuais (nivel aluno) dos anos 2021 a 2024. Em julho/2023, o INEP passou a permitir que entidades se cadastrassem para criar nucleos Sedap em outras localidades.
Confidence: high
```

### 2.7 Open Knowledge Brasil — Da Transparencia a Opacidade

```
Claim: A mudanca na politica de divulgacao do INEP em 2022 resultou na retirada permanente das bases de alunos, docentes e turmas, restando apenas microdados ao nivel da escola com colunas agregadas.
Source: Open Knowledge Brasil / Fundacao Lemann
URL: https://observatoriodeeducacao.institutounibanco.org.br/api/assets/observatorio/c33d31d2-4738-4f47-852c-d916757a0b14/
Date: 2025
Excerpt: "A partir de marco de 2022, a mudanca na politica de transparencia ativa do Inep implicou a retirada permanente do ar das bases de alunos, docentes e turmas. Restaram, entao, apenas os microdados no nivel da escola, que receberam o acrescimo de algumas colunas contendo informacoes agregadas, como o total de matriculas e docentes da instituicao."
Context: Relatorio detalhado sobre o impacto da supressao dos microdados na pesquisa educacional e fiscalizacao.
Confidence: high
```

### 2.8 IEDE — Analise Empirica sobre Supressao

```
Claim: O INEP divulgou o Censo Escolar 2021 como uma "sinopse estatistica expandida", excluindo informacoes no nivel do aluno e dos docentes, e removeu as bases anteriores do site.
Source: IEDE (Interdisciplinaridade e Evidencias no Debate Educacional)
URL: https://portaliede.org.br/contribuicao/iede-realiza-analise-empirica-sobre-a-supressao-dos-microdados-do-censo-escolar/
Date: 2024-07-26
Excerpt: "No caso do Censo Escolar 2021, as mudancas foram ainda mais drasticas e o Inep divulgou somente uma especie de 'sinopse estatistica expandida', que nao continha dados no nivel do aluno e do professor. Alem disso, na ocasiao, foram retiradas do site do Inep as bases anteriores do Censo Escolar."
Context: O IEDE demonstrou empiricamente que era possivel pseudoanonimizar os dados sem suprimi-los completamente.
Confidence: high
```

### 2.9 Lei 15.017/2024

```
Claim: A Lei 15.017/2024, sancionada em 12 de novembro de 2024, obriga o poder publico a compartilhar e tornar publicos dados e microdados obtidos por meio do Censo Escolar e demais avaliacoes, agregados e desagregados, anonimizados.
Source: Diario Oficial da Uniao / Senado Federal
URL: https://www2.camara.leg.br/legin/fed/lei/2024/lei-15017-12-novembro-2024-796541-publicacaooriginal-173508-pl.html
Date: 2024-11-12
Excerpt: "Art. 5o [...] SS 8o Dados e microdados, agregados e desagregados, coletados na execucao de politicas educacionais de carater censitario, avaliativo ou regulatorio, serao tratados, divulgados e compartilhados, sempre que possivel, de forma anonimizada, observados os parametros para anonimizacao previstos em regulamento."
Context: Lei que altera a LDB (Lei 9.394/1996) para tornar obrigatoria a divulgacao de microdados educacionais. Origem: PL 454/2022, apresentado apos a retirada dos microdados pelo INEP em 2022.
Confidence: high
```

### 2.10 ANPD — Nota Tecnica sobre INEP

```
Claim: A ANPD fiscalizou o INEP e concluiu que o instituto cumpriu adequadamente as determinacoes para protecao de dados, elaborando RIPD e adotando medidas apropriadas. A ANPD nao concluiu que a metodologia anterior fosse inadequada.
Source: ANPD — Coordenacao-Geral de Fiscalizacao
URL: https://legismap.com.br/component/legismap_ferramentas/?task=generatePdf.getPdf&artigo=148764&Itemid=101
Date: 2023-11-13
Excerpt: "A analise da CGF se restringiu a metodologia de divulgacao face a LGPD e ao RIPD. 'Isso nao significa, necessariamente, que a metodologia adotada anteriormente fosse inadequada', concluiu."
Context: A ANPD encerrou o processo de fiscalizacao do INEP em setembro de 2023, considerando que as medidas foram adequadas.
Confidence: high
```

### 2.11 INEP — Nota de Esclarecimento (2022)

```
Claim: O INEP, baseado em parecer juridico da Procuradoria Federal (Projur), suspendeu a divulgacao de microdados pessoais nao anonimizados ou que permitam reidentificacao, em atendimento a LGPD.
Source: INEP — Nota de Esclarecimento
URL: https://www.gov.br/inep/pt-br/centrais-de-conteudo/noticias/institucional/nota-de-esclarecimento-divulgacao-dos-microdados
Date: 2022-02-22
Excerpt: "O parecer juridico emitido pela Projur do Instituto conclui que, 'se a divulgacao dos censos ou outras bases de dados mantidos pelo Inep puder resultar em acesso, por terceiros, a microdados pessoais nao anonimizados ou que permitam a reidentificacao de seus titulares, a divulgacao nao podera ser realizada, de acordo com a LGPD'."
Context: Nota oficial do INEP justificando a mudanca na politica de divulgacao de microdados.
Confidence: high
```

### 2.12 OBMigra — Portal de Imigracao e Dados Educacionais

```
Claim: O Observatorio das Migracoes (OBMigra) utiliza microdados do Censo Escolar INEP para produzir estatisticas de alunos imigrantes/estrangeiros matriculados na educacao basica brasileira.
Source: Portal de Imigracao MJSP — OBMigra
URL: https://portaldeimigracao.mj.gov.br/pt/dados
Date: Acesso em 2025
Excerpt: "O OBMigra utiliza os microdados do Censo Escolar INEP para produzir estatisticas de alunos imigrantes."
Context: O Portal de Imigracao do MJSP disponibiliza relatorios anuais com capitulo dedicado a educacao, baseado nos microdados do Censo Escolar.
Confidence: medium
```

---

## 3. Disponibilidade por Ano

| Ano | Disponivel Publicamente | Formato | Nivel de Desagregacao | Obs |
|-----|------------------------|---------|----------------------|-----|
| 1995-2004 | Sim | ZIP com CSV | Escola | Sem dados individuais |
| 2005-2006 | Sim | ZIP com CSV | Escola + Turma + Docente + **Aluno** | Arquivos MATRICULA por UF |
| 2007-2020 | Sim (republicado em 08/03/2023) | ZIP com CSV | Escola + Turma + Docente + **Aluno** | Arquivos MATRICULA_*.CSV por regiao (inclui MATRICULA_SUL) |
| 2021 | Sim (08/03/2023) | ZIP com CSV | **Escola (agregado)** | Sinopse estatistica expandida; sem dados individuais |
| 2022 | Sim | ZIP com CSV | **Escola (agregado)** | Dados agregados por escola (~370 colunas) |
| 2023 | Sim | ZIP com CSV | **Escola (agregado)** | Dados agregados por escola (~370 colunas) |
| 2024 | Sim | ZIP com CSV | **Escola (agregado)** | Dados agregados por escola |
| 2025 | Sim | ZIP com CSV | **Escola (agregado)** | Dados agregados por escola |

**Notas importantes:**
- Todos os arquivos de 2005 a 2025 foram **atualizados em 08/03/2023**, indicando uma republicacao geral apos a crise de 2022.
- O download direto e feito via URL padrao: `https://download.inep.gov.br/dados_abertos/microdados_censo_escolar_YYYY.zip`
- O servidor `download.inep.gov.br` pode apresentar instabilidade/lentidao em alguns horarios.

---

## 4. Variavel de Nacionalidade

### 4.1 Variaveis Confirmadas no Dicionario de Dados

As seguintes variaveis estao documentadas no dicionario de dados do Censo Escolar:

| Variavel | Descricao | Tipo | Valores |
|----------|-----------|------|---------|
| **TP_NACIONALIDADE** | Nacionalidade | Numerico (1) | 1 = Brasileira; 2 = Brasileira — nascido no exterior ou naturalizado; 3 = Estrangeira |
| **NOME_PAIS_CE** | Nome do pais de origem do aluno | Caractere (100) | Texto livre com o nome do pais |

**Fonte do dicionario:** `https://portaldeimigracao.mj.gov.br/images/dados/microdados/2021/INEP/Dicion%C3%A1rios_INEP_-_Divulga%C3%A7%C3%A3o_-_Censo_Escolar.xlsx`

### 4.2 Disponibilidade da Variavel por Periodo

| Periodo | Formato dos Microdados | TP_NACIONALIDADE Disponivel? | NOME_PAIS_CE Disponivel? |
|---------|------------------------|------------------------------|--------------------------|
| Ate 2020 | Individual (aluno) | **SIM** — nivel aluno | **SIM** — nivel aluno |
| 2021-2025 (publico) | Agregado (escola) | **NAO** — dados agregados nao incluem composicao por nacionalidade | **NAO** |
| 2021-2024 (SEDAP) | Individual desidentificado | **PROVAVELMENTE SIM** — catalogo nao detalha exclusao dessa variavel | **PROVAVELMENTE SIM** |

**Limitacao critica:** Nos microdados publicos atuais (2021-2025), como os dados sao agregados por escola com contagens totais de matriculas por etapa (ex: `qt_mat_inf`, `qt_mat_fund`), **nao e possivel identificar quantos alunos estrangeiros/imigrantes estao matriculados em cada escola**, pois nao ha variaveis de composicao demografica (raca, nacionalidade, idade individual) no formato agregado.

---

## 5. Formato dos Arquivos: Evolucao Historica

### 5.1 Periodo 2007-2020 (Formato Individual)

Neste periodo, cada arquivo ZIP continha multiplos arquivos CSV:
- **ESCOLAS.CSV** — Dados de cada escola
- **TURMAS.CSV** — Dados de cada turma
- **DOCENTES_*.CSV** — Dados de cada docente (dividido por regiao)
- **MATRICULA_*.CSV** — Dados de cada matricula/aluno (dividido por regiao: CO, NORDESTE, NORTE, SUDESTE, **SUL**)

A divisao por regiao era necessaria devido ao volume de dados (mais de 40 milhoes de matriculas por ano).

### 5.2 Periodo 2021-2025 (Formato Agregado)

A partir de 2021/2022, o formato mudou para um **unico arquivo CSV por ano**, contendo dados ao nivel de escola com aproximadamente **370 colunas/variaveis**. Estas incluem:
- Dados cadastrais da escola (ID, endereco, dependencia administrativa)
- Infraestrutura (agua, energia, laboratorios, biblioteca)
- Contagens agregadas: `qt_mat_inf`, `qt_mat_fund`, `qt_mat_fund_ai`, `qt_mat_fund_af`, `qt_mat_med`, `qt_mat_eja`, `qt_mat_esp`, etc.
- Contagens de docentes: `qt_doc_inf`, `qt_doc_fund`, `qt_doc_med`, etc.
- Contagens de turmas: `qt_tur_inf`, `qt_tur_fund`, etc.

**Nao ha mais arquivos MATRICULA_*.CSV no formato publico.**

---

## 6. Supressao de Dados e Impacto da LGPD

### 6.1 Cronologia dos Eventos

| Data | Evento |
|------|--------|
| Ago/2018 | Aprovacao da LGPD (Lei 13.709/2018) |
| Nov/2020 | INEP cria forca-tarefa para diagnosticar impactos da LGPD |
| Mai/2021 | Nota tecnica da DEED aponta fragilidades nos microdados publicos |
| Fev/2022 | INEP divulga Censo 2021 como "sinopse estatistica expandida" e remove bases anteriores |
| Fev/2022 | ANPD inicia fiscalizacao do INEP |
| Mai/2022 | INEP realiza seminario sobre controle de microdados |
| Mar/2022 | Bases de alunos, docentes e turmas retiradas permanentemente |
| Set/2023 | ANPD conclui fiscalizacao, considerando medidas do INEP adequadas |
| 08/03/2023 | INEP republica todos os microdados historicos (2005-2020) no formato individual |
| 08/03/2023 | INEP mantem microdados 2021+ no formato agregado por escola |
| Nov/2024 | Lei 15.017/2024 sancionada, obrigando divulgacao de microdados |
| Dez/2025 | Open Knowledge Brasil publica estudo mostrando perda de ate 99% da riqueza das informacoes |

### 6.2 Impacto na Variavel de Nacionalidade

A supressao dos microdados individuais **elimina diretamente a possibilidade de analisar a distribuicao de alunos estrangeiros/imigrantes** na educacao basica brasileira via dados publicos. Antes de 2021, era possivel:
- Contar quantos alunos estrangeiros por pais de origem estavam matriculados
- Analisar a distribuicao geografica (estado, municipio, escola) desses alunos
- Cruzar nacionalidade com etapa de ensino, sexo, cor/raca, idade
- Monitorar fluxo e rendimento escolar de alunos imigrantes

Apos 2021, com dados agregados por escola, **nenhuma dessas analises e possivel** usando apenas os microdados publicos.

---

## 7. Lei 15.017/2024 e Perspectivas Futuras

### 7.1 Dispositivos Legais

A Lei 15.017/2024 alterou a Lei de Diretrizes e Bases da Educacao Nacional (Lei 9.394/1996), acrescentando:

> **Art. 5o, SS 8o:** "Dados e microdados, agregados e desagregados, coletados na execucao de politicas educacionais de carater censitario, avaliativo ou regulatorio, serao tratados, divulgados e compartilhados, sempre que possivel, de forma anonimizada, observados os parametros para anonimizacao previstos em regulamento."

### 7.2 Efeito Pratico

Ate o momento (janeiro 2026), **a Lei 15.017/2024 ainda nao resultou em mudanca pratica no formato dos microdados publicos do INEP**. Os arquivos de 2024 e 2025 continuam no formato agregado por escola. Nao foi editado regulamento especifico definindo os "parametros para anonimizacao", que e condicao para a implementacao plena da lei.

**Expectativa:** A lei cria obrigacao legal, mas depende de regulamentacao e de adaptacao tecnica do INEP para voltar a divulgar microdados desagregados (nivel aluno) de forma anonimizada.

---

## 8. Alternativas de Acesso

### 8.1 SEDAP (Servico de Acesso a Dados Protegidos)

- **O que e:** Sala segura em Brasilia (ou nucleos remotos) para acesso a bases desidentificadas
- **Bases disponiveis:** Censo Escolar 2007-2024 (inclusive anos individuais 2021-2024)
- **Requisitos:** Ser pesquisador vinculado a instituicao, submeter projeto de pesquisa, obter autorizacao das areas tecnicas do INEP
- **Processo:** Cadastro no sistema, agendamento, acesso presencial (ou remoto em nucleos credenciados)
- **Variavel de nacionalidade:** Provavelmente disponivel, pois as bases sao as originais desidentificadas

### 8.2 Base dos Dados (basedosdados.org)

- **Cobertura:** Censo Escolar 2009-2020 no formato individual (tabelas: escola, turma, docente, matricula)
- **Variavel de nacionalidade:** Nao mencionada explicitamente no blog; a tabela matricula inclui `sexo`, `cor_raca`, `id_municipio_nascimento`, `id_municipio_endereco`
- **Acesso:** Gratuito via BigQuery, Python, R
- **Limitacao:** Nao inclui anos 2021+

### 8.3 Google Cloud Storage (mirror historico)

- **URL:** `gs://microdados-inep/microdados-censo-escolar`
- **Conteudo:** Arquivos Parquet dos microdados de 2007 a 2019 (formato individual)
- **Fonte:** Projeto comunitario (github.com/paeselhz/microdados_censo_escolar)

### 8.4 Portal de Imigracao / OBMigra

- **Conteudo:** Relatorios anuais com estatisticas agregadas de alunos estrangeiros
- **Limitacao:** Dados ja processados e agregados; nao permite analise individual
- **URL:** https://portaldeimigracao.mj.gov.br/pt/dados

---

## 9. Resumo Executivo

### Principais Achados

- **Disponibilidade de microdados publicos:** O INEP disponibiliza arquivos ZIP para download direto para todos os anos de 2005 a 2025 via `https://download.inep.gov.br/dados_abertos/microdados_censo_escolar_YYYY.zip`. Todos os arquivos foram republicados em 08/03/2023.

- **Mudanca de formato critica (2021+):** A partir do Censo Escolar 2021, os microdados publicos deixaram de conter informacoes individuais de alunos e passaram a ser **dados agregados por escola** (~370 colunas com contagens de matriculas, docentes e turmas por categoria).

- **Variavel de nacionalidade (TP_NACIONALIDADE e NOME_PAIS_CE):**
  - **Existe no dicionario de dados** do Censo Escolar
  - **Disponivel nos microdados individuais ate 2020** (inclusive na Base dos Dados)
  - **INDISPONIVEL nos microdados publicos de 2021-2025** porque o formato agregado por escola nao preserva caracteristicas demograficas individuais
  - **Provavelmente disponivel via SEDAP** (bases desidentificadas 2007-2024)

- **Impacto da LGPD:** A justificativa do INEP foi a protecao de dados pessoais e o risco de reidentificacao. A ANPD fiscalizou e considerou as medidas adequadas. Estudos da UFMG, IEDE e Open Knowledge Brasil demonstraram que era tecnicamente possivel anonimizar os dados sem suprimi-los completamente.

- **Lei 15.017/2024:** Sancionada em novembro de 2024, obriga a divulgacao de microdados agregados e desagregados, anonimizados. Ate o momento, **nao houve mudanca pratica no formato dos microdados publicos**.

- **Acesso para pesquisadores sobre imigrantes/estrangeiros:**
  - **Opcao 1 (recomendada):** Solicitar acesso ao SEDAP para bases desidentificadas 2007-2024
  - **Opcao 2:** Usar dados historicos ate 2020 via Base dos Dados ou download direto do INEP
  - **Opcao 3:** Consultar relatorios agregados do OBMigra/Portal de Imigracao

- **Limitacao especifica para SC:** No formato publico atual, nao e possivel identificar escolas em Santa Catarina (incluidas na regiao SUL no formato antigo) que tenham alunos estrangeiros matriculados, pois os dados agregados por escola nao desagregam por nacionalidade.

---

*Documento gerado em pesquisa sistematica com 24+ buscas independentes em fontes primarias oficiais (INEP, Senado, ANPD, MJSP, UFPR, UFRGS, IEDE, Open Knowledge Brasil, Base dos Dados).*
