# Cross-Verification — Dados de Matrículas por Nacionalidade em Santa Catarina

## Data da verificação: 2025-04-29
## Fontes: 12 dimensões investigadas em paralelo

---

## TIER 1: HIGH CONFIDENCE (Confirmado por ≥2 dimensões de fontes independentes)

### HC-01: Disponibilidade dos microdados INEP/Censo Escolar
- **Finding**: O INEP disponibiliza microdados do Censo Escolar para os anos 2005-2025 em formato ZIP para download direto.
- **Confirmed by**: Dim01, Dim07, Dim12
- **Sources**: Portal Gov.br INEP, UOL, Portal IEDE, Brazil Visible
- **Confidence**: HIGH

### HC-02: Mudança de formato dos microdados em 2021
- **Finding**: A partir de 2021, os microdados públicos do Censo Escolar deixaram de conter registros individuais de alunos e passaram a ser agregados ao nível da escola (~370 colunas com contagens agregadas como qt_mat_inf, qt_mat_fund, etc.).
- **Confirmed by**: Dim01, Dim07, Dim12
- **Sources**: UFPR Litoral, UFRGS dissertação, Scribd read-me INEP 2022
- **Confidence**: HIGH

### HC-03: Existência de variáveis de nacionalidade nos microdados até 2020
- **Finding**: Os microdados individuais até 2020 possuem as variáveis `TP_NACIONALIDADE` (1-Brasileira, 2-Brasileira nascido no exterior/naturalizado, 3-Estrangeira) e `NOME_PAIS_CE` (Nome do país de origem do aluno).
- **Confirmed by**: Dim01, Dim07, Dim12, Dim03
- **Sources**: Dicionário INEP/MJSP, UFPR dissertação, Portal de Imigração
- **Confidence**: HIGH

### HC-04: Supressão de variáveis por LGPD
- **Finding**: A LGPD causou supressão de dados pessoais nos microdados do Censo Escolar. O INEP removeu bases anteriores do site em fevereiro/2022 e republicou em formato reduzido. A variável nacionalidade foi potencialmente agregada de 3 para 2 categorias em algumas versões.
- **Confirmed by**: Dim01, Dim07, Dim09
- **Sources**: Portal IEDE, UOL, INEP nota oficial, Observatório de Educação/Unibanco
- **Confidence**: HIGH

### HC-05: SED-SC possui dados internos de matrículas por nacionalidade
- **Finding**: A Secretaria de Estado da Educação de Santa Catarina mantém internamente dados de matrículas de estudantes estrangeiros/migrantes (via SISGESC/SIDEP), mas não os publica como dados abertos.
- **Confirmed by**: Dim02, Dim04, Dim05, Dim06, Dim09, Dim11
- **Sources**: Artigos acadêmicos (Revista Aracê, Revista Pedagógica), notícias NSC Total, SED-SC portal
- **Confidence**: HIGH

### HC-06: Chapecó é polo de imigração no Oeste de SC
- **Finding**: Chapecó é o município da região Oeste com maior volume documentado de matrículas de estrangeiros (3.291 na rede municipal em 2024; 3.698 em todas as redes em 2023). É a 3ª cidade de SC com mais migrantes (80.973 segundo dados estaduais; 11.189 estrangeiros no Censo IBGE 2022).
- **Confirmed by**: Dim04, Dim06, Dim10, Dim11
- **Sources**: NSC Total, G1 Santa Catarina, Governo estadual (SC em Territórios), Prefeitura de Chapecó
- **Confidence**: HIGH

### HC-07: Programa PAM da SED-SC
- **Finding**: O Programa Estadual de Acolhimento ao Migrante (PAM, anteriormente PARE) é único no Brasil em rede estadual. Atende aproximadamente 1.300-1.500 estudantes migrantes em ~50-87 unidades escolares estaduais.
- **Confirmed by**: Dim02, Dim06, Dim09
- **Sources**: Revista Aracê, REASE, AJ Notícias, NSC Total, SED-SC
- **Confidence**: HIGH

### HC-08: Nenhum portal de indicadores público permite filtro por nacionalidade
- **Finding**: QEdu, IDEB, SAEB, TCE-SC/Lume, INEP painéis BI, dados.sc.gov.br — nenhum permite filtrar ou visualizar matrículas de estudantes estrangeiros por município ou escola.
- **Confirmed by**: Dim02, Dim03, Dim11
- **Sources**: QEdu.org.br, TCE-SC Lume, INEP Data, dados.sc.gov.br
- **Confidence**: HIGH

### HC-09: Pesquisadores obtêm dados da SED-SC via e-mail
- **Finding**: Múltiplos artigos acadêmicos obtiveram dados de matrículas de estrangeiros em SC via e-mail para `gaebe@sed.sc.gov.br` (Gerência de Avaliação e Estatísticas Educacionais) ou NIDEA/SIDEP.
- **Confirmed by**: Dim02, Dim06, Dim08, Dim09
- **Sources**: Revista Aracê 2025, Revista Pedagógica 2025, ESMPU apresentação 2019, UFFS dissertação
- **Confidence**: HIGH

### HC-10: Pedidos LAI são viáveis para obter dados não publicados
- **Finding**: A nacionalidade não é dado pessoal sensível segundo a LGPD. Dados agregados (contagens por município/escola/ano) não configuram sigilo art. 31 da LAI. Canais: ouvidoria.sc.gov.br (e-SIC), e-mails específicos (gaebe@sed.sc.gov.br, ouvidoria@sed.sc.gov.br).
- **Confirmed by**: Dim08, Dim05, Dim02
- **Sources**: CGE/SC, SED-SC Relatório Ouvidoria 2024, artigos acadêmicos
- **Confidence**: HIGH

### HC-11: SISMIGRA/PF disponibiliza microdados públicos de imigração
- **Finding**: O Portal de Imigração do MJSP disponibiliza microdados do SISMIGRA (2000-2024) com desagregação por município, sexo, país de nascimento, incluindo dados de SC. SC registrou 153.459 imigrantes internacionais até 2024.
- **Confirmed by**: Dim10, Dim11
- **Sources**: Portal de Imigração/MJSP, Revista Aracê, OBMigra
- **Confidence**: HIGH

---

## TIER 2: MEDIUM CONFIRMATION (Confirmado por 1 dimensão de fonte autoritativa)

### MC-01: Base dos Dados disponibiliza microdados 2009-2020 em BigQuery
- **Finding**: A Base dos Dados (basedosdados.org) possui tabela `br_inep_censo_escolar.matricula` com dados individuais 2009-2020 em BigQuery público (~90 GB). Não incluiu 2021+ devido à mudança de formato.
- **Source**: Dim01, Dim12
- **Confidence**: MEDIUM (Base dos Dados é fonte confiável, mas não foi verificado em tempo real durante a pesquisa)

### MC-02: educabR pacote R para download automático
- **Finding**: Pacote `educabR` no CRAN permite download automático de microdados 1995-2024 com filtro por UF (`uf="SC"`).
- **Source**: Dim12
- **Confidence**: MEDIUM (Documentação do CRAN verificada, mas não testado funcionalmente)

### MC-03: SEDAP permite acesso a microdados individuais 2021-2024
- **Finding**: O INEP disponibiliza, exclusivamente na Sala de Acesso a Dados Protegidos (SEDAP) em Brasília ou núcleos remotos, bases desidentificadas 2007-2024 mediante solicitação de pesquisador com autorização.
- **Source**: Dim01, Dim07
- **Confidence**: MEDIUM (Informação oficial do INEP, mas requer processo burocrático não testado)

### MC-04: Lei 15.017/2024 obriga divulgação de microdados
- **Finding**: Lei sancionada em 12/11/2024 obriga INEP a divulgar microdados agregados e desagregados anonimizados. Ainda não houve mudança prática no formato público (2024-2025 continuam agregados por escola).
- **Source**: Dim01, Dim07
- **Confidence**: MEDIUM (Lei publicada no DOU, mas eficácia depende de regulamentação/interpretação do INEP)

### MC-05: CadÚnico identifica crianças estrangeiras em vulnerabilidade social
- **Finding**: O CadÚnico possui variáveis sobre frequência escolar/creche e grupo etário. Em 2022 havia 42.756 imigrantes cadastrados no CadÚnico em SC.
- **Source**: Dim10
- **Confidence**: MEDIUM (Fonte OBMigra/IPARDES confiável, mas dados não foram verificados diretamente)

---

## TIER 3: LOW CONFIDENCE

### LC-01: Número exato de matrículas de migrantes em Chapecó em 2024
- **Finding**: 3.291 imigrantes matriculados nas escolas municipais de Chapecó (setembro/2024, NSC Total).
- **Concern**: Dado de notícia jornalística baseada em dados da Seduc Chapecó, mas não há documento oficial público com esse número. Pode haver variação dependendo da definição de "imigrante" usada.
- **Source**: Dim04
- **Confidence**: LOW

### LC-02: Mirror GCS com microdados em Parquet
- **Finding**: Existe mirror GCS `gs://microdados-inep/microdados-censo-escolar` com arquivos Parquet 2007-2019.
- **Concern**: Fonte não oficial; disponibilidade e atualidade não verificadas.
- **Source**: Dim01, Dim12
- **Confidence**: LOW

---

## TIER 4: CONFLICT ZONES

### CZ-01: Dados de matrículas de migrantes em Chapecó — variação de números
- **Conflict**: Dim04 relata 3.698 matrículas de estudantes migrantes em Chapecó em 2023 (todas as redes) vs. Dim06 relata 3.604 estudantes estrangeiros em 76 unidades municipais (rede municipal). Dim04 também cita 3.291 na rede municipal em 2024.
- **Analysis**: Não é uma contradição factual, mas variação temporal e definicional. Os números de 2023 (3.698 total; provavelmente ~3.000+ municipal) e 2024 (3.291 municipal) são consistentes com crescimento contínuo. A diferença entre 3.604 e 3.291 pode ser de ano (2023 vs 2024) ou de critério de contagem.
- **Resolution**: RESOLVED — variação temporal e de escopo (todas as redes vs. apenas municipal).
- **Sources**: Dim04, Dim06

### CZ-02: Número de unidades escolares no PAM
- **Conflict**: Dim02 cita ~50 unidades escolares do PAM em 2025. Dim06 cita 70 escolas em 2023 e 87 escolas em 2024. Dim09 cita ~50 unidades.
- **Analysis**: Os números de 2023 (70), 2024 (87) e 2025 (~50) parecem inconsistentes. Possíveis explicações: (a) o número de 2025 (~50) refere-se a unidades com atendimento ativo, enquanto 2023-2024 refere-se a unidades adesistas; (b) pode haver erro de transcrição nas fontes jornalísticas; (c) o programa pode ter sofrido redução em 2025.
- **Resolution**: PARTIALLY RESOLVED — provável variação de critérios de contagem (unidades ativas vs. unidades adesistas), mas não há fonte primária que esclareça.
- **Sources**: Dim02, Dim06, Dim09

### CZ-03: Série histórica do Censo Escolar — disponível ou não?
- **Conflict**: Dim01 afirma que todos os anos 2005-2025 estão disponíveis para download direto. Dim07 relata que o INEP removeu toda a série histórica em fevereiro/2022 e republicou em formato reduzido.
- **Analysis**: Não é uma contradição. A série histórica foi republicada em 08/03/2023 (Dim01), mas no "novo formato" reduzido (Dim07). Ou seja, os arquivos existem para download, mas não contêm os mesmos dados que continham antes de 2022.
- **Resolution**: RESOLVED — a série está disponível, mas em formato alterado/agregado.
- **Sources**: Dim01, Dim07

---

## Summary Statistics

| Tier | Count | Description |
|------|-------|-------------|
| High Confidence | 11 | Core findings robustly confirmed across multiple dimensions |
| Medium Confidence | 5 | Important findings from authoritative single sources |
| Low Confidence | 2 | Weakly sourced or unverified claims |
| Conflict Zones | 3 | All either resolved or partially resolved with explanation |

## Overall Assessment

A investigação convergiu fortemente em torno de **quatro conclusões centrais** com alto grau de confiança:

1. **Não existe portal público** (estadual, municipal ou federal) que permita baixar ou consultar diretamente dados de matrículas de estudantes estrangeiros por nacionalidade nas escolas públicas de SC.

2. **Os dados existem e são coletados** tanto pelo INEP (Censo Escolar, até 2020 com variável de nacionalidade) quanto pela SED-SC (SISGESC/SIDEP, com dados consolidados por nacionalidade até pelo menos 2023).

3. **O acesso é possível por três vias principais**: (a) download dos microdados INEP até 2020 + processamento próprio; (b) solicitação direta à SED-SC via e-mail (gaebe@sed.sc.gov.br); (c) pedido formal via LAI (ouvidoria.sc.gov.br).

4. **A região Oeste (especialmente Chapecó)** é a área do estado com maior concentração de dados documentados sobre matrículas de estrangeiros, embora sem datasets abertos nos portais municipais.
