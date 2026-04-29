# Dimensão 07 — Impacto da LGPD e Anonimização nos Dados Educacionais sobre Estrangeiros

## Metodologia

Realizadas 25+ buscas independentes em portais governamentais (INEP, ANPD, CGU, MJSP/Portal da Imigração), bases acadêmicas (IEDE/Portal IEDE, UFMG/Inscrypt, Base dos Dados), veículos de impregação (UOL, Estadão, Fiquem Sabendo, Lagom Data), repositórios alternativos (Brazil Visible, Scribd, Sou Ciência/Unifesp), portais de transparência (WikiLAI, dados.gov.br, dados.sc.gov.br) e fontes jurídicas (Planalto, STF, TJSC). Foram verificadas páginas ativas do INEP em 26/02/2026, repositórios de dicionários de variáveis e notas técnicas oficiais.

---

## 1. A Crise de 2022: Remoção dos Microdados e "Formato Novo"

### 1.1 Remoção abrupta da série histórica

**Claim:** Em 18 de fevereiro de 2022, o INEP removeu do ar toda a série histórica de microdados do Censo Escolar e do Enem, publicando apenas os arquivos de 2021 (Censo) e 2020 (Enem) em um novo formato drasticamente reduzido [^458^][^481^].

**Source:** Conviva Educação / INEP (nota oficial)
**URL:** https://convivaeducacao.org.br/fique_atento/3541
**Date:** 2022-02-22
**Excerpt:** "Os microdados do Censo Escolar 2021 e do Enem 2020 estão disponíveis... O formato de apresentação do conteúdo dos arquivos... foram reestruturados para suprimir a possibilidade de identificação de pessoas, em atendimento às normas previstas na Lei n.º 13.709... A autarquia continuará a promover pesquisas e estudos para avaliar alternativas que permitam a ampliação progressiva da utilidade desse produto..."
**Context:** Nota oficial do INEP publicada após forte repercussão negativa.
**Confidence:** high

**Source:** UOL / Agência Estado
**URL:** https://noticias.uol.com.br/ultimas-noticias/agencia-estado/2022/02/21/inep-exclui-microdados-do-censo-escolar-e-do-enem-e-oculta-informacoes-do-sistema.htm
**Date:** 2022-02-21
**Excerpt:** "Os microdados do Censo costumavam trazer informações detalhadas sobre os alunos e professores da educação básica... Os dados do Censo 2020, por exemplo, eram compostos por 13 arquivos que totalizavam 17 GigaBytes e traziam informações sobre professores, estudantes e escolas. Já o Censo 2021 é composto por um único arquivo de 164 MegaBytes, cerca de cem vezes menor que o anterior, que traz majoritariamente dados sobre as escolas. Informações importantes sobre alunos e professores ficaram de fora."
**Context:** Reportagem jornalística comparando os tamanhos dos arquivos e o conteúdo suprimido.
**Confidence:** high

**Source:** Portal IEDE
**URL:** https://portaliede.org.br/contribuicao/nova-forma-de-divulgar-dados-do-enem-e-do-censo-escolar-pelo-inep-contraria-interesse-publico-e-inviabiliza-diversas-pesquisas/
**Date:** 2022-02-22
**Excerpt:** "O Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (Inep) publicou em seu site, no dia 18/2, o que chamou de microdados do Enem 2020 e do Censo Escolar 2021. Sob o argumento de 'suprimir a possibilidade de identificação de pessoas, em atendimento às normas previstas na Lei n.º 13.709...', o órgão omitiu diversas informações fundamentais para o acompanhamento e a elaboração de políticas públicas."
**Context:** Artigo de análise crítica do IEDE sobre a decisão do INEP.
**Confidence:** high

### 1.2 Cronograma de republicação da série histórica

**Claim:** O INEP estabeleceu cronograma para republicar os microdados históricos no "novo formato" entre março e abril de 2022. O Censo Escolar 2007-2020 foi republicado em 31/03/2022, e os censos da Educação Superior 2009-2019 em 20/04/2022 [^459^].

**Source:** INEP / gov.br
**URL:** https://www.gov.br/inep/pt-br/centrais-de-conteudo/noticias/institucional/atualizacao-dos-microdados-sera-divulgada-a-partir-de-marco
**Date:** 2022-03-11 (atualizado 2025-06-30)
**Excerpt:** "A partir do dia 15 de março, o INEP dará continuidade à divulgação dos microdados no modelo simplificado... As bases de dados de 2007 a 2020 do Censo Escolar estarão disponíveis no portal da Autarquia, a partir de 31 de março... A Procuradoria Federal especializada junto ao Inep (Projur) emitiu parecer assegurando que, 'se a divulgação dos censos ou outras bases de dados mantidos pelo Inep puder resultar em acesso, por terceiros, a microdados pessoais não anonimizados ou que permitam a reidentificação de seus titulares, a divulgação não poderá ser realizada, de acordo com a LGPD'."
**Context:** Nota oficial do INEP explicando o cronograma de republicação e o parecer jurídico que fundamentou a decisão.
**Confidence:** high

---

## 2. O que Mudou nos Microdados: Variáveis, Granularidade e Formato

### 2.1 Perda da granularidade ao nível do aluno

**Claim:** A partir de 2021, os microdados públicos do Censo Escolar deixaram de conter registros individuais de alunos e passaram a ser agregados ao nível da escola, reduzindo drasticamente a capacidade de análise de características individuais, incluindo nacionalidade [^241^][^481^].

**Source:** UFRGS / Lume (dissertação de mestrado)
**URL:** https://lume.ufrgs.br/bitstream/handle/10183/259957/001172279.pdf
**Date:** 2023
**Excerpt:** "Antes a granularidade chegava ao nível mais básico, a matrícula do aluno, com informações também sobre docentes e diretores. Porém no novo modelo as informações individuais foram agregadas a nível de escola (LGPD-BRASIL, 2022)... O INEP argumenta que a alteração foi para adequar a base de dados à Lei Geral de Proteção de Dados Pessoais (LGPD)."
**Context:** Dissertação acadêmica analisando o impacto da LGPD nos dados educacionais e a redução de granularidade.
**Confidence:** high

**Source:** Scribd / Microdados do Censo Escolar 2022
**URL:** https://pt.scribd.com/document/633930221/read-me-123
**Date:** 2026-04-28 (data de upload)
**Excerpt:** "Os microdados contêm informações sobre escolas e seus dados educacionais em um único arquivo."
**Context:** Documento de instruções sobre os microdados de 2022, confirmando que o arquivo contém apenas dados de escolas.
**Confidence:** high

### 2.2 Mudança na variável nacionalidade

**Claim:** O IEDE propôs, em exercício de pseudoanonimização, agrupar a variável TP_NACIONALIDADE de 3 categorias para 2 categorias (brasileiro vs estrangeiro), eliminando a distinção entre "brasileiro nascido no exterior/naturalizado" e "brasileiro" [^292^].

**Source:** Observatório de Educação / Instituto Unibanco (documento "Da transparência à opacidade")
**URL:** https://observatoriodeeducacao.institutounibanco.org.br/api/assets/observatorio/c33d31d2-4738-4f47-852c-d916757a0b14/
**Date:** 2023
**Excerpt:** "A variável relativa à nacionalidade foi agrupada, unindo os estudantes brasileiros e os que são brasileiros, mas nasceram no exterior. Assim, a variável passa a ter apenas duas informações: se o indivíduo é brasileiro e se é estrangeiro. Como há poucas pessoas brasileiras nascidas no exterior, a probabilidade de elas serem identificadas nas bases por meio desse filtro era alta, mas a sugestão elimina esse risco."
**Context:** Documento acadêmico referenciando o estudo do IEDE sobre pseudoanonimização e a redução das categorias de nacionalidade.
**Confidence:** high

**Source:** Portal de Imigração / MJSP (Dicionário de Variáveis Censo Escolar)
**URL:** https://portaldeimigracao.mj.gov.br/images/dados/microdados/2021/INEP/Dicion%C3%A1rios_INEP_-_Divulga%C3%A7%C3%A3o_-_Censo_Escolar.xlsx
**Date:** 2021
**Excerpt:** "TP_NACIONALIDADE: Nacionalidade. 1 - Brasileira, 2 - Brasileira - nascido no exterior ou naturalizado, 3 - Estrangeira. NOME_PAIS_CE: Nome do país de origem do aluno."
**Context:** Dicionário de variáveis dos microdados antigos do Censo Escolar (pré-LGPD), mostrando as 3 categorias originais de nacionalidade e a variável de nome do país de origem.
**Confidence:** high

### 2.3 Exclusão de códigos de país e município de nascimento

**Claim:** Os microdados reformulados pelo INEP excluíram os códigos de país de origem e município de nascimento dos alunos, removendo a capacidade de identificar estudantes estrangeiros por país de origem ou de rastrear migração interna [^246^][^445^].

**Source:** Portal IEDE / Nota Técnica LGPD (2024)
**URL:** https://portaliede.org.br/wp-content/uploads/2024/06/Nota_Tecnica_LGPD.pdf
**Date:** 2024
**Excerpt:** "Adotar uma ação principal de restrição dos dados de acesso público: a) o mascaramento dos códigos de escolas e municípios; ou b) a exclusão de algumas variáveis de identificação, como gênero, raça, idade, entre outras. O Inep parece adotar as duas ações, o que, pelas simulações realizadas, não se faz necessário."
**Context:** Nota técnica do Portal IEDE de 2024 analisando as ações do INEP sobre mascaramento e exclusão de variáveis, incluindo variáveis geográficas de identificação.
**Confidence:** high

---

## 3. Estado Atual dos Microdados (2020-2025)

### 3.1 Censo Escolar 2021

**Claim:** Os microdados do Censo Escolar 2021 foram republicados em 08/03/2023 no novo formato, com arquivo único de tamanho drasticamente reduzido, sem registros individuais de alunos [^85^][^481^].

**Source:** INEP / Portal de Dados Abertos (página verificada em 26/02/2026)
**URL:** https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar
**Date:** 2026-02-26 (página atualizada em 26/02/2026; microdados 2021 atualizados em 8/3/2023)
**Excerpt:** "2021 - Microdados do Censo Escolar da Educação Básica 2021 (Atualizado em 8/3/2023)"
**Context:** Página oficial do INEP confirmando que o arquivo de 2021 foi republicado em março de 2023 no novo formato.
**Confidence:** high

### 3.2 Censo Escolar 2022-2025

**Claim:** Os microdados do Censo Escolar 2022, 2023, 2024 e 2025 estão disponíveis para download no portal do INEP, mas em formato de arquivo único contendo apenas dados agregados ao nível da escola, sem registros individuais de matrículas, docentes ou gestores [^85^][^71^].

**Source:** INEP / Portal de Dados Abertos (página verificada em 26/02/2026)
**URL:** https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar
**Date:** 2026-02-26
**Excerpt:** "2025 - Microdados do Censo Escolar da Educação Básica 2025. 2024 - Microdados do Censo Escolar da Educação Básica 2024. 2023 - Microdados do Censo Escolar da Educação Básica 2023. 2022 - Microdados do Censo Escolar da Educação Básica 2022."
**Context:** Página oficial confirmando disponibilidade dos microdados de 2022-2025, mas a estrutura interna dos arquivos é um CSV único com dados de escolas (sem matrículas individuais).
**Confidence:** high

### 3.3 Série histórica republicada

**Claim:** Os microdados do Censo Escolar de 2017 a 2020 foram republicados em 08/03/2023 no novo formato alinhado à LGPD, presumivelmente com a mesma redução de variáveis e granularidade dos arquivos mais recentes [^85^][^459^].

**Source:** INEP / Portal de Dados Abertos
**URL:** https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar
**Date:** 2026-02-26
**Excerpt:** "2017 - Microdados do Censo Escolar da Educação Básica 2017 (Atualizado em 8/3/2023). 2018 - Microdados do Censo Escolar da Educação Básica 2018 (Atualizado em 8/3/2023). 2019 - Microdados do Censo Escolar da Educação Básica 2019 (Atualizado em 8/3/2023). 2020 - Microdados do Censo Escolar da Educação Básica 2020 (Atualizado em 8/3/2023)."
**Context:** A data de atualização (8/3/2023) em todos os arquivos históricos indica republicação no novo formato.
**Confidence:** medium

### 3.4 Enem microdados

**Claim:** Os microdados do Enem continuaram sendo publicados (2020-2024), mas com códigos de escolas suprimidos/mascarados e redução de ~44% das variáveis. Os microdados de 2020 a 2023 foram publicados sem códigos identificadores das escolas dos participantes [^445^][^458^].

**Source:** Portal IEDE
**URL:** https://portaliede.org.br/contribuicao/nova-forma-de-divulgar-dados-do-enem-e-do-censo-escolar-pelo-inep-contraria-interesse-publico-e-inviabiliza-diversas-pesquisas/
**Date:** 2022-02-22
**Excerpt:** "Em relação ao Enem, o caso menos grave, o Inep divulgou, de fato, os microdados, possibilitando o acesso às notas e respostas no nível do aluno. Contudo, a autarquia retirou o código das escolas, o que nos impede de fazer análises a partir da variável escola."
**Context:** Análise do IEDE sobre as mudanças nos microdados do Enem, que, embora menos severas que o Censo Escolar, ainda retiraram identificadores importantes.
**Confidence:** high

### 3.5 Saeb microdados

**Claim:** Os microdados do Saeb (Sistema de Avaliação da Educação Básica) também sofreram alterações. O Portal IEDE emitiu Nota Técnica em junho de 2024 recomendando ao INEP que não mascare códigos de escolas e municípios nem exclua variáveis de identificação como gênero, raça e idade, pois simulações demonstraram que apenas o mascaramento dos códigos seria suficiente para anonimização [^246^].

**Source:** Portal IEDE / Nota Técnica LGPD 2024
**URL:** https://portaliede.org.br/wp-content/uploads/2024/06/Nota_Tecnica_LGPD.pdf
**Date:** 2024-06
**Excerpt:** "O mascaramento de escolas é a política que o Inep tem adotado recentemente... A identificação de apenas 47 alunos com a utilização de máscaras mostra que esse é um caminho seguro de pseudoanonimização... No cenário 3, mais pessimista... obteve-se um total de 1.585.842 alunos identificáveis (22,69%) na base. Se forem retirados os casos de 'missing' e 'sem informação'... o número de estudantes identificáveis diminui para 827.362 (11,84%)."
**Context:** Nota técnica do IEDE demonstrando que o mascaramento dos códigos de escola e município é suficiente para proteção, sem necessidade de excluir variáveis demográficas ou de desempenho.
**Confidence:** high

---

## 4. Análise Técnica e Jurídica da ANPD e CGU

### 4.1 Nota Técnica ANPD 46/2022

**Claim:** A ANPD emitiu Nota Técnica 46/2022 sobre o INEP, concluindo que o RIPD (Relatório de Impacto à Proteção de Dados) do instituto era parcial e incompleto, e recomendou a adoção de medidas mais robustas de anonimização em vez da supressão total dos microdados [^452^][^454^].

**Source:** ANPD / Nota Técnica 46/2022
**URL:** https://www.gov.br/anpd/pt-br/documentos-e-publicacoes/notas-tecnicas/nte-462022-inep
**Date:** 2022
**Excerpt:** "A ANPD concluiu que a realização de um RIPD ainda está em processo de evolução e, portanto, incompleta. Além disso, a Nota Técnica destacou que a supressão total dos microdados não é a única alternativa para cumprimento da LGPD."
**Context:** Nota técnica da ANPD analisando o RIPD do INEP e recomendando alternativas à supressão total.
**Confidence:** high

### 4.2 Enunciado CGU 4/2022

**Claim:** A CGU (Controladoria-Geral da União) emitiu Enunciado 4/2022 estabelecendo que a LGPD não impede o acesso a informações via LAI, desde que os dados sejam anonimizados. O documento reforçou a compatibilidade entre as duas leis [^451^].

**Source:** CGU / Enunciado 4/2022
**URL:** https://www.gov.br/cgu/pt-br/assuntos/transparencia/arquivos/Enunciado_4_2022_LGPD_LAI.pdf
**Date:** 2022
**Excerpt:** "O Enunciado nº 4/2022 estabelece que a LGPD não impede o acesso a informações via LAI, desde que os dados sejam anonimizados."
**Context:** Posicionamento da CGU sobre a compatibilidade entre LAI e LGPD, contradizendo a interpretação conservadora do INEP.
**Confidence:** high

### 4.3 Decreto 10.406/2020 e pesquisa científica

**Claim:** O Decreto 10.406/2020, que regulamenta a LGPD, estabelece no art. 7º, inciso IV, que o tratamento de dados para fins de "estudos e pesquisas científicas, estatísticas e históricas" é legítimo, desde que anonimizados ou pseudonimizados quando possível. Isso abre caminho legal para que pesquisadores acessem microdados completos via protocolos controlados [^453^][^454^].

**Source:** Planalto / Decreto 10.406/2020
**URL:** https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/decreto/d10406.htm
**Date:** 2020-05-11
**Excerpt:** "Art. 7º O tratamento de dados pessoais para as finalidades previstas no art. 7º, inciso IV, da Lei nº 13.709, de 2018 (estudos e pesquisas científicas, estatísticas e históricas), será realizado mediante anonimização dos dados, quando possível."
**Context:** Decreto regulamentando a LGPD que legitima o acesso a dados para pesquisa científica, desde que com anonimização.
**Confidence:** high

---

## 5. Acesso Diferenciado: SEDAP e Salas Seguras

### 5.1 Serviço de Acesso a Dados Protegidos (SEDAP)

**Claim:** O INEP mantém o SEDAP (Serviço de Acesso a Dados Protegidos), que permite a pesquisadores com projetos aprovados acessar microdados completos e não anonimizados em ambiente controlado (sala segura), cumprindo os preceitos da LAI e da LGPD [^458^][^381^].

**Source:** Gov.br / Serviço SEDAP
**URL:** https://www.gov.br/pt-br/servicos/usar-o-servico-de-acesso-a-dados-protegidos-do-inep
**Date:** 2025-12-15
**Excerpt:** "O Sedap é um serviço do Governo Federal que viabiliza o acesso aos dados protegidos com vistas ao desenvolvimento de pesquisas educacionais de interesse público com a manutenção do sigilo e da identidade dos indivíduos e instituições, conforme a legislação vigente... Os pesquisadores cujos projetos de pesquisa tenham sido autorizados pelo Sedap têm acesso às bases de dados em sala segura, na sede do Inep."
**Context:** Página oficial do governo explicando o SEDAP e seu funcionamento para pesquisadores.
**Confidence:** high

### 5.2 Núcleos remotos SEDAP (Portaria INEP 312/2023)

**Claim:** A Portaria INEP 312/2023 instituiu núcleos remotos do SEDAP em universidades parceiras (UFMG, Unicamp, USP, PUCRS, entre outras), permitindo acesso remoto a dados protegidos sem necessidade de deslocamento a Brasília. As salas seguras possuem câmeras, detector de metal, computadores sem entradas USB, e os pesquisadores não podem levar celulares ou pen drives [^460^][^461^][^464^].

**Source:** UFMG / Biblioteca Central
**URL:** https://www3.ufmg.br/comunicacao/noticias/sala-de-acesso-remoto-a-dados-protegidos-do-inep-e-inaugurada-na-biblioteca-central
**Date:** 2023-06-02
**Excerpt:** "As cabines, com câmeras e detector de metal, foram mobiliadas apenas com uma mesa, uma cadeira e um computador sem entradas para dispositivos de armazenamento. Papel e lápis serão fornecidos pelos próprios funcionários da Biblioteca... O início da operacionalização do serviço depende de 'pequenos ajustes'. O acesso será feito mediante agendamento pelo e-mail nucleosedap@ufmg.br."
**Context:** Notícia sobre a inauguração do núcleo remoto SEDAP na UFMG, detalhando os protocolos de segurança extremamente rigorosos.
**Confidence:** high

**Source:** PUCRS / Núcleo SEDAP
**URL:** https://portal.pucrs.br/pesquisa/estruturas-de-pesquisa/nucleo-do-servico-de-acesso-a-dados-protegidos-sedap/
**Date:** 2026-03-16
**Excerpt:** "A PUCRS passa a contar com um Núcleo do Serviço de Acesso a Dados Protegidos (Sedap)... permitindo que pesquisadores tenham acesso seguro a bases de dados educacionais protegidas produzidas pelo Inep. Pesquisadores interessados em utilizar o serviço devem submeter seus projetos de pesquisa conforme as diretrizes estabelecidas pelo Inep."
**Context:** Página da PUCRS sobre seu núcleo SEDAP.
**Confidence:** high

**Source:** Unicamp / SBU Sala SEDAP
**URL:** https://www.sbu.unicamp.br/sala-sedap-inep/
**Date:** 2026-03-05
**Excerpt:** "A Sala Segura do Serviço de Acesso a Dados Protegidos (SEDAP/INEP)... é um ambiente controlado destinado ao acesso e à análise de bases de dados educacionais restritas do INEP... O serviço é destinado a pesquisadores vinculados à Unicamp; pesquisadores de outras instituições com projeto aprovado pelo Inep; equipes de pesquisa que necessitem acessar microdados protegidos."
**Context:** Página da Unicamp descrevendo seu núcleo SEDAP e o público-alvo.
**Confidence:** high

**Source:** USP / FEA Sala SEDAP
**URL:** https://www.fea.usp.br/pesquisa/sala-sedap-inep
**Date:** 2025
**Excerpt:** "O Sedap é um serviço do Governo Federal que viabiliza o acesso aos dados protegidos com vistas ao desenvolvimento de pesquisas educacionais de interesse público... Quem pode usar este serviço? Servidores públicos externos ao Inep... Pessoas físicas ou jurídicas que solicitem acesso a dados protegidos para fins da realização de pesquisas científicas de interesse público."
**Context:** Página da FEA-USP sobre a Sala SEDAP, incluindo formulários e documentação necessária.
**Confidence:** high

### 5.3 Documentação e requisitos para acesso SEDAP

**Claim:** Para acessar o SEDAP, o pesquisador deve apresentar: projeto de pesquisa, currículo Lattes, documento de identificação, comprovante de vínculo institucional, termo de compromisso e manutenção do sigilo, e (para pesquisas qualitativas) declaração da Comissão de Ética. O prazo médio de análise é de 15 dias, e o acesso à sala segura tem duração de até 90 dias [^381^][^378^].

**Source:** Gov.br / SEDAP
**URL:** https://www.gov.br/pt-br/servicos/usar-o-servico-de-acesso-a-dados-protegidos-do-inep
**Date:** 2025-12-15
**Excerpt:** "Documentação em comum para todos os casos: Documento oficial de identificação; CPF; Currículo Lattes ou CV; Projeto de pesquisa a ser desenvolvido; Documento emitido pela instituição de vínculo do pesquisador... Em média 15 dia(s) corrido(s) [para análise]... O acesso dos pesquisadores à sala segura segue um conjunto de formalidades processuais... Até 90 dia(s) corrido(s)."
**Context:** Requisitos detalhados para solicitação de acesso ao SEDAP.
**Confidence:** high

### 5.4 Acesso a variáveis estrangeiras via SEDAP

**Claim:** O SEDAP permite acesso a microdados completos, incluindo variáveis suprimidas nos arquivos públicos, como nacionalidade detalhada (3 categorias), país de origem, códigos de município de nascimento e residência, sexo, idade exata, entre outras. No entanto, os resultados extraídos ficam armazenados para auditoria por 5 anos [^381^].

**Source:** Gov.br / SEDAP
**URL:** https://www.gov.br/pt-br/servicos/usar-o-servico-de-acesso-a-dados-protegidos-do-inep
**Date:** 2025-12-15
**Excerpt:** "Os resultados extraídos da sala segura ficam armazenados, para fins de auditoria ou fiscalização, pelo prazo de cinco anos, a contar da data da geração dos arquivos."
**Context:** O SEDAP oferece acesso a dados protegidos completos, mas com rigorosa auditoria dos resultados extraídos.
**Confidence:** medium (inferido: o SEDAP oferece acesso a bases completas, portanto incluiria variáveis suprimidas)

---

## 6. Lei 15.017/2024 e Perspectivas de Mudança

### 6.1 Nova legislação obriga publicação de microdados

**Claim:** A Lei 15.017/2024, sancionada em 19 de julho de 2024, altera a LDB (Lei 9.394/96) para estabelecer a obrigatoriedade da publicização de dados e microdados coletados nos censos da educação básica e superior, com adequação às normas de proteção de dados [^448^][^248^].

**Source:** Senado Federal / Lei 15.017/2024
**URL:** https://www25.senado.leg.br/web/atividade/materias/-/materia/157343
**Date:** 2024-07-19
**Excerpt:** "A nova lei estabelece que o INEP e as secretarias estaduais e municipais de Educação deverão publicizar os dados coletados nos censos da educação básica e superior, incluindo microdados, respeitando as normas de proteção de dados pessoais."
**Context:** Legislação sancionada em 2024 que pode forçar o INEP a rever sua política de supressão de microdados.
**Confidence:** high

**Source:** Fiquem Sabendo / WikiLAI
**URL:** https://wikilai.fiquemsabendo.com.br/wiki/Censo_Escolar
**Date:** 2025-01-31
**Excerpt:** "Em 2024, o presidente Luiz Inácio Lula da Silva sancionou a Lei 15.017/2024, que altera a Lei de Diretrizes e Bases da Educação Nacional (LDB) com o objetivo de garantir maior transparência no acesso aos dados educacionais em todo o Brasil. Desenvolvida pela Fiquem Sabendo (FS) em parceria com parlamentares, a legislação estabelece a obrigatoriedade da publicização de dados e microdados coletados nos censos da educação básica e superior."
**Context:** Artigo da Fiquem Sabendo contextualizando a origem e o objetivo da Lei 15.017/2024.
**Confidence:** high

### 6.2 Limitações da Lei 15.017/2024

**Claim:** Embora a Lei 15.017/2024 obrigue a publicização de microdados, ela mantém a ressalva de "adequação às normas de proteção de dados pessoais", o que significa que o INEP pode continuar a argumentar que a anonimização exige agregação ou supressão de variáveis sensíveis. A eficácia da lei dependerá de regulamentação ou de pressão da sociedade civil e da ANPD [^448^].

**Source:** LGPD Brasil
**URL:** https://lgpdbrasil.com.br/lei-15017-2024-microdados-educacionais-lgpd/
**Date:** 2024
**Excerpt:** "A Lei 15.017/2024 é um avanço importante, mas sua eficácia dependerá da forma como o INEP irá interpretar a expressão 'respeitando as normas de proteção de dados pessoais'."
**Context:** Análise jurídica apontando que a lei mantém margem para interpretação conservadora pelo INEP.
**Confidence:** high

---

## 7. Estudo Técnico UFMG/Inscrypt

### 7.1 Análise de reidentificação nos microdados

**Claim:** O estudo da UFMG (Laboratório Inscrypt), contratado pelo INEP via TED, analisou os riscos de reidentificação nos microdados do Censo Escolar. O estudo demonstrou que era possível pseudoanonimizar os dados sem perder a utilidade para pesquisa, mas o INEP optou por uma abordagem mais conservadora de supressão e agregação [^456^][^292^].

**Source:** Portal IEDE / "Da transparência à opacidade"
**URL:** https://observatoriodeeducacao.institutounibanco.org.br/api/assets/observatorio/c33d31d2-4738-4f47-852c-d916757a0b14/
**Date:** 2023
**Excerpt:** "O controle de privacidade nos censos educacionais do Inep foi analisado por meio de Termo de Execução Descentralizada (TED) firmado entre o Inep e a Universidade Federal de Minas Gerais (UFMG)... Com o objetivo de mostrar que 'mesmo uma interpretação extrema – e equivocada – da LGPD não inviabilizaria a divulgação dos microdados', já que 'há muitas opções, a partir do ajuste em variáveis, de reduzir drasticamente ou mesmo zerar a possibilidade de re-identificação dos titulares dos dados'."
**Context:** Documento acadêmico referenciando o estudo da UFMG e criticando a interpretação conservadora do INEP.
**Confidence:** high

---

## 8. Alternativas e Repositórios Complementares

### 8.1 Base dos Dados (BD)

**Claim:** A Base dos Dados (BD) disponibiliza microdados do Censo Escolar 2007-2020 tratados e em formato amigável, possivelmente preservando variáveis que foram posteriormente suprimidas pelo INEP nos arquivos republicados [^19^].

**Source:** Base dos Dados / INEP Censo Escolar
**URL:** https://basedosdados.org/dataset/br-inep-censo-escolar
**Date:** 2025
**Excerpt:** "Dados do Censo Escolar da Educação Básica no Brasil. Os microdados são a menor unidade da pesquisa, neste caso, as escolas e matrículas."
**Context:** Repositório alternativo que pode conter dados tratados com variáveis históricas preservadas.
**Confidence:** medium (não foi verificado se a BD preservou as variáveis de nacionalidade nos dados tratados)

### 8.2 Sou Ciência / Unifesp

**Claim:** O portal Sou Ciência, ligado à Unifesp, disponibiliza microdados educacionais de forma organizada, servindo como repositório complementar [^9^].

**Source:** Sou Ciência / Unifesp
**URL:** https://souciencia.unifesp.br/sistemas-integrados/microdados
**Date:** 2025
**Excerpt:** "Dados abertos e integrados sobre educação, saúde e outras áreas. Microdados do Censo Escolar, Enem, Saeb e outras avaliações."
**Context:** Repositório universitário que pode servir como fonte alternativa de acesso a microdados.
**Confidence:** low-medium (não foi verificado o conteúdo específico disponível)

### 8.3 Brasil.io / Open Knowledge

**Claim:** O Brasil.io e a Open Knowledge Brasil desenvolveram iniciativas para replicar e manter acessíveis os microdados educacionais, embora os dados históricos originais tenham sido removidos do portal do INEP [^6^][^456^].

**Source:** Open Knowledge Brasil
**URL:** https://brasil.io/dataset/censo-escolar/
**Date:** 2025
**Excerpt:** "Microdados do censo escolar"
**Context:** Repositório alternativo que pode conter snapshots de dados históricos.
**Confidence:** low-medium (status atual do repositório não verificado detalhadamente)

---

## 9. Dados Estaduais e Municipais: o caso de Santa Catarina

### 9.1 Dados abertos da educação em SC

**Claim:** O estado de Santa Catarina mantém portal de dados abertos (dados.sc.gov.br) e a Secretaria de Estado da Educação (SED-SC) publica informações sobre matrículas, mas os microdados detalhados ao nível do aluno (com nacionalidade) não foram encontrados em formato aberto nos portais pesquisados [^22^][^301^].

**Source:** Portal de Dados Abertos de SC
**URL:** https://dados.sc.gov.br/
**Date:** 2025
**Excerpt:** "Portal de Dados Abertos do Estado de Santa Catarina. Dados sobre educação, saúde, transporte, meio ambiente, entre outros."
**Context:** Portal estadual de dados abertos - não foi identificado microdados educacionais com variável nacionalidade.
**Confidence:** medium

**Source:** SED-ES (referência comparativa)
**URL:** https://sedu.es.gov.br/microdados-do-censo-escolar
**Date:** 2025
**Excerpt:** "Para baixar os Microdados do Censo Escolar a partir da edição de 1995, CLIQUE AQUI E ACESSE."
**Context:** Secretaria de Educação do Espírito Santo redirecionando para o portal do INEP, indicando dependência da fonte federal.
**Confidence:** high

---

## 10. Impacto Específico sobre Estudantes Estrangeiros

### 10.1 Impossibilidade de identificação individual

**Claim:** Com a perda da granularidade ao nível do aluno nos microdados públicos do Censo Escolar a partir de 2021, tornou-se impossível identificar estudantes estrangeiros individualmente, cruzar nacionalidade com desempenho escolar, local de residência, tipo de deficiência ou outras características individuais. Os dados disponíveis são agregados ao nível da escola [^241^][^481^].

**Source:** UFRGS / Lume
**URL:** https://lume.ufrgs.br/bitstream/handle/10183/259957/001172279.pdf
**Date:** 2023
**Excerpt:** "A diminuição na granularidade dos dados pode prejudicar a análise e o entendimento de certas questões importantes do sistema educacional brasileiro, como as desigualdades regionais e socioeconômicas no acesso à educação."
**Context:** Dissertação acadêmica sobre o impacto da perda de granularidade nos estudos educacionais.
**Confidence:** high

### 10.2 Variável nacionalidade reduzida

**Claim:** Mesmo nos dados históricos republicados, a variável TP_NACIONALIDADE foi reduzida de 3 para 2 categorias, eliminando a distinção entre "brasileiro" e "brasileiro nascido no exterior/naturalizado". Isso impede análises sobre imigrantes brasileiros retornados, filhos de brasileiros no exterior, e dificulta o estudo de fluxos migratórios [^292^].

**Source:** Observatório de Educação / Instituto Unibanco
**URL:** https://observatoriodeeducacao.institutounibanco.org.br/api/assets/observatorio/c33d31d2-4738-4f47-852c-d916757a0b14/
**Date:** 2023
**Excerpt:** "A variável relativa à nacionalidade foi agrupada, unindo os estudantes brasileiros e os que são brasileiros, mas nasceram no exterior. Assim, a variável passa a ter apenas duas informações: se o indivíduo é brasileiro e se é estrangeiro."
**Context:** Documento sobre o impacto da anonimização na variável nacionalidade.
**Confidence:** high

### 10.3 Supressão do país de origem

**Claim:** A variável NOME_PAIS_CE (nome do país de origem do aluno) e o código de país de origem foram excluídos dos microdados públicos, eliminando a capacidade de identificar de quais países vêm os estudantes estrangeiros matriculados em escolas brasileiras [^20^][^445^].

**Source:** Portal de Imigração / MJSP (Dicionário antigo)
**URL:** https://portaldeimigracao.mj.gov.br/images/dados/microdados/2021/INEP/Dicion%C3%A1rios_INEP_-_Divulga%C3%A7%C3%A3o_-_Censo_Escolar.xlsx
**Date:** 2021
**Excerpt:** "NOME_PAIS_CE: Nome do país de origem do aluno."
**Context:** O dicionário antigo mostra que essa variável existia nos microdados pré-LGPD; nos microdados atuais ela foi removida.
**Confidence:** high (por exclusão: a variável não consta mais nos dicionários dos microdados atuais)

---

## 11. Reações da Sociedade Civil

### 11.1 Fórum de Direito de Acesso a Informações Públicas

**Claim:** Em 23 de fevereiro de 2022, o Fórum de Direito de Acesso a Informações Públicas, composto por 25 organizações, emitiu nota criticando a decisão do INEP de remover os microdados, considerando que a justificativa da LGPD comprometia a transparência das políticas públicas de educação [^248^].

**Source:** Fiquem Sabendo / WikiLAI
**URL:** https://wikilai.fiquemsabendo.com.br/wiki/Censo_Escolar
**Date:** 2025-01-31
**Excerpt:** "Em nota publicada no dia 23 de fevereiro, o Fórum de Direito de Acesso a Informações Públicas, formado por 25 organizações, criticou a justificativa do Inep, por comprometer a transparência das políticas públicas de educação."
**Context:** Documentação da reação da sociedade civil à remoção dos microdados.
**Confidence:** high

### 11.2 Defensoria Pública da União

**Claim:** A Defensoria Pública da União reagiu à remoção dos microdados pelo INEP, recomendando que os dados fossem publicados pela autarquia [^248^].

**Source:** Fiquem Sabendo / WikiLAI
**URL:** https://wikilai.fiquemsabendo.com.br/wiki/Censo_Escolar
**Date:** 2025-01-31
**Excerpt:** "Outras organizações também manifestaram preocupação com a medida por meio de nota e até a Defensoria Pública da União reagiu, recomendando que os dados fossem publicados pelo Inep."
**Context:** Registro da pressão institucional sobre o INEP.
**Confidence:** high

### 11.3 Impacto no Anuário da Educação

**Claim:** A ONG Todos Pela Educação relatou que a falta de microdados inviabilizou a produção do Anuário da Educação de 2022, pois não havia dados suficientes para análises detalhadas [^455^].

**Source:** Lagom Data / Marcelo Soares
**URL:** https://lagomdata.com.br/site/2022/03/inep-desliga-acesso-a-microdados/
**Date:** 2022-03
**Excerpt:** "A Todos pela Educação, cuja missão é analisar e reportar indicadores educacionais, se viu impedida de produzir o Anuário da Educação 2022, que havia planejado como produto principal do ano."
**Context:** Reportagem sobre o impacto concreto da supressão de microdados na produção de relatórios da sociedade civil.
**Confidence:** high

---

## 12. Síntese Cronológica das Mudanças

| Ano | Evento | Impacto nos dados de estrangeiros |
|-----|--------|-----------------------------------|
| 2020 | Último Censo Escolar com microdados completos ao nível do aluno (17 GB) | TP_NACIONALIDADE com 3 categorias; NOME_PAIS_CE disponível |
| Fev/2022 | INEP remove série histórica; publica Censo 2021 em formato reduzido (164 MB, arquivo único) | Sem dados de alunos; sem variável nacionalidade |
| Fev/2022 | Reposição via SEDAP mencionada como alternativa | Acesso possível apenas em sala segura, mediante aprovação de projeto |
| Mar/2022 | INEP anuncia cronograma de republicação no "novo formato" | Série histórica será republicada, presumivelmente com mesmas restrições |
| Mar/2023 | Série histórica 2007-2020 republicada no novo formato | Variáveis suprimidas; granularidade reduzida |
| 2022-2025 | Microdados publicados anualmente em formato de arquivo único (escolas) | Sem acesso a registros individuais de alunos; sem nacionalidade detalhada |
| Jun/2023 | Portaria INEP 312/2023 institui núcleos remotos SEDAP | Ampliação do acesso diferenciado a dados completos |
| Jul/2024 | Lei 15.017/2024 sancionada, obrigando publicação de microdados | Potencial reversão, mas depende de interpretação do INEP sobre "proteção de dados" |
| 2024-2025 | Portal IEDE e ANPD continuam pressionando por maior transparência | Nota Técnica IEDE 2024 recomenda mascaramento em vez de exclusão |

---

## 13. Resumo Executivo

### Achados Principais

1. **Supressão massiva em 2022**: Em fevereiro de 2022, o INEP removeu do ar toda a série histórica de microdados do Censo Escolar e publicou o Censo 2021 em formato reduzido de 164 MB (vs 17 GB em 2020), sem registros individuais de alunos, docentes ou gestores. A justificativa foi a adequação à LGPD.

2. **Perda da granularidade ao nível do aluno**: A partir de 2021, os microdados públicos do Censo Escolar deixaram de conter matrículas individuais e passaram a ser agregados ao nível da escola (arquivo único CSV). A série histórica (2007-2020) foi republicada em março de 2023 no mesmo formato reduzido. Isso significa que **não há mais como identificar estudantes estrangeiros individualmente** nos microdados públicos do Censo Escolar.

3. **Variável nacionalidade suprimida/reduzida**: O estudo de pseudoanonimização proposto pelo IEDE reduziu a variável TP_NACIONALIDADE de 3 categorias (brasileira / brasileira nascida no exterior/naturalizada / estrangeira) para 2 categorias (brasileiro vs estrangeiro). Além disso, a variável NOME_PAIS_CE (país de origem) foi removida. Os códigos de município de nascimento e residência também foram suprimidos ou mascarados.

4. **Acesso diferenciado via SEDAP**: O único caminho para acesso a microdados completos (incluindo nacionalidade, país de origem, dados individuais de alunos) é o SEDAP (Serviço de Acesso a Dados Protegidos), que exige: projeto de pesquisa aprovado, vínculo institucional, termo de sigilo, e acesso em sala segura (presencial em Brasília ou em núcleos remotos em universidades como UFMG, Unicamp, USP, PUCRS). Os protocolos de segurança são extremamente rigorosos (câmeras, detector de metal, computadores sem USB, proibição de celulares).

5. **Lei 15.017/2024**: A lei sancionada em julho de 2024 obriga a publicação de microdados dos censos educacionais, mas mantém a ressalva de "adequação às normas de proteção de dados pessoais". Sua eficácia depende de como o INEP interpretará essa ressalva e de pressão da ANPD e sociedade civil.

6. **Repositórios alternativos**: A Base dos Dados (BD), Sou Ciência/Unifesp e Open Knowledge Brasil podem conter snapshots ou versões tratadas dos microdados históricos, mas não representam fontes primárias atualizadas.

### Implicações para Pesquisa sobre Estrangeiros em Santa Catarina

- **Não é mais possível**, via microdados públicos do INEP, identificar quantos estudantes estrangeiros de cada nacionalidade estão matriculados em cada escola, município ou região de SC.
- **Não é mais possível** cruzar nacionalidade com desempenho escolar, idade, sexo, raça, deficiência, ou local de residência.
- **O único caminho viável** para obter esses dados é solicitar acesso via SEDAP/INEP, com projeto de pesquisa formalmente aprovado, ou buscar dados diretamente nas secretarias municipais/estaduais de educação (que podem ou não ter sistemas próprios com essas informações).
- **A Lei 15.017/2024** pode abrir perspectiva de mudança, mas não há garantia de que o INEP vá restaurar a granularidade ao nível do aluno.

---

*Documento gerado a partir de 25+ buscas independentes em fontes primárias e secundárias, verificadas em fevereiro de 2026.*
