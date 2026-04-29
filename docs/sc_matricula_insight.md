# Insight Extraction — Dados de Matrículas por Nacionalidade em Santa Catarina

## Data: 2025-04-29
## Baseado em: 12 dimensões de pesquisa + cross-verification

---

## Insight 1: Assimetria estrutural entre redes estadual e municipal

**Insight**: A SED-SC possui dados consolidados de matrículas de migrantes, mas a maior parte das matrículas (54% em 2023, ou 14.325 de 26.363) está na rede municipal — que NÃO é centralizada na SED-SC. Isso cria uma lacuna estrutural permanente: mesmo obtendo dados estaduais, o pesquisador ou gestor não terá visibilidade da maioria das matrículas sem solicitar dados individualmente a cada prefeitura.

**Derived From**:
- Dim02 (portais estaduais): SED-SC tem apenas 4 datasets no dados.sc.gov.br
- Dim04 (municipal): Chapecó tem 3.291 estrangeiros na municipal; outros municípios do Oeste têm dados fragmentados
- Dim06 (programas): PAM é exclusivo da rede estadual; rede municipal não tem programa equivalente centralizado
- Dim11 (integração): Não existe integração automatizada entre SISGESC e sistemas municipais

**Rationale**: A arquitetura de dados de SC reflete a organização federativa da educação: a SED controla a estadual, mas cada município controla sua rede. Como imigrantes se concentram em municípios específicos (Chapecó, Joinville, Florianópolis), a descentralização torna o mapeamento estadual incompleto.

**Implications**: Qualquer análise estadual que use apenas dados da SED-SC ou do INEP subnotificará a real presença de estrangeiros nas escolas, especialmente no Oeste onde a rede municipal é predominante.

**Confidence**: HIGH

---

## Insight 2: O paradoxo da transparência visual vs. tabular

**Insight**: Santa Catarina é o estado com maior infraestrutura de acolhimento ao migrante (PAM, diagnósticos anuais, painéis PowerBI, SIDEP) e, simultaneamente, um dos piores em publicação proativa de dados tabulares abertos. Os painéis visuais existem, mas não permitem download de microdados ou exportação CSV com variável de nacionalidade.

**Derived From**:
- Dim02 (portais): Educação na Palma da Mão tem painel PAM interativo, mas sem filtro/export por nacionalidade
- Dim03 (indicadores): QEdu, IDEB, TCE-SC — nenhum permite filtro por estrangeiros
- Dim06 (programas): Diagnósticos anuais do PAM são coletados, mas não publicados como documentos públicos
- Dim08 (LAI): Dados existem internamente, mas requerem pedido

**Rationale**: Há uma cultura de "transparência visual" (dashboards, BI, painéis) sem "transparência de dados" (datasets abertos, APIs, CSV). Isso atende ao gestor que precisa de uma foto rápida, mas não atende ao pesquisador, jornalista ou cidadão que precisa cruzar dados.

**Implications**: O estado gera dados de alto valor para políticas públicas, mas subutiliza seu potencial de accountability e pesquisa ao não publicar datasets estruturados.

**Confidence**: HIGH

---

## Insight 3: O INEP suprimiu dados individuais exatamente no período de pico migratório em SC

**Insight**: A mudança do INEP para microdados agregados por escola (2021+) coincidiu com o maior fluxo migratório internacional para SC. O estado recebeu 354 mil imigrantes (2017-2022), e o número de estrangeiros saltou de 11.671 (2010) para 72.793 (2022). O período de maior necessidade de dados desagregados para políticas de acolhimento foi exatamente quando os microdados individuais deixaram de ser públicos.

**Derived From**:
- Dim01 (INEP): Formato agregado a partir de 2021
- Dim07 (LGPD): Supressão de variáveis de nacionalidade/país de origem
- Dim10 (alternativas): Censo IBGE 2022 mostra crescimento de 523% de estrangeiros em SC
- Dim11 (integração): SC lidera saldo migratório no Brasil

**Rationale**: A justificativa do INEP foi a LGPD, mas o timing criou um "vale de dados" para pesquisadores e gestores de SC: não há como analisar, por exemplo, se alunos venezuelanos em Chapecó estão concentrados em determinadas séries ou escolas, porque os microdados pós-2021 não permitem essa desagregação.

**Implications**: Gestores municipais e estaduais de SC estão operando programas como o PAM sem acesso a dados de referência nacional atualizados sobre perfil etário, distribuição geográfica e progressão escolar dos migrantes.

**Confidence**: HIGH

---

## Insight 4: Matrícula garantida ≠ matrícula registrada digitalmente

**Insight**: As normativas federais (Resolução CNE 1/2020) e estaduais (Portaria 2083/2023) garantem matrícula sem documentação, criando uma lacuna estatística: alunos sem CRNM/RNE não podem ter seu número de registro migratório inserido nos sistemas escolares digitais (SED/SISGESC), especialmente na rede municipal. Isso significa que a "matrícula garantida por lei" não necessariamente se traduz em "matrícula contabilizada nos dados oficiais".

**Derived From**:
- Dim05 (legislação): Portaria 2083/2023 dispensa documentação; Resolução CNE 1/2020 garante matrícula sem documentos
- Dim02 (portais): SISGESC requer registro de RA; sem documento, escola deve solicitar inserção manual via Portal de Atendimento
- Dim04 (municipal): Chapecó tem processo de classificação manual para alunos sem documentação
- Dim06 (programas): PAM atende alunos que "muitas vezes vêm sem nenhum documento"

**Rationale**: Existe uma contradição entre o direito à educação (universal, sem documentos) e a arquitetura de dados (dependente de identificação digital). Alunos sem documentos são matriculados, mas o processo de inserção no sistema é manual, demorado e depende da diligência da escola/secretaria.

**Implications**: Os números oficiais de matrículas de estrangeiros (tanto do INEP quanto da SED-SC) são, na prática, **pisos mínimos**, não totais. A subnotificação é provável, especialmente para refugiados e imigrantes em situação irregular.

**Confidence**: HIGH

---

## Insight 5: Cruzamento de bases migratórias como "proxy viável" para demanda educacional

**Insight**: Embora não exista integração direta entre bases migratórias e educacionais, o cruzamento de três fontes públicas permite estimar demanda educacional por nacionalidade no Oeste de SC sem depender de dados escolares: (1) SISMIGRA (PF) mostra concentração municipal de imigrantes por país de origem e faixa etária; (2) CadÚnico identifica crianças estrangeiras em vulnerabilidade social com marcador de frequência escolar; (3) Censo IBGE 2022 mostra estrangeiros residentes por município. Nenhuma base isolada resolve, mas combinadas permitem modelagem preditiva.

**Derived From**:
- Dim10 (alternativas): SISMIGRA tem 153.459 registros em SC; CadÚnico tem 42.756 imigrantes; Censo IBGE tem 72.793 estrangeiros
- Dim11 (integração): Não existe integração direta entre bases, mas a Plataforma BoaVista (CIASC) consolida ~140 conjuntos de dados
- Dim03 (indicadores): QEdu usa combinação de Censo Escolar + DATASUS + Registro Civil para estimar atendimento na Educação Infantil

**Rationale**: O modelo do QEdu (combinar múltiplas bases para estimar indicadores) pode ser replicado para matrículas de estrangeiros, usando SISMIGRA + CadÚnico + Censo Demográfico como "triangulação de proxies".

**Implications**: Pesquisadores podem contornar a ausência de dados escolares desagregados usando modelagem estatística com bases administrativas alternativas, desde que transparente sobre limitações.

**Confidence**: MEDIUM

---

## Insight 6: Chapecó como "ilha de boa prática não replicável em dados abertos"

**Insight**: Chapecó desenvolveu a política municipal mais avançada de acolhimento educacional a migrantes no Oeste (Lei 7.729/2022, Resolução COMED 001/2021, CAI, projeto bilíngue, avaliação na língua materna). No entanto, nenhum desses dados é publicado em formato aberto. Outros municípios do Oeste (São Miguel do Oeste, Videira, Concórdia) têm projetos pontuais, mas sem sistematização. A "boa prática de acolhimento" não veio acompanhada de "boa prática de dados abertos".

**Derived From**:
- Dim04 (municipal): Chapecó tem 3.291 estrangeiros na municipal (2024), lei específica, CAI; outros municípios têm projetos isolados
- Dim06 (programas): Projeto municipal "Caminhos para uma Educação Equitativa" atende 3.604 estudantes, mas não publica relatórios anuais
- Dim08 (LAI): Nenhum portal municipal da região Oeste tem dataset educacional por nacionalidade

**Rationale**: Há um descompasso entre capacidade institucional de acolhimento (alta em Chapecó) e capacidade institucional de transparência (baixa em toda a região). Isso sugere que os dados existem nos sistemas internos da Seduc Chapecó, mas não há demanda institucional ou pressão social para publicação.

**Implications**: Pesquisadores ou gestores interessados no Oeste de SC devem focar em Chapecó como ponto de entrada, mas precisarão de solicitação direta (e-mail/LAI) à Seduc municipal, não apenas à SED estadual.

**Confidence**: HIGH

---

## Insight 7: O e-mail gaebe@sed.sc.gov.br como infraestrutura informal de dados — e seu risco de descontinuidade

**Insight**: Múltiplos artigos acadêmicos (2019-2025) obtiveram dados de matrículas de estrangeiros via o mesmo e-mail técnico (`gaebe@sed.sc.gov.br`). Isso revela uma "infraestrutura informal de dados" que funciona por boa vontade institucional, mas não é sustentável, transparente ou equitativa. Não há portaria, resolução ou termo de cooperação que garanta esse canal. Se o servidor mudar de função ou o e-mail for desativado, a porta de acesso se fecha.

**Derived From**:
- Dim02 (portais): GAEBE/SIAD é o setor de estatísticas da SED-SC
- Dim08 (LAI): Pesquisadores obtiveram dados sem necessidade de LAI formal
- Dim09 (acadêmico): 4+ publicações obtiveram dados via gaebe@sed.sc.gov.br

**Rationale**: A dependência de um único e-mail técnico para acesso a dados de interesse público é uma fragilidade institucional. A SED-SC não publicou nenhum "termo de solicitação de dados" ou "política de acesso a pesquisadores" que formalize esse canal.

**Implications**: Pesquisadores devem diversificar os canais de solicitação (LAI formal + e-mail técnico + contato com ouvidoria) para reduzir risco de não-resposta. A comunidade acadêmica tem interesse em pressionar pela formalização desse acesso.

**Confidence**: MEDIUM

---

## Insight 8: A Lei 15.017/2024 como janela de oportunidade — ainda não aproveitada

**Insight**: A Lei 15.017/2024 (sancionada em novembro/2024) obriga o INEP a divulgar microdados agregados e desagregados, anonimizados. A lei poderia forçar o retorno de dados individuais de alunos (incluindo nacionalidade/país de origem) em formato público. No entanto, até abril/2025, não houve mudança prática no formato dos microdados (2024-2025 continuam agregados por escola). Isso cria uma janela de oportunidade para advocacy e pedidos LAI baseados na nova lei.

**Derived From**:
- Dim01 (INEP): Lei 15.017/2024 mencionada como obrigação legal
- Dim07 (LGPD): INEP ainda mantém formato agregado apesar da lei
- Dim08 (LAI): Prazos e recursos da LAI podem ser usados para exigir cumprimento

**Rationale**: A Lei 15.017/2024 é uma ferramenta jurídica nova que pode ser invocada em pedidos LAI para questionar a não-divulgação de microdados desagregados. O INEP pode estar em processo de adequação, mas a pressão externa (pedidos, reportagens, notas técnicas) pode acelerar.

**Implications**: Pesquisadores e gestores de SC têm uma nova base legal para exigir dados do INEP. Um pedido LAI ao INEP citando especificamente a Lei 15.017/2024 e solicitando a variável de nacionalidade nos microdados poderia ser um precedente nacional.

**Confidence**: MEDIUM

---

## Summary of Insights

| # | Insight | Confidence | Key Dimensions |
|---|---------|------------|----------------|
| 1 | Assimetria estadual vs. municipal | HIGH | 02, 04, 06, 11 |
| 2 | Paradoxo transparência visual vs. tabular | HIGH | 02, 03, 06, 08 |
| 3 | INEP suprimiu dados no pico migratório | HIGH | 01, 07, 10, 11 |
| 4 | Matrícula garantida ≠ matrícula registrada | HIGH | 02, 04, 05, 06 |
| 5 | Cruzamento de bases como proxy | MEDIUM | 03, 10, 11 |
| 6 | Chapecó: boa prática não replicável em dados | HIGH | 04, 06, 08 |
| 7 | e-mail gaebe como infraestrutura informal | MEDIUM | 02, 08, 09 |
| 8 | Lei 15.017/2024 como janela de oportunidade | MEDIUM | 01, 07, 08 |
