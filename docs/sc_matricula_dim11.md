# Dimensão 11 — Dados de Imigração vs. Matrícula Escolar: Integração de Bases e Possibilidades de Cruzamento

## Santa Catarina — Relatório de Pesquisa (Phase 1)

---

## 1. Contexto e Objetivo

Esta pesquisa investiga se é possível cruzar diferentes bases de dados administrativas (Censo Escolar, Censo IBGE, dados da Polícia Federal, RNE/CRNM, RAIS, Cadastro Único, etc.) para estimar ou mapear estudantes estrangeiros matriculados na rede pública de Santa Catarina. Verifica iniciativas de integração de dados governamentais no estado, data lakes, big data governamental e limitações impostas pela LGPD.

---

## 2. Sistemas de Dados Educacionais em Santa Catarina

### 2.1 SISGESC — Sistema de Gestão Educacional de Santa Catarina

Claim: O SISGESC é o sistema central da Secretaria de Estado da Educação (SED-SC), administrado pelo CIASC, com 21 módulos que armazenam todos os dados da rede estadual de educação, incluindo escolas, alunos, profissionais, histórico de notas e outras informações [^13^].
Source: CIASC
URL: https://www.ciasc.sc.gov.br/sisgesc/
Date: 2023-03-17
Excerpt: "O sistema é administrado pela Secretaria de Estado da Educação (SED) e armazena todos os dados da rede estadual de educação, como quais são as escolas, os alunos e profissionais que trabalham nelas, o histórico de notas dos estudantes e outras informações importantes."
Context: Sistema operacional da educação estadual
Confidence: high

### 2.2 SIDEP — Sistema de Inteligência de Dados Educação na Palma da Mão

Claim: A SED-SC possui o sistema on-line SIDEP/SC que concentra dados e indicadores da rede estadual de ensino, desenvolvido em parceria com o CIASC [^13^].
Source: SED-SC
URL: https://www.sed.sc.gov.br/informacoes-educacionais/indicadores-educacionais/
Date: Não informado
Excerpt: "Sistema de Inteligência de Dados Educação na Palma da Mão - SIDEP/SC. É um sistema on-line que concentra dados e indicadores da rede estadual de ensino de Santa Catarina."
Context: Painel de inteligência de dados da educação estadual
Confidence: high

Claim: O SIDEP foi utilizado para gerar planilha com matrículas por nacionalidade de 2014 a 2023, fornecida a pesquisadores via equipe técnica [^78^].
Source: Revista Aracê (artigo acadêmico)
URL: https://periodicos.newsciencepubl.com/arace/article/download/4418/5924/17167
Date: 2025-04-14
Excerpt: "Em consulta à Secretaria de Estado da Educação de Santa Catarina – SED, foi possível acessar, por meio da Equipe Técnica do Sistema de Inteligência de Dados Educação na Palma da Mão – SIDEP, uma planilha de Excel contendo as matrículas da educação básica, no Estado de Santa Catarina, no período de 2014 a 2023."
Context: Acesso a dados internos da SED-SC via SIDEP
Confidence: high

### 2.3 Portal de Dados Abertos da SED-SC

Claim: O portal dados.sc.gov.br da Secretaria de Estado da Educação possui apenas 4 datasets: Avaliação Educacional, Orçamentos Públicos em Educação (SIOPE), Busca de Escolas e Bolsas Universitárias. Não há datasets específicos sobre matrículas de estrangeiros ou migrantes [^14^].
Source: Dados Abertos SC
URL: https://dados.sc.gov.br/ne/organization/sed
Date: 2025-12-12 (consulta)
Excerpt: "4 datasets found: Avaliação Educacional; Orçamentos Públicos em Educação; busca de Escolas; Bolsas Universitárias"
Context: Verificação presencial do portal de dados abertos
Confidence: high

---

## 3. Dados de Imigração em Santa Catarina

### 3.1 Censo Demográfico 2022 (IBGE)

Claim: Santa Catarina apresentou o maior saldo migratório do Brasil entre 2017 e 2022: 354.350 pessoas (taxa líquida de 4,66%). O estado recebeu 503.580 imigrantes interestaduais [^453^].
Source: IBGE / Agência de Notícias
URL: https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/43815-censo-2022-19-2-milhoes-de-pessoas-vivem-fora-de-sua-regiao-de-nascimento
Date: 2025-06-27
Excerpt: "Santa Catarina apresentou o maior saldo migratório e a maior taxa líquida de migração em 2022. Entre 2017 e 2022, o estado registrou um ganho populacional de 354 mil pessoas, uma contribuição de 4,66% à sua população total."
Context: Dados oficiais do Censo 2022 sobre migração
Confidence: high

Claim: O número de estrangeiros em SC mais que triplicou entre 2010 e 2022, passando de 11.671 para 72.793 pessoas (crescimento de 523%). Somando estrangeiros e naturalizados brasileiros, o número saltou de 17,6 mil para 83,4 mil [^481^].
Source: G1 Santa Catarina
URL: https://g1.globo.com/sc/santa-catarina/noticia/2025/06/27/sc-principal-destino-migrantes-brasil-origem-novos-moradores.ghtml
Date: 2025-06-27
Excerpt: "Em 2010, o número de estrangeiros no estado somava 11.671 pessoas; Em 2022, o número de estrangeiros passou para 72.793 pessoas... Considerando estrangeiros e naturalizados brasileiros, o número saltou de 17,6 mil para 83,4 mil no mesmo período."
Context: Dados do Censo IBGE 2022 sobre estrangeiros em SC
Confidence: high

Claim: Os principais imigrantes estrangeiros em SC são da Venezuela (54%), Haiti (15,7%), Argentina (5%), Estados Unidos (2,7%) e Portugal (1,9%). Os municípios com mais estrangeiros são Chapecó (11.189), Florianópolis (10.517) e Joinville (7.854) [^644^].
Source: G1 Santa Catarina
URL: https://g1.globo.com/sc/santa-catarina/noticia/2025/06/28/por-que-sc-se-tornou-o-principal-destino-de-migrantes-no-pais-entenda.ghtml
Date: 2025-06-28
Excerpt: "1. Venezuela: 54%; 2. Haiti: 15,7%; 3. Argentina: 5%... Chapecó (11.189), maior cidade do Oeste de Santa Catarina, é o município catarinense com mais pessoas naturalizadas brasileiras e estrangeiras, seguido de Florianópolis (10.517) e Joinville (7.854)."
Context: Censo 2022 — perfil dos estrangeiros em SC
Confidence: high

### 3.2 SISMIGRA — Sistema de Registro Nacional Migratório (Polícia Federal)

Claim: Santa Catarina teve 55.261 registros ativos de imigrantes internacionais no SISMIGRA entre 2018 e 2022, sendo o 5º estado do Brasil no ranking [^592^].
Source: Instituto Mauro Borges (Goiás) / OBMigra
URL: https://goias.gov.br/imb/wp-content/uploads/sites/29/2024/01/Estudo_007_2023_imigracao_internacional_em_goias.pdf
Date: 2024-01
Excerpt: "SC: 6.910 (2018), 9.709 (2019), 7.647 (2020), 13.726 (2021), 17.269 (2022) — Total Geral: 55.261"
Context: Dados do SISMIGRA/OBMigra sobre registros de imigrantes por UF
Confidence: high

Claim: O SISMIGRA cadastra imigrantes com vistos de residência regular no país, que devem comparecer à Polícia Federal em até 30 dias do ingresso. A base permite identificar perfil do migrante (sexo, país de nascimento, UF de residência) [^592^].
Source: OBMigra/IMB
URL: https://goias.gov.br/imb/wp-content/uploads/sites/29/2024/01/Estudo_007_2023_imigracao_internacional_em_goias.pdf
Date: 2024-01
Excerpt: "O Sistema de Registro Nacional Migratório (SISMIGRA) cadastra os imigrantes com vistos de residência regular no país. Esses devem comparecer à Polícia Federal em até 30 dias do ingresso no país para se cadastrar e obter o Registro Nacional Migratório (RMN)."
Context: Sistema administrativo da Polícia Federal
Confidence: high

### 3.3 DataMigra — Plataforma do MJSP/OBMigra

Claim: O DataMigra é uma plataforma desenvolvida pelo OBMigra/UnB para auxiliar na obtenção de dados de imigração internacional e refúgio, permitindo o cruzamento eficiente de variáveis comumente demandadas [^573^].
Source: MJSP / Portal de Imigração
URL: https://www.gov.br/mj/pt-br/assuntos/noticias/mjsp-e-obmigra-lancam-relatorio-anual-de-2022-com-dados-de-migracoes
Date: 2022-12-07
Excerpt: "O DataMigra foi projetado para auxiliar na obtenção de dados de imigração internacional e solicitações do reconhecimento da condição de refúgio, de forma dinâmica e intuitiva, possibilitando o cruzamento entre as variáveis comumente demandadas por esses usuários."
Context: Plataforma federal de dados migratórios
Confidence: high

### 3.4 CAGED — Emprego Formal de Estrangeiros em SC

Claim: Santa Catarina liderou as contratações de estrangeiros no Brasil em 2024, com 18.900 trabalhadores estrangeiros (26,6% do total nacional). Venezuelanos representaram 74,7% do saldo (14.135 contratações) [^497^].
Source: Governo de Santa Catarina / SICOS
URL: https://estado.sc.gov.br/noticias/santa-catarina-e-lider-nacional-na-contratacao-de-estrangeiros/
Date: 2025-02-13
Excerpt: "Santa Catarina é líder nacional na contratação de estrangeiros. Conforme dados do Caged, o estado registrou em 2024 a contratação de 18.900 trabalhadores estrangeiros, o maior volume do país... Venezuelanos representam 74,7% do saldo das contratações, com 14.135 novos funcionários."
Context: Dados do CAGED sobre emprego formal de estrangeiros em SC
Confidence: high

Claim: Chapecó foi o município catarinense que mais contratou estrangeiros no primeiro semestre de 2025 (1,3 mil), seguido de Joinville (1,1 mil) e Florianópolis (457) [^614^].
Source: NSC Total
URL: https://www.nsctotal.com.br/colunistas/estela-benetti/sc-e-o-segundo-estado-que-mais-contrata-estrangeiros-e-a-maioria-vem-da-america-latina
Date: 2025-08-08
Excerpt: "As cidades que mais abriram oportunidades neste ano em SC foram Chapecó com 1,3 mil, Joinville com 1,1 mil, Florianópolis com 457, Blumenau 448 e Guatambu 384."
Context: Dados CAGED por município de SC
Confidence: high

---

## 4. Bases Administrativas Nacionais com Potencial de Cruzamento

### 4.1 Censo Escolar (INEP)

Claim: Os microdados do Censo Escolar possuem as variáveis TP_NACIONALIDADE (1-Brasileira, 2-Brasileira nascida no exterior/naturalizada, 3-Estrangeira) e NOME_PAIS_CE (nome do país de origem do aluno), conforme dicionário de variáveis do INEP [^20^].
Source: Portal de Imigração / MJSP (dicionário INEP)
URL: https://portaldeimigracao.mj.gov.br/images/dados/microdados/2021/INEP/Dicion%C3%A1rios_INEP_-_Divulga%C3%A7%C3%A3o_-_Censo_Escolar.xlsx
Date: Não informado
Excerpt: "TP_NACIONALIDADE: 1 - Brasileira; 2 - Brasileira - nascido no exterior ou naturalizado; 3 - Estrangeira... NOME_PAIS_CE: Nome do país de origem do aluno"
Context: Dicionário de variáveis dos microdados do Censo Escolar
Confidence: high

Claim: Estudo acadêmico analisou os microdados do Censo Escolar 2020 para identificar matrículas de crianças migrantes na educação infantil de São Paulo, utilizando variáveis como país de origem, sexo, cor/raça, etapa de ensino e dependência administrativa [^18^].
Source: Revista Momento / FURG
URL: https://periodicos.furg.br/momento/article/download/15988/10544/58966
Date: 2023
Excerpt: "Utilizaremos, para tanto, as seguintes variáveis: país de origem, sexo, cor/raça, etapa de ensino, dependência administrativa e categoria de escola privada."
Context: Prova de conceito de uso dos microdados para mapear estrangeiros
Confidence: high

Claim: A partir de 2020, os relatórios do Censo Escolar descontinuaram as informações específicas de estudantes estrangeiros nos resumos técnicos nacionais, embora as variáveis continuem existindo nos microdados [^78^].
Source: Revista Aracê
URL: https://periodicos.newsciencepubl.com/arace/article/download/4418/5924/17167
Date: 2025-04-14
Excerpt: "Contudo, as últimas edições do relatório do Censo Escolar descontinuaram as informações de estudantes estrangeiros."
Context: Limitação na divulgação agregada do INEP sobre estrangeiros
Confidence: medium

### 4.2 Cadastro Único (MDS)

Claim: O Cadastro Único permite a identificação de pessoas estrangeiras cadastradas. O indicador IN143 mede o "Quantitativo de pessoas cadastradas de nacionalidade estrangeira", disponível desde 12/2012, com desagregação municipal, estadual e nacional [^641^].
Source: Wiki SAGI / MDS
URL: https://wiki-sagi.mds.gov.br/home/DS/Cad/I/IN143
Date: 2025-06-17
Excerpt: "Quantitativo de pessoas cadastradas de nacionalidade estrangeira. A informação é autodeclarada pela Responsável Familiar, para cada pessoa de sua composição, por meio dos Campos 4.11 e 4.12 do Formulário de Cadastramento."
Context: Variável do CadÚnico para identificar estrangeiros
Confidence: high

Claim: Imigrantes e refugiados podem se cadastrar no Cadastro Único para acessar programas sociais, desde que tenham CPF. O MDS publicou orientações específicas para cadastramento de famílias indígenas imigrantes e refugiadas [^555^].
Source: MDS
URL: https://www.mds.gov.br/webarquivos/sala_de_imprensa/boletins/boletim_auxilio_brasil/2022/marco/Boletim_PAB_Informa_826.html
Date: 2022-03-17
Excerpt: "Todos os refugiados e imigrantes no Brasil têm direito de se inscrever no Cadastro Único e de ser atendidos pelo SUAS, independentemente da sua condição migratória ou nacionalidade, mesmo o imigrante em situação irregular (documental)."
Context: Normativa do MDS sobre inclusão de migrantes no CadÚnico
Confidence: high

Claim: O município de São José (SC) possui moradores de 41 nacionalidades cadastrados no Cadastro Único, sendo a maioria venezuelanos (1,6 mil), cubanos (514), haitianos (248), colombianos (44) e argentinos (36) [^649^].
Source: NSC Total / Prefeitura de São José
URL: https://www.nsctotal.com.br/noticias/cidade-colada-em-florianopolis-atrai-moradores-de-41-paises-e-vira-refugio-de-nacoes-em-guerra
Date: 2026-04-23
Excerpt: "A maior parte dos moradores estrangeiros cadastrados no CadÚnico são da Venezuela, com 1,6 mil pessoas vivendo em São José. Imigrantes de Cuba também aparecem em peso, com 514 pessoas cadastradas."
Context: Dados municipais de CadÚnico sobre estrangeiros em SC
Confidence: high

### 4.3 RAIS / CAGED

Claim: A RAIS possui informações sobre trabalhadores imigrantes no mercado formal, com variáveis de escolaridade, rendimento, inserção ocupacional e nacionalidade. O OBMigra analisou microdados da RAIS de 2010 a 2018 para estudar a inserção socioeconômica dos imigrantes [^538^].
Source: Portal de Imigração / OBMigra
URL: https://portaldeimigracao.mj.gov.br/images/dados/relatorios_RAIS/Relat%C3%B3rio_RAIS.pdf
Date: 2019
Excerpt: "O estudo foi realizado a partir do registro administrativo da Relação Anual de Informações Sociais (RAIS), base de dados do Ministério da Economia. As informações disponibilizadas pela RAIS possuem grande riqueza de detalhes e permite acompanhar as tendências do mercado de trabalho formal para a população imigrante."
Context: Potencial de cruzamento RAIS-Censo Escolar via localização e escolaridade
Confidence: high

### 4.4 Datasus / SUS

Claim: O Ministério da Saúde lançou Nota Técnica em 2024 orientando o cadastro de migrantes no e-SUS APS, independentemente da documentação. O SISAB registrou 512.517 migrantes cadastrados na atenção primária de 2013 a 2023 [^543^].
Source: Ministério da Saúde
URL: https://www.gov.br/saude/pt-br/assuntos/noticias/2024/abril/saude-lanca-nota-tecnica-com-orientacoes-de-atendimento-a-migrantes-refugiados-e-apatridas
Date: 2024-04-02
Excerpt: "Segundo o Sistema de Informações em Saúde da Atenção Básica (Sisab), 512.517 migrantes foram cadastrados nas equipes da atenção primária de 2013 a 2023."
Context: Potencial de cruzamento via endereço/CPF do migrante
Confidence: high

---

## 5. Integração de Dados Governamentais em Santa Catarina

### 5.1 CIASC e Plataforma BoaVista

Claim: A Plataforma BoaVista é um ecossistema de Big Data do CIASC que consolida dados governamentais de SC, com duas camadas: Big Data (armazenamento e processamento distribuído) e BoaVista Gestão (compartilhamento de painéis e relatórios). A plataforma incorpora aproximadamente 140 conjuntos de dados e mais de 4.000 tabelas acessadas por mais de 1.500 usuários em 35 entidades públicas diferentes [^589^][^590^].
Source: CIASC / Cloudera
URL: https://www.ciasc.sc.gov.br/boavista/ ; https://br.cloudera.com/customers/ciasc.html
Date: 2025-12-12 / 2024-04-18
Excerpt: "A infraestrutura de compartilhamento de dados incorpora hoje em dia aproximadamente 140 conjuntos de dados, mais de 4.000 tabelas acessadas por mais de 1.500 usuários em 35 entidades públicas diferentes no governo do estado de Santa Catarina."
Context: Infraestrutura central de integração de dados do governo de SC
Confidence: high

Claim: Todas as principais secretarias, incluindo fazenda, saúde, segurança, agricultura e educação, interagem com a Plataforma BoaVista. A Secretaria de Educação já utiliza a plataforma para melhorar a gestão de recursos humanos, contrastando informações em seu próprio sistema com dados da Secretaria de Administração [^590^].
Source: Cloudera (história de sucesso do CIASC)
URL: https://br.cloudera.com/customers/ciasc.html
Date: 2024-04-18
Excerpt: "Outro exemplo tem sido a capacidade da Secretaria de Educação de melhorar a gestão de recursos humanos, contrastando informações em seu próprio sistema com dados fornecidos pela Secretaria de Estado da Administração, responsável pelos recursos humanos."
Context: Integração intersecretarial via BoaVista
Confidence: high

### 5.2 SAT-Datalake (SEF-SC)

Claim: A Secretaria de Estado da Fazenda de Santa Catarina desenvolveu o SAT-Datalake, uma plataforma de Big Data que utiliza Cloudera como base tecnológica para processamento, armazenamento e análise de grandes volumes de dados, incluindo mais de 350 Terabytes de dados líquidos armazenados e mais de 50 tipos de documentos fiscais e bases (RAIS/CAGED, ANAC, DETRAN, entre outros) [^527^][^529^].
Source: SEF-SC / COGEF
URL: https://www.sef.sc.gov.br/noticias/fazenda-conquista-premio-internacional-por-uso-de-tecnologia-e-participa-de-foruns-estrategicos ; https://www.cogef.ms.gov.br/wp-content/uploads/2025/05/Palestra-6.1-Iniciativas-de-uso-de-IA-na-SEF-SC-Marcos-Domingues.pdf
Date: 2025-09-04 / Não informado
Excerpt: "A solução, chamada de SAT-Datalake, utiliza a plataforma de Big Data da Cloudera... Mais de 350 Terabytes de dados líquidos armazenados no big data... Mais de 50 tipos de documentos fiscais, declarações e bases de dados já carregados no ambiente... incluindo EFD, DIME, NFe, RAIS/CAGED, ANAC, DETRAN, SCANC, entre outros."
Context: Data lake da fazenda estadual com potencial de integração com outras bases
Confidence: high

### 5.3 SC em Territórios (SEPLAN)

Claim: O projeto SC em Territórios, lançado pela SEPLAN, espacializa dados e indicadores socioeconômicos em mapas geográficos. Utilizou dados do Censo 2022 para mapear o fluxo migratório, identificando Florianópolis (215.609 migrantes), Joinville (184.492) e Chapecó (80.973) como principais destinos [^516^].
Source: SEPLAN-SC
URL: https://www.seplan.sc.gov.br/seplan-lanca-sc-em-territorios/
Date: 2025-08-20
Excerpt: "A Secretaria de Estado do Planejamento (Seplan) apresenta o projeto SC em Territórios, que tem como objetivo espacializar dados e indicadores, transformando números e estatísticas em informação visual e geográfica... Florianópolis lidera o ranking dos municípios que mais receberam migrantes."
Context: Plataforma geoespacial do governo de SC com dados de migrantes
Confidence: high

### 5.4 Infraestrutura de Dados Espaciais de SC (IDE/SC)

Claim: A SEPLAN avança na implementação da Infraestrutura de Dados Espaciais de Santa Catarina (IDE/SC), com grupos de trabalho técnicos e encontros de representantes de diversas pastas para centralizar e facilitar o acesso a dados espaciais de todo o Estado [^591^].
Source: SEPLAN-SC
URL: https://www.seplan.sc.gov.br/estado-avanca-nos-trabalhos-para-implementacao-da-infraestrutura-de-dados-espaciais/
Date: 2025-04-15
Excerpt: "A IDE/SC visa centralizar e facilitar o acesso a dados espaciais de todo o Estado, promovendo transparência, eficiência e integração entre os órgãos governamentais e a sociedade."
Context: Iniciativa estrutural de dados espaciais integrados em SC
Confidence: medium

---

## 6. Dados de Matrícula de Estrangeiros em Santa Catarina

### 6.1 Matrículas por Nacionalidade na Educação Básica de SC

Claim: Em 2023, Santa Catarina registrou 1.726.930 matrículas na educação básica, das quais 26.363 eram de estudantes migrantes (informados como estrangeiros). A distribuição por dependência administrativa era: Municipal 14.325 (54,33%), Estadual 9.407 (35,68%), Privada 2.453 e Federal 178 [^78^].
Source: Revista Aracê (dados da SED-SC)
URL: https://periodicos.newsciencepubl.com/arace/article/download/4418/5924/17167
Date: 2025-04-14
Excerpt: "No ano de 2023, o Estado de Santa Catarina registrou 1.726.930 matrículas na educação básica, das quais 26.363 eram de estudantes migrantes... Distribuídas as matrículas de estudantes migrantes por dependências administrativas... Municipal 14.325; Estadual 9.407; Privada 2.453; Federal 178."
Context: Dados primários da SED-SC sobre matrículas de estrangeiros
Confidence: high

Claim: As três principais nacionalidades de estudantes migrantes em SC em 2023 foram: Venezuela (16.130 matrículas), Haiti (3.005) e Argentina (1.498). Outras nacionalidades incluem Paraguai, Cuba, Estados Unidos, Portugal, Bolívia e Colômbia [^78^].
Source: Revista Aracê (dados SED-SC)
URL: https://periodicos.newsciencepubl.com/arace/article/download/4418/5924/17167
Date: 2025-04-14
Excerpt: "Em primeiro lugar, os originários da Venezuela (16.130 matrículas); em segundo, do Haiti (3.005 matrículas); e, em terceiro lugar, da Argentina (1.498 matrículas)."
Context: Nacionalidades dos estudantes migrantes em SC
Confidence: high

Claim: As cidades com mais estudantes migrantes na rede estadual de SC em 2023 foram: Chapecó (1.303), Florianópolis (840), Joinville (763), Blumenau (440) e São José (404). No total estadual, Chapecó lidera com 3.698 matrículas de migrantes (todas as redes) [^78^].
Source: Revista Aracê (dados SED-SC)
URL: https://periodicos.newsciencepubl.com/arace/article/download/4418/5924/17167
Date: 2025-04-14
Excerpt: "As dez cidades com o maior quantitativo de estudantes migrantes, na rede estadual de ensino, no ano de 2023, são: Chapecó 1.303; Florianópolis 840; Joinville 763; Blumenau 440; São José 404... A respeito das cidades com o maior número de estudantes migrantes, no Estado, sobressaem: Chapecó, com 3.698 matrículas; Joinville, com 3.026 matrículas; Florianópolis, com 2.396 matrículas."
Context: Distribuição geográfica dos estudantes migrantes em SC
Confidence: high

### 6.2 Programa PARE — Acolhimento a Refugiados e Migrantes

Claim: A SED-SC criou em agosto de 2021 o Programa de Acolhimento a Migrantes e Refugiados (PARE), considerado o único programa do tipo vinculado a uma rede estadual de ensino no Brasil. Em 2023, o programa atingiu 70 escolas estaduais, 134 turmas, 1.277 matrículas e 76 professores. Em 2024, expandiu para 87 escolas e 1.509 matrículas [^86^][^78^].
Source: SCTD / Revista Aracê
URL: https://sctd.com.br/educacao/sc-cria-programa-pioneiro-de-apoio-pedagogico-a-estudantes-migrantes/ ; https://periodicos.newsciencepubl.com/arace/article/download/4418/5924/17167
Date: 2025-09-06 / 2025-04-14
Excerpt: "O programa prevê atendimento no contraturno escolar ao menos duas vezes por semana... Em 2023, o programa registrou a adesão de 70 escolas da rede estadual, com o total de 134 turmas, 1.277 matrículas e 76 professores/as."
Context: Programa estadual específico para estudantes migrantes
Confidence: high

### 6.3 Portaria SED-SC nº 2083/2023

Claim: A Portaria SED-SC nº 2083, de 31/07/2023, regulamenta os procedimentos de matrícula, aproveitamento de estudos e transferência de alunos migrantes, refugiados, apátridas e solicitantes de refúgio na rede estadual. A matrícula é assegurada em qualquer ano/série mediante análise de documentação e/ou avaliação da escolarização anterior [^169^].
Source: Diário Oficial do Estado de SC
URL: https://portal.doe.sea.sc.gov.br/repositorio/2023/20230801/Jornal/22072.pdf
Date: 2023-08-01
Excerpt: "Art. 1º Fica assegurada ao aluno migrante, refugiado, apátrida, solicitante de refúgio ou que tenha realizado estudos no exterior, a matrícula escolar em qualquer ano/série da Educação Básica na rede Estadual de Ensino, em qualquer tempo..."
Context: Normativa estadual sobre matrícula de estrangeiros
Confidence: high

---

## 7. Censo IBGE 2022: Variáveis de Nacionalidade e Escolaridade

Claim: O Censo 2022 investigou variáveis que permitem cruzamento entre migração e educação: Nacionalidade, País estrangeiro de nascimento, Ano que fixou residência no Brasil, Frequenta escola ou creche, Curso que frequenta, Série/ano que frequenta, Nível de instrução, e País estrangeiro que frequentava escola ou creche [^554^].
Source: IBGE
URL: https://www.ibge.gov.br/estatisticas/sociais/populacao/22827-censo-demografico-2022.html
Date: 2022-12-25
Excerpt: "Nacionalidade; Ano que fixou residência no Brasil; País estrangeiro de nascimento; Frequenta escola ou creche; Curso que frequenta; Série/ano que frequenta; Nível de instrução; País estrangeiro que frequentava escola ou creche"
Context: Variáveis do Censo 2022 com potencial de cruzamento migração-educação
Confidence: high

---

## 8. Legislação e LGPD

### 8.1 Resolução CNE nº 1/2020

Claim: O Conselho Nacional de Educação aprovou a Resolução nº 1/2020 que assegura o direito de matrícula de crianças e adolescentes migrantes, refugiados, apátridas e solicitantes de refúgio nas redes públicas de educação básica, sem discriminação em razão de nacionalidade ou condição migratória [^190^][^286^].
Source: Agência Brasil / Casa Civil
URL: https://agenciabrasil.ebc.com.br/educacao/noticia/2020-11/cne-garante-matricula-de-estudantes-estrangeiros-na-rede-publica ; https://www.gov.br/casacivil/pt-br/assuntos/noticias/2020/novembro/conselho-nacional-de-educacao-garante-direito-de-matricula-de-criancas-e-adolescentes-migrantes-e-refugiados
Date: 2020-11-16
Excerpt: "O Conselho Nacional de Educação (CNE) aprovou medida que assegura o direito de matrícula de crianças e adolescentes migrantes, refugiados, apátridas e solicitantes de refúgio nas redes públicas de educação básica brasileiras."
Context: Norma federal sobre matrícula de migrantes
Confidence: high

### 8.2 LGPD e Compartilhamento de Dados

Claim: A LGPD permite o uso compartilhado de dados pelo Poder Público para execução de políticas públicas (art. 26), desde que formalizado, com finalidade específica, base legal indicada e prazo de duração estabelecido. A anonimização dispensa o consentimento do titular para fins de pesquisa [^594^][^598^].
Source: AGE-MG / Ministério da Saúde
URL: https://lgpd.seguranca.mg.gov.br/storage/documentos/3/x7Q2GhIZ4D81IB1OSsxQ4HgpLAvQ9TuWKih3vEEw.pdf ; https://sisaps.saude.gov.br/sistemas/esusaps/docs/manual/LGPD/
Date: Não informado
Excerpt: "Art. 25. Os dados deverão ser mantidos em formato interoperável e estruturado para o uso compartilhado, com vistas à execução de políticas públicas... Art. 26. O uso compartilhado de dados pessoais pelo Poder Público deve atender a finalidades específicas de execução de políticas públicas."
Context: Base legal para integração de bases governamentais
Confidence: high

---

## 9. Iniciativas Nacionais de Integração de Dados

### 9.1 Plataforma Integrada do IBGE/Serpro

Claim: O IBGE desenvolveu nova plataforma de geodados em parceria com o Serpro (Singed — Sistema Nacional Soberano de Geociência, Estatísticas e Dados), envolvendo 8 ministérios. A ferramenta cruza informações do Censo 2022, PNAD Contínua, RAIS e Cadastro Único com imagens de satélite, permitindo inferências sobre deslocamentos populacionais, expansão urbana e evasão escolar [^626^].
Source: Poder360
URL: https://www.poder360.com.br/opiniao/governanca-preditiva-o-salto-de-dados-do-ibge/
Date: 2025-08-08
Excerpt: "Ao cruzar informações do Censo 2022, da Pnad Contínua, da Rais e do Cadastro Único com imagens de satélite, a plataforma permite inferências que antes exigiam longos prazos ou estavam fora do alcance técnico do setor público. É possível estimar deslocamentos populacionais, mapear áreas de expansão urbana irregular ou identificar sinais precoces de evasão escolar."
Context: Iniciativa federal de integração de bases
Confidence: medium

### 9.2 Data for Good — SC

Claim: Santa Catarina integra o movimento mundial Data for Good, coordenado pela Secretaria de Estado da Administração, com cronograma de ações para disponibilizar aos gestores públicos uma fonte integrada de informações base de estudo para tomada de decisões [^526^].
Source: SEA-SC
URL: https://www.sea.sc.gov.br/blog/santa-catarina-integra-movimento-mundial-para-uso-de-dados-na-gestao-publica/
Date: 2025-05-21
Excerpt: "O intuito é disponibilizar aos gestores públicos uma fonte integrada de informações que seja base de estudo para tomada de decisões. Com esta 'inteligência de dados' disponível podemos esperar maior assertividade e eficiência nas decisões."
Context: Movimento estadual de uso de dados na gestão pública
Confidence: medium

---

## 10. Limitações, Contradições e Lacunas

### 10.1 Ausência de Dados Abertos sobre Matrículas de Estrangeiros

Claim: O portal dados.sc.gov.br da SED-SC não disponibiliza datasets sobre matrículas de estrangeiros ou migrantes. Acesso a esses dados requer contato direto com a equipe técnica do SIDEP, como demonstrado por pesquisadores acadêmicos [^14^][^78^].
Source: Verificação própria no portal + Revista Aracê
URL: https://dados.sc.gov.br/ne/organization/sed ; https://periodicos.newsciencepubl.com/arace/article/download/4418/5924/17167
Date: 2025-12-12 / 2025-04-14
Context: Dados sobre matrículas de estrangeiros existem internamente mas não são abertos
Confidence: high

### 10.2 Descontinuação de Informações sobre Estrangeiros nos Relatórios do Censo Escolar

Claim: A partir de 2020, os relatórios técnicos agregados do Censo Escolar descontinuaram a divulgação específica de informações sobre estudantes estrangeiros, embora as variáveis continuem existindo nos microdados [^78^].
Source: Revista Aracê
URL: https://periodicos.newsciencepubl.com/arace/article/download/4418/5924/17167
Date: 2025-04-14
Excerpt: "Contudo, as últimas edições do relatório do Censo Escolar descontinuaram as informações de estudantes estrangeiros."
Context: Redução da transparência federal sobre estrangeiros na educação básica
Confidence: medium

### 10.3 Não Integração Direta entre Bases

Claim: Não foi identificada nenhuma integração direta e automatizada entre as bases de dados de imigração (SISMIGRA/Polícia Federal) e os sistemas educacionais de SC (SISGESC/SIDEP). O cruzamento depende de trabalho manual ou de solicitações específicas entre órgãos [^78^][^590^].
Source: Análise integrada das fontes
URL: N/A
Date: 2025-12-12
Context: Ausência de integração direta entre bases migratórias e educacionais
Confidence: high

### 10.4 Limitações do SISMIGRA

Claim: O SISMIGRA não atualiza periodicamente as exclusões referentes à re-emigração ou óbito, e não captura imigrantes em situação irregular documental. Além disso, seu propósito é controle de entrada/saída, não compreensão das condições de vida dos imigrantes [^592^].
Source: IMB / OBMigra
URL: https://goias.gov.br/imb/wp-content/uploads/sites/29/2024/01/Estudo_007_2023_imigracao_internacional_em_goias.pdf
Date: 2024-01
Excerpt: "Entre suas limitações está a não atualização periódica das exclusões referentes à re-emigração ou óbito... Dessa forma, a quantidade de imigrantes internacionais pode ser maior que a aqui analisada."
Context: Subnotificação de imigrantes nas bases administrativas
Confidence: high

---

## 11. Possibilidades de Cruzamento de Bases

Com base nas fontes investigadas, identificam-se as seguintes possibilidades de cruzamento para estimar/mapear estudantes estrangeiros matriculados na rede pública de SC:

| Base 1 | Base 2 | Variável de Cruzamento | Viabilidade |
|--------|--------|------------------------|-------------|
| Censo Escolar (INEP) | — | TP_NACIONALIDADE + NOME_PAIS_CE + CO_MUNICIPIO_END | **Alta** — microdados disponíveis publicamente |
| SED-SC (SIDEP/SISGESC) | — | Matrículas por nacionalidade (interno) | **Alta** — dados existem, mas não são abertos |
| Censo IBGE 2022 | Censo Escolar | Município + faixa etária + nacionalidade | **Média** — necessita anonimização e tratamento estatístico |
| SISMIGRA (PF) | SED-SC | UF + município de residência | **Baixa/Média** — necessita acordo interinstitucional e LGPD |
| RAIS/CAGED | SED-SC | Município + idade dos filhos (indireto) | **Baixa** — não há variável de parentesco direta |
| Cadastro Único | SED-SC | CPF da criança + município | **Baixa/Média** — necessita formalização e LGPD |
| Datasus (SISAB/e-SUS) | SED-SC | CPF/CNS + município | **Baixa/Média** — dados de saúde são sensíveis (LGPD) |
| SC em Territórios | SED-SC | Geolocalização + dados migratórios | **Média** — potencial para visualização espacial |

---

## 12. Resumo Executivo

### Achados Principais

1. **Santa Catarina é o principal destino de migrantes do Brasil**: o estado registrou o maior saldo migratório do país no Censo 2022 (354.350 pessoas entre 2017-2022) e o número de estrangeiros mais que triplicou (de 11.671 para 72.793). Os principais grupos são venezuelanos (54%), haitianos (15,7%) e argentinos (5%).

2. **A SED-SC possui dados primários sobre matrículas de estrangeiros**: em 2023, havia 26.363 estudantes migrantes na educação básica catarinense, sendo 9.407 na rede estadual. Os dados são mantidos pelo SIDEP (Sistema de Inteligência de Dados Educação na Palma da Mão) e pela equipe técnica da SED, mas **não são disponibilizados como dados abertos** no portal dados.sc.gov.br.

3. **O Censo Escolar (INEP) possui variáveis para identificar estrangeiros**: TP_NACIONALIDADE e NOME_PAIS_CE existem nos microdados, permitindo análise independente. Contudo, os relatórios técnicos agregados descontinuaram a divulgação específica sobre estudantes estrangeiros a partir de 2020.

4. **SC possui infraestrutura avançada de integração de dados**: a Plataforma BoaVista (CIASC) consolida ~140 conjuntos de dados de 35 entidades públicas, incluindo a Secretaria de Educação. A SEF-SC opera o SAT-Datalake com 350TB+ de dados. A SEPLAN desenvolve o SC em Territórios e a IDE/SC para dados espaciais.

5. **Não existe integração direta entre bases migratórias e educacionais**: não foi identificado nenhum sistema automatizado que cruze dados do SISMIGRA/Polícia Federal, RNE/CRNM, RAIS ou Cadastro Único com os sistemas educacionais de SC. O cruzamento depende de trabalho manual, solicitações pontuais ou pesquisa acadêmica.

6. **A LGPD permite o compartilhamento** para execução de políticas públicas (art. 25 e 26), desde que formalizado, com finalidade específica e adoção de medidas de segurança. A anonimização dos dados dispensa o consentimento do titular para fins de pesquisa.

7. **Iniciativas de integração nacional estão em desenvolvimento**: o IBGE/Serpro criou plataforma integrada (Singed) que cruza Censo, PNAD, RAIS e Cadastro Único. O DataMigra (MJSP/OBMigra) permite cruzamento de variáveis de imigração internacional.

### Recomendações

- **Curto prazo**: Formalizar acordo entre SED-SC e CIASC para incluir painel de matrículas de estrangeiros no portal de dados abertos, respeitando a LGPD.
- **Médio prazo**: Desenvolver cruzamento sistemático entre microdados do Censo Escolar e dados do Censo IBGE 2022 por município, utilizando anonimização estatística.
- **Longo prazo**: Implementar interoperabilidade entre SISGESC/SIDEP e bases federais (SISMIGRA, Cadastro Único, Datasus) via Plataforma BoaVista, com governança de dados e compliance com a LGPD.

---

*Relatório elaborado em dezembro de 2025. Fontes primárias verificadas: sites governamentais (SED-SC, CIASC, SEPLAN, SEA, SEF-SC, IBGE, INEP, MJSP, MDS, Ministério da Saúde), portais oficiais (dados.sc.gov.br, portaldeimigracao.mj.gov.br), documentos oficiais (DOE/SC, Resolução CNE nº 1/2020), estudos acadêmicos (Revista Aracê, Revista Momento, TCC UFSC) e reportagens de veículos de referência (G1, Agência Brasil, NSC Total).*
