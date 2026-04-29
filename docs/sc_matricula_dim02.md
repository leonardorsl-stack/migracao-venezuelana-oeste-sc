# Dimensão 02 — Portais Estaduais de Dados Abertos: SED-SC, dados.sc.gov.br, FCEE

**Data da pesquisa:** 2025-01-25  
**Pesquisador:** Agente de investigação em dados educacionais e transparência governamental  
**Objetivo:** Investigar portais de dados abertos de Santa Catarina (SED-SC, dados.sc.gov.br, FCEE) quanto à disponibilidade de datasets de matrícula com filtros por nacionalidade, estrangeiros ou país de origem; verificar formatos (CSV, XLS, HTML), granularidade e anos disponíveis.

---

## Índice de Fontes

1. [dados.sc.gov.br — Portal Estadual de Dados Abertos](#11-dadosscgovbr--portal-estadual-de-dados-abertos)
2. [SED-SC — Educação na Palma da Mão](#12-sed-sc--educação-na-palma-da-mão)
3. [SED-SC — Informações Educacionais e Portarias](#13-sed-sc--informações-educacionais-e-portarias)
4. [FCEE — Fundação Catarinense de Educação Especial](#14-fcee--fundação-catarinense-de-educação-especial)
5. [Programa de Acolhimento ao Migrante (PAM)](#15-programa-de-acolhimento-ao-migrante-pam)
6. [Dados sobre Estrangeiros/Imigrantes na Educação de SC](#16-dados-sobre-estrangeirosimigrantes-na-educação-de-sc)
7. [Artigos Acadêmicos e Fontes Alternativas](#17-artigos-acadêmicos-e-fontes-alternativas)
8. [Resumo Executivo](#resumo-executivo)

---

## 1.1 dados.sc.gov.br — Portal Estadual de Dados Abertos

### Claim 1.1.1: O portal dados.sc.gov.br possui 111 conjuntos de dados, 26 organizações e 27 grupos, mas apenas 4 datasets da SED-SC
**Source:** Portal de Dados Abertos SC  
**URL:** https://dados.sc.gov.br/dataset?organization=sed  
**Date:** Acesso em 2025-01-25  
**Excerpt:** "4 conjuntos de dados encontrados. Organização: Secretaria de Estado da Educação. Datasets: Avaliação Educacional, Orçamentos Públicos em Educação (SIOPE), busca de Escolas, Bolsas Universitárias."  
**Context:** A SED-SC publica apenas 4 datasets no portal estadual de dados abertos. Nenhum deles contém dados de matrículas desagregados por nacionalidade ou estrangeiros.  
**Confidence:** high

### Claim 1.1.2: O dataset "busca de Escolas" é um link HTML para consulta externa, não um arquivo baixável
**Source:** Portal de Dados Abertos SC — Dataset "busca de Escolas"  
**URL:** https://dados.sc.gov.br/dataset/busca-de-escolas  
**Date:** Última atualização: 14 de Janeiro de 2020, 06:38 (UTC+08:00)  
**Excerpt:** "Consulta de escolas públicas e privadas por município, rede e unidade escolar. Dados e recursos: Consulta - Escolas (HTML)."  
**Context:** O recurso é apenas um link HTML para uma ferramenta de consulta. Não há download em formato CSV, XLS ou JSON. A última atualização data de janeiro de 2020, indicando desatualização.  
**Confidence:** high

### Claim 1.1.3: O portal disponibiliza dataset de Pedidos de LAI (2019-2026) em múltiplos formatos
**Source:** Portal de Dados Abertos SC — Pedidos de Acesso à Informação  
**URL:** https://dados.sc.gov.br/dataset/pedidos-informacao  
**Date:** Última atualização: 29 de Abril de 2026, 00:46 (UTC+08:00)  
**Excerpt:** "Disponibiliza os dados de pedidos de acesso à informação que passaram pela Ouvidoria-Geral do Estado de Santa Catarina em atendimento à Lei de Acesso à Informação (LAI). Dados e recursos: XLSX, JSON, CSV, pedidos-de-informacao.csv, pedidos-de-informacao.xlsx, lai-2019-2026.csv."  
**Context:** Embora exista este dataset de transparência ativa, não foi identificado nenhum pedido de LAI específico sobre matrículas de estrangeiros dentro dos resultados de busca direta no portal.  
**Confidence:** high

### Claim 1.1.4: A API CKAN do portal permite acesso programático aos datasets
**Source:** Portal de Dados Abertos SC — Documentação da API  
**URL:** https://dados.sc.gov.br/api/3  
**Date:** Acesso em 2025-01-25  
**Excerpt:** "Você também pode ter acesso a esses registros usando a API (veja Documentação da API)."  
**Context:** A API CKAN oferece endpoint para listar organizações, grupos, datasets e recursos. No entanto, a SED possui apenas 4 datasets catalogados, nenhum com variável de nacionalidade.  
**Confidence:** high

---

## 1.2 SED-SC — Educação na Palma da Mão

### Claim 1.2.1: O sistema "Educação na Palma da Mão" foi desenvolvido em 2019 pela SED/CIASC e oferece painéis com filtros personalizados
**Source:** Tutorial no YouTube — SED/SC  
**URL:** https://www.youtube.com/watch?v=qIuCW6OrWq0  
**Date:** 2021-12-20  
**Excerpt:** "A Secretaria de Estado da Educação (SED), em parceria com o Centro de Informática e Automação do Estado de Santa Catarina (CIASC), desenvolveu em 2019 o sistema de inteligência de dados 'Educação na Palma da Mão'. A iniciativa inclui vários painéis que tornam as informações sobre a educação catarinense mais dinâmicas, detalhadas e transparentes, agrupando uma grande quantidade de dados para consulta personalizada a partir dos filtros."  
**Context:** O sistema possui painéis como: Escola, Matrículas e Turmas; Indicadores Educacionais Georreferenciados; Educação Especial; Censo da Educação Básica.  
**Confidence:** high

### Claim 1.2.2: O painel "Escola, Matrículas e Turmas" permite filtros por coordenadoria regional, município e unidade escolar
**Source:** Página oficial da SED — Educação na Palma da Mão  
**URL:** https://www.sed.sc.gov.br/educacao-na-palma-da-mao/  
**Date:** Acesso em 2025-01-25 (site indisponível via HTTPS, consultado via cache/buscas)  
**Excerpt:** "Neste painel é possível conhecer o total de matrículas, turmas e unidades escolares desta modalidade de ensino, a partir de filtros por coordenadoria regional..."  
**Context:** O painel oferece granularidade por Coordenadoria Regional de Educação (CRE), município e unidade escolar. Não há menção a filtros por nacionalidade, país de origem ou condição de estrangeiro.  
**Confidence:** high

### Claim 1.2.3: O painel do Programa de Acolhimento ao Migrante (PAM) no PowerBI oferece filtros por CRE, município, unidade escolar, etapa/modalidade e turno
**Source:** Painel PowerBI — PAM/SED-SC  
**URL:** https://app.powerbi.com/view?r=eyJrIjoiZGI0YmNiZmMtNTNkMC00ZTgxLThiMzUtNGUwMjZkM2E3OTQxIiwidCI6ImExN2QwM2ZjLTRiYWMtNGI2OC1iZDY4LWUzOTYzYTJlYzRlNiJ9  
**Date:** Acesso em 2025-01-25  
**Excerpt:** "PAM — Rede Estadual de Ensino — Programa Estadual de Acolhimento ao Migrante. Filtros: Coord. Reg. de Educação, Município, Unidade Escolar, Matriz, Etapa/Modalidade de ensino, Turno. Fonte: SISGESC/SED-SC/Atualizações diárias com guarda das informações do último dia de cada mês."  
**Context:** O painel PAM permite visualizar matrículas dos estudantes do programa por unidade escolar e município, mas não exibe filtro por nacionalidade ou país de origem no painel principal.  
**Confidence:** high

### Claim 1.2.4: O site oficial da SED (sed.sc.gov.br) apresenta instabilidade e erro de SSL
**Source:** Tentativas de acesso direto  
**URL:** https://www.sed.sc.gov.br/ e https://www2.sed.sc.gov.br/  
**Date:** 2025-01-25  
**Excerpt:** "ERR_CONNECTION_CLOSED" / "ERR_CERT_COMMON_NAME_INVALID" / "403 Forbidden"  
**Context:** O portal da SED apresentou múltiplas falhas de conexão durante a pesquisa, restringindo acesso direto a documentos. Parte do conteúdo foi acessível apenas via cache de buscadores, Google Cache ou PDFs indexados.  
**Confidence:** high

---

## 1.3 SED-SC — Informações Educacionais e Portarias

### Claim 1.3.1: A Portaria SED-SC nº 2083/2023 regulamenta matrícula de migrantes, refugiados e apátridas na rede estadual
**Source:** Diário Oficial do Estado de SC — Portaria 2083/2023  
**URL:** https://portal.doe.sea.sc.gov.br/repositorio/2023/20230801/Jornal/22072.pdf  
**Date:** 01/08/2023 (publicação no DOE/SC nº 22072)  
**Excerpt:** "PORTARIA N° 2083 de 31/07/2023 Regulamenta os procedimentos relativos à matrícula, aproveitamento de estudos realizados no exterior e transferência para o exterior de alunos da Rede Estadual de Ensino. Fica assegurada ao aluno migrante, refugiado, apátrida, solicitante de refúgio ou que tenha realizado estudos no exterior, a matrícula escolar em qualquer ano/série da Educação Básica na rede Estadual de Ensino, em qualquer tempo..."  
**Context:** A portaria revoga a Portaria 3030/2016 e estabelece novos procedimentos, incluindo dispensa de tradução juramentada de documentos para fins de matrícula e classificação/reclassificação por idade quando não há documentação. Não há menção à coleta ou publicação de dados estatísticos por nacionalidade.  
**Confidence:** high

### Claim 1.3.2: A Portaria SED-SC nº 3030/2016, revogada em 2023, já assegurava matrícula a estrangeiros
**Source:** Extranet SED-SC — Portaria 3030/2016  
**URL:** https://extranet.sed.sc.gov.br/index.php/downloads/digr/1076-portaria-n-3030-alunos-estrangeiros-1/file  
**Date:** 14/12/2016  
**Excerpt:** "PORTARIA N/3030 — Regulamenta os procedimentos relativos à matrícula e aproveitamento de estudos de estudantes transferidos do exterior para a Rede Estadual de Ensino. Art. 1º Fica assegurada, ao aluno estrangeiro, a matrícula escolar em qualquer ano/série da Educação Básica, em qualquer tempo..."  
**Context:** Documento histórico que estabelecia regras anteriores, incluindo exigência de apostila de Haia para documentos estrangeiros (com exceções para países do Mercosul e França).  
**Confidence:** high

### Claim 1.3.3: O Setor de Estatística e Avaliação da SED (GAEBE) fornece dados por e-mail mediante solicitação
**Source:** Artigo acadêmico — Dialnet (Unochapecó)  
**URL:** https://dialnet.unirioja.es/descarga/articulo/10137541.pdf  
**Date:** Acesso em 2025-01-25 (artigo com dados de 2016-2022)  
**Excerpt:** "Os dados todos foram recebidos por e-mail, pelo contato eletrônico gaebe@sed.sc.gov.br, com base nos censos escolares. Os dados, de 2007 a 2022, foram fornecidos através da Gerência de Estatística e Avaliação vinculada à Secretaria Estadual de Educação de Santa Catarina e pelo site Educação na Palma da Mão..."  
**Context:** Este é um achado crucial: dados detalhados de matrículas (incluindo imigrantes na EJA em Chapecó) foram obtidos por pesquisadores via e-mail direto para a GAEBE, não via portal de dados abertos. Isso demonstra que a SED detém os dados, mas não os publica em formato aberto e estruturado.  
**Confidence:** high

### Claim 1.3.4: A SED utiliza o sistema SISGESC para gestão de matrículas e migra dados para o Educacenso/INEP
**Source:** Portaria SED 1378/2024 (DOE/SC)  
**URL:** https://portal.doe.sea.sc.gov.br/repositorio/2024/20240528/Jornal/22275.pdf  
**Date:** 28/05/2024  
**Excerpt:** "Estabelece os responsáveis e cronograma específico para as escolas estaduais de Santa Catarina, que realizam a coleta via processo de Migração de dados do sistema de Gestão Educacional de Santa Catarina — SISGESC para sistema Educacenso."  
**Context:** O SISGESC é o sistema de gestão educacional estadual. Os dados de matrículas (incluindo campo de nacionalidade/país de origem) são coletados pelas escolas e migrados para o INEP/Educacenso. A SED possui esses dados em seu sistema interno, mas não os disponibiliza como dataset aberto.  
**Confidence:** high

---

## 1.4 FCEE — Fundação Catarinense de Educação Especial

### Claim 1.4.1: A FCEE mantém publicações estatísticas focadas em educação especial, não em dados de estrangeiros
**Source:** FCEE — Biblioteca Virtual  
**URL:** https://www.fcee.sc.gov.br/downloads/biblioteca-virtual  
**Date:** Acesso em 2025-01-25  
**Excerpt:** "Biblioteca virtual da FCEE. Acervo Histórico, Acessibilidade, Campanhas, Relatório de Atividades Anual, Relatório Estatístico, Relatórios de Ouvidoria, FCEE em números."  
**Context:** A FCEE produz relatórios estatísticos sobre educação especial (matrículas em SAEDE, atendimento em classe, instituições especializadas), mas não há evidência de dados desagregados por nacionalidade ou país de origem.  
**Confidence:** high

### Claim 1.4.2: O relatório "FCEE em Números" (2000-2010) detalha matrículas em instituições especializadas e serviços de educação especial
**Source:** FCEE — PDF "FCEE em Números"  
**URL:** https://www.fcee.sc.gov.br/images/stories/Publicacoes/op_3728_cartilha_fcee_em_nmeros_adp-3211_00022.pdf  
**Date:** 1ª Edição, 2013 (dados 2000-2010)  
**Excerpt:** "Este documento é um levantamento dos dados estatísticos do período de 2000 a 2010, com base na síntese dos Relatórios de Estatística e nos Relatórios de Atividades deste período. Tabela 2 — Número de matrículas nas Instituições Especializadas conveniadas com a FCEE — 2000 a 2010: TOTAL variando de 13.837 (2000) a 17.704 (2010)."  
**Context:** O relatório é rico em dados de educação especial, mas não inclui qualquer variável relacionada a nacionalidade ou estrangeiros.  
**Confidence:** high

### Claim 1.4.3: A FCEE possui relatórios estatísticos anuais (ex: 2011) com tabelas desagregadas por GERED
**Source:** FCEE — Relatório Estatístico 2011  
**URL:** https://www.fcee.sc.gov.br/downloads/biblioteca-virtual/relatorio-de-atividades-anual-fcee/relatorio-estatistico/530-relatorio-estatistico-2011/file  
**Date:** 2011  
**Excerpt:** "TABELA 37 — Número de alunos por GEREDs, por CAESP, período e tipos de deficiência do Serviço de Atendimento Educacional Especializado — SAEDE em 2011. TABELA 47 — Educandos matriculados na rede regular de ensino que tem Atendimento em Classe, por GEREDs e unidade escolar em 2011."  
**Context:** A granularidade chega ao nível de GERED (Gerência Regional de Educação, equivalente à CRE) e unidade escolar, mas não inclui nacionalidade.  
**Confidence:** high

---

## 1.5 Programa de Acolhimento ao Migrante (PAM)

### Claim 1.5.1: O PAM é o único programa estadual brasileiro de atendimento pedagógico especializado a migrantes
**Source:** Portal RBV / NSC Total  
**URL:** https://portalrbv.com.br/cotidiano/educacao/sc-e-o-unico-estado-do-brasil-com-programa-pioneiro-de-ensino-para-imigrantes-sz/  
**Date:** 2025-09-18  
**Excerpt:** "Santa Catarina é o único estado brasileiro que oferece atendimento pedagógico especializado a estudantes imigrantes na rede estadual de ensino. Com mais de 1.300 alunos matriculados, o Programa Estadual de Acolhimento ao Migrante (PAM), coordenado pela Secretaria de Estado da Educação (SED)..."  
**Context:** O PAM atende aproximadamente 1.324 estudantes migrantes em cerca de 50 unidades escolares da rede estadual, com 70 professores. Os estudantes vêm de Venezuela, Haiti, Argentina, Paraguai, Bolívia, Senegal, Colômbia, entre outros.  
**Confidence:** high

### Claim 1.5.2: O PAM foi criado em agosto de 2021 como PARE e renomeado em 2023
**Source:** Revista REASE (Periodicorease.pro.br)  
**URL:** https://periodicorease.pro.br/rease/article/download/23970/15258/72056  
**Date:** fev. 2026 (artigo publicado)  
**Excerpt:** "O PAM teve início em agosto de 2021, inicialmente denominado Programa de Acolhimento a Refugiados e Estrangeiros (PARE), em resposta ao aumento expressivo de matrículas de estudantes migrantes e refugiados, especialmente no Ensino Fundamental. Posteriormente, o programa passou a adotar a nomenclatura atual... Atualmente, o PAM atende aproximadamente 1.150 estudantes migrantes matriculados entre o Ensino Fundamental e o Ensino Médio, com predominância de estudantes de nacionalidade venezuelana."  
**Context:** O artigo acadêmico traz informações detalhadas sobre o programa, mas ressalta que os dados de adesão são coletados via diagnóstico anual das escolas, não via painel público estruturado.  
**Confidence:** high

### Claim 1.5.3: A SED oferece também curso de Língua Portuguesa e Cultura Brasileira para Estrangeiros nos CEJAs
**Source:** AJ Notícias  
**URL:** https://ajnoticias.com.br/noticia/45636/educacao-inclusiva-santa-catarina-desenvolve-projeto-para-estudantes-migrantes  
**Date:** 2025-09-05  
**Excerpt:** "A SED oferece, por meio dos Centros de Educação de Jovens e Adultos (CEJAs), o curso de qualificação profissional (FIC) em Língua Portuguesa e Cultura Brasileira para Estrangeiros. Atualmente, são atendidos 1.490 estrangeiros no nível básico; 412 no intermediário; e 156 no avançado, em 26 CEJAs e 16 unidades descentralizadas."  
**Context:** Este dado demonstra que a SED possui cadastros de estrangeiros em programas específicos, mas esses números não aparecem nos datasets do portal de dados abertos.  
**Confidence:** high

---

## 1.6 Dados sobre Estrangeiros/Imigrantes na Educação de SC

### Claim 1.6.1: Em 2017, SC registrou 5.220 matrículas de estrangeiros (0,42% do total)
**Source:** Artigo acadêmico — Ana Paula Silva et al. (MPU/UFSC)  
**URL:** https://escola.mpu.mp.br/h/rede-de-capacitacao-a-refugiados-e-migrantes/atividade-em-florianopolis/criancas_migrantes-parte-3.pdf  
**Date:** Dados de 2017  
**Excerpt:** "CENSO ESCOLAR DE 2017 — Santa Catarina. 1.228.575 matrículas iniciais nas redes municipal e estadual. 5.220 matrículas de estrangeiros = 0,42% do total de matrículas do estado. Fonte: Secretaria de Educação do Estado de Santa Catarina. Foram registradas 85 nacionalidades, destas Haiti, Argentina, Paraguai, Estados Unidos, Portugal, Itália e Emirados Árabes se destacam."  
**Context:** Dados fornecidos pela própria SED para pesquisadores, baseados no Censo Escolar. A fonte primária é a SED/Setor de Estatística, mas não está disponível como dataset aberto no portal estadual.  
**Confidence:** high

### Claim 1.6.2: Em 2022, a rede estadual de SC possuía 6.323 alunos estrangeiros (nascidos no exterior)
**Source:** Página da SED — Ensino Fundamental (cache/indexação)  
**URL:** https://www.sed.sc.gov.br/etapas-e-modalidades-de-ensino/ensino-fundamental/  
**Date:** Dados SISGESC/SED (2022)  
**Excerpt:** "Conforme dados dos SISGESC/SED (2022), a rede estadual de ensino de Santa Catarina possui atualmente 6.323 alunos estrangeiros (nascidos no exterior)..."  
**Context:** Este número aparece em páginas da SED, mas não como dataset baixável. A menção a "nascidos no exterior" indica que o sistema possui essa variável, mas não a publica em formato aberto.  
**Confidence:** high

### Claim 1.6.3: Em Chapecó, as matrículas de imigrantes na EJA cresceram 606,67% entre 2016 e 2022
**Source:** Dialnet — Revista do PPGE/Unochapecó  
**URL:** https://dialnet.unirioja.es/descarga/articulo/10137541.pdf  
**Date:** Dados de 2016-2022  
**Excerpt:** "Em 2016 havia 15 estudantes imigrantes matriculados na EJA, em 2022 havia 106, o que representou um aumento no período de 606,67%."  
**Context:** O artigo detalha ainda que das 106 matrículas de imigrantes na EJA em Chapecó em 2022, 91 (85%) estavam em instituições públicas. Os dados foram obtidos por e-mail da GAEBE/SED.  
**Confidence:** high

---

## 1.7 Artigos Acadêmicos e Fontes Alternativas

### Claim 1.7.1: O artigo de Castro (UFSC, 2025) analisa convergências e divergências entre a Resolução CNE 1/2020 e a Portaria SED-SC 2083/2023
**Source:** Repositório UFSC  
**URL:** https://repositorio.ufsc.br/handle/123456789/267205  
**Date:** 2025-08-01  
**Excerpt:** "Um dos pontos em que esses documentos divergem é quanto ao pedido de documentação para efetivação da matrícula. Entre os pontos de convergência, podemos citar a avaliação."  
**Context:** O TCC destaca que os Editais de Matrícula publicados em 2023 e 2024 não constam informações sobre procedimentos de matrícula para migrantes, indicando uma lacuna na comunicação oficial da SED.  
**Confidence:** high

### Claim 1.7.2: O OBMigra/UNB utiliza microdados do Censo Escolar (INEP) para analisar imigrantes em SC
**Source:** Periplos — OBMigra/UNB  
**URL:** https://periodicos.unb.br/index.php/obmigra_periplos/article/download/34881/28595/92810  
**Date:** 2020-10-02  
**Excerpt:** "Quatro Unidades da Federação — São Paulo, Roraima, Paraná e Santa Catarina — concentram boa parte das crianças imigrantes na Educação Infantil (62,7%)."  
**Context:** Os dados do INEP/Censo Escolar são a fonte mais confiável para análise de estrangeiros por UF, mas exigem processamento dos microdados, que estão disponíveis em https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar.  
**Confidence:** high

### Claim 1.7.3: O TCE/SC produz painéis de transparência com dados educacionais, mas sem detalhamento por nacionalidade
**Source:** Relatório de Avaliação PME — Ipumirim/SC  
**URL:** https://ipumirim.sc.gov.br/uploads/sites/386/2024/06/Relatorio-Avaliacao-PME-2023.pdf  
**Date:** 2023  
**Excerpt:** "As informações disponibilizadas no Painel produzido pelo TCE – SC demonstram o percentual da população de 4 e 5 anos que frequentam a pré-escola... Uma das hipóteses é que o município está recebendo muitos imigrantes provenientes principalmente da região Nordeste do país."  
**Context:** O painel do TCE/SC (https://paineistransparencia.tce.sc.gov.br) utiliza dados do Censo Escolar e IBGE, mas não oferece filtro por nacionalidade.  
**Confidence:** medium

---

## Resumo Executivo

### Principais Achados

| Aspecto | Avaliação | Evidência |
|---------|-----------|-----------|
| **Portal dados.sc.gov.br** | 4 datasets da SED; nenhum com dados de matrícula por nacionalidade | Dataset "busca de Escolas" é apenas link HTML (atualizado em 2020); demais são Avaliação Educacional, SIOPE e Bolsas Universitárias |
| **SED-SC — Educação na Palma da Mão** | Painel interativo com filtros por CRE, município, escola, etapa, modalidade, turno; **sem filtro por nacionalidade/país de origem** | Fonte: SISGESC/SED; desenvolvido em 2019 pelo CIASC |
| **SED-SC — PAM** | Painel PowerBI com filtros por CRE, município, unidade escolar, etapa/modalidade, turno; **sem filtro por nacionalidade** | Fonte: SISGESC/SED; atualizações diárias |
| **FCEE** | Relatórios estatísticos de educação especial (2000-2011+); **sem dados de nacionalidade** | "FCEE em Números", Relatórios Estatísticos Anuais |
| **Dados de estrangeiros na rede estadual** | Existem internamente: 6.323 alunos estrangeiros (2022), 5.220 (2017), 85 nacionalidades identificadas em 2017 | Fornecidos pela SED para pesquisadores, mas **não publicados como dataset aberto** |
| **Acesso alternativo** | Pesquisadores obtêm dados por e-mail (gaebe@sed.sc.gov.br) ou via INEP/Censo Escolar (microdados) | Artigo de Chapecó (Dialnet) documenta obtenção por e-mail da GAEBE/SED |
| **Legislação** | Portaria 2083/2023 regulamenta matrícula de migrantes; revoga Portaria 3030/2016 | DOE/SC nº 22072, de 01/08/2023 |

### Lacunas Críticas Identificadas

1. **Ausência de dataset aberto por nacionalidade**: Nenhum dos portais investigados (dados.sc.gov.br, SED-SC, FCEE) disponibiliza dataset para download (CSV, XLS, JSON) com dados de matrículas desagregados por nacionalidade, país de origem ou condição de estrangeiro.

2. **Formato inadequado**: O único dataset da SED no portal de dados abertos que se aproxima do tema ("busca de Escolas") é um link HTML para consulta externa, não um arquivo estruturado, e está desatualizado (2020).

3. **Dados existentes apenas internamente**: A SED possui os dados em seu sistema SISGESC (migrados para o Educacenso/INEP), e fornece estatísticas pontuais para pesquisadores por e-mail, mas não os publica como dados abertos estruturados.

4. **Painéis visuais sem exportação estruturada**: O "Educação na Palma da Mão" e o painel PAM (PowerBI) permitem visualização com filtros geográficos e administrativos, mas não oferecem download dos dados subjacentes em formato tabular com variável de nacionalidade.

5. **FCEE não abrange o tema**: A Fundação Catarinense de Educação Especial produz relatórios estatísticos detalhados sobre educação especial, mas não inclui variável de nacionalidade/país de origem.

### Recomendações para Acesso aos Dados

| Fonte | Tipo de acesso | Granularidade | Anos disponíveis | Observações |
|-------|---------------|---------------|------------------|-------------|
| INEP — Microdados do Censo Escolar | Dados abertos nacionais (CSV) | Escola, turma, aluno | 2007-2023 | Variável "Nacionalidade" e "País de origem" disponíveis; requer tratamento estatístico |
| SED-SC — GAEBE (gaebe@sed.sc.gov.br) | Pedido direto/e-mail | Município, escola, CRE | Sob demanda | Não é dados aberto; depende da disponibilidade do setor |
| SED-SC — PAM (PowerBI) | Visualização online | Unidade escolar, município, CRE | 2021-atual | Sem exportação tabular; sem filtro de nacionalidade |
| SED-SC — Educação na Palma da Mão | Visualização online | CRE, município, escola, etapa | 2007-atual | Sem exportação estruturada por nacionalidade |
| dados.sc.gov.br — LAI | Pedido formal de acesso à informação | Sob demanda | 2019-2026 | Dataset de pedidos LAI disponível; pode-se fazer novo pedido |

### Contradições e Limitações

- **Contradição**: A SED-SC afirma promover transparência via "Educação na Palma da Mão" e PAM, mas não disponibiliza a variável "nacionalidade" nos painéis públicos, mesmo possuindo os dados internamente (SISGESC → Educacenso).
- **Limitação**: O site oficial da SED (sed.sc.gov.br) apresentou instabilidade durante a pesquisa, inviabilizando acesso direto a documentos e painéis.
- **Limitação**: A FCEE, embora tenha publicações estatísticas robustas, limita-se à educação especial e não cruza dados com variáveis migratórias.

---

**Fim do relatório.**
