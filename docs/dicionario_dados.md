# Dicionário de Dados

**Projeto:** `migracao-venezuelana-oeste-sc`  
**Autores:** Leonardo Rafael Santos Leitão e Vicente Neves da Silva Ribeiro (UFFS)  
**Data:** Abril de 2026

Este documento descreve as variáveis utilizadas no projeto, organizadas por fonte de dados. Para cada variável, indicamos: nome técnico, tipo de dado, descrição, fonte original, valores possíveis e sensibilidade (dados pessoais ou sensíveis, sujeitos a proteção legal).

---

## (a) Variáveis Demográficas — IBGE

| Nome | Tipo | Descrição | Fonte | Valores Possíveis | Sensível |
|:---|:---|:---|:---|:---|:---:|
| `V0001` | string(2) | Unidade da Federação (UF) | Censo IBGE / PNAD Contínua | Código IBGE da UF (ex.: "42" = SC) | Não |
| `V0002` | string(6) | Município de residência | Censo IBGE / PNAD Contínua | Código IBGE de 6 dígitos | Não |
| `V0601` | categorical | Sexo | Censo IBGE | 1=Homem, 2=Mulher | Não |
| `V6036` | int | Idade em anos completos | Censo IBGE | 0–120 | Não |
| `V6040` | categorical | Idade em meses (para < 1 ano) | Censo IBGE | 0–11 | Não |
| `V0606` | categorical | Cor ou raça | Censo IBGE | 1=Branca, 2=Preta, 3=Amarela, 4=Parda, 5=Indígena, 9=Ignorado | Não |
| `V0636` | categorical | Estado civil | Censo IBGE | 1=Solteiro(a), 2=Casado(a), 3=Separado(a), 4=Divorciado(a), 5=Viúvo(a) | Não |
| `V0628` | categorical | País de nascimento | Censo IBGE | Código do país (ex.: "0608" = Venezuela) | Não |
| `V0629` | categorical | Nacionalidade | Censo IBGE | 1=Brasileira, 2=Brasileira – nascido no exterior, 3=Estrangeira | Não |
| `V6400` | categorical | Escolaridade (grau) | Censo IBGE | 1=Sem instrução, 2=Fundamental incompleto, ..., 8=Pós-graduação | Não |
| `V6461` | categorical | Condição de atividade | PNAD Contínua | 1=Ocupado, 2=Desocupado, 3=Inativo | Não |
| `V1022` | categorical | Situação do domicílio | Censo IBGE | 1=Urbana, 2=Rural | Não |
| `V1005` | float | Peso amostral | Censo IBGE / PNAD Contínua | Peso expandido da amostra | Não |
| `renda_pc` | float | Renda per capita do domicílio | Censo IBGE (derivada) | Valor em reais (R$) | Não |
| `faixa_etaria` | categorical | Faixa etária quinquenal | Derivada | 0–4, 5–9, ..., 80+ | Não |

---

## (b) Variáveis DataSUS — SIM, SINASC, AIH, BPA

### Sistema de Informação sobre Mortalidade (SIM)

| Nome | Tipo | Descrição | Fonte | Valores Possíveis | Sensível |
|:---|:---|:---|:---|:---|:---:|
| `CAUSABAS` | string(4) | Causa básica do óbito (CID-10) | SIM | Código CID-10 (ex.: "J189" = Pneumonia) | Sim |
| `DTOBITO` | date | Data do óbito | SIM | AAAA-MM-DD | Sim |
| `DTNASC` | date | Data de nascimento do falecido | SIM | AAAA-MM-DD | Sim |
| `IDADE` | int | Idade do falecido (anos) | SIM | 0–120 | Sim |
| `SEXO` | categorical | Sexo do falecido | SIM | 1=Masculino, 2=Feminino, 0=Ignorado | Sim |
| `RACACOR` | categorical | Cor ou raça | SIM | 1=Branca, 2=Preta, 3=Amarela, 4=Parda, 5=Indígena | Sim |
| `CODMUNRES` | string(6) | Município de residência | SIM | Código IBGE | Sim |
| `LOCOCOR` | categorical | Local de ocorrência do óbito | SIM | 1=Hospital, 2=Outro estabelecimento, 3=Domicílio, 4=Via pública, 5=Outros | Sim |
| `TPMORTEOCO` | categorical | Tipo de morte (materna, fetal, etc.) | SIM | 1=Antes do parto, 2=Durante parto, 3=Após parto, 4=Ignorado | Sim |
| `ASSISTMED` | categorical | Assistência médica | SIM | 1=Sim, 2=Não, 9=Ignorado | Sim |
| `PAISRES` | string(3) | País de residência | SIM | Código do país (ex.: "0608" = Venezuela) | Sim |

### Sistema de Informação sobre Nascidos Vivos (SINASC)

| Nome | Tipo | Descrição | Fonte | Valores Possíveis | Sensível |
|:---|:---|:---|:---|:---|:---:|
| `DTNASC` | date | Data do nascimento | SINASC | AAAA-MM-DD | Sim |
| `SEXO` | categorical | Sexo do recém-nascido | SINASC | 1=Masculino, 2=Feminino | Sim |
| `RACACOR` | categorical | Cor ou raça do RN | SINASC | 1=Branca, 2=Preta, 3=Amarela, 4=Parda, 5=Indígena | Sim |
| `IDADEMAE` | int | Idade da mãe | SINASC | 10–55 | Sim |
| `ESCMAE` | categorical | Escolaridade da mãe | SINASC | 1=Nenhuma, 2=1–3 anos, ..., 5=12+ anos | Sim |
| `CODMUNRES` | string(6) | Município de residência da mãe | SINASC | Código IBGE | Sim |
| `QTDFILVIVO` | int | Quantidade de filhos vivos | SINASC | 0–20 | Sim |
| `QTDFILMORT` | int | Quantidade de filhos mortos | SINASC | 0–20 | Sim |
| `GESTACAO` | categorical | Semanas de gestação | SINASC | 1=<22 sem, 2=22–27, 3=28–31, 4=32–36, 5=37–41, 6=>42 | Sim |
| `GRAVIDEZ` | categorical | Tipo de gravidez | SINASC | 1=Única, 2=Dupla, 3=Tripla+ | Sim |
| `PARTO` | categorical | Tipo de parto | SINASC | 1=Vaginal, 2=Cesáreo | Sim |
| `CONSULTAS` | categorical | Número de consultas de pré-natal | SINASC | 1=Nenhuma, 2=1–3, 3=4–6, 4=7+, 9=Ignorado | Sim |
| `PAISNASC` | string(3) | País de nascimento da mãe | SINASC | Código do país | Sim |
| `PESO` | int | Peso ao nascer (gramas) | SINASC | 0–9999 | Sim |

### Sistema de Informações Hospitalares (SIH/AIH)

| Nome | Tipo | Descrição | Fonte | Valores Possíveis | Sensível |
|:---|:---|:---|:---|:---|:---:|
| `N_AIH` | string(13) | Número da AIH | SIH | Identificador único | Sim |
| `DT_INTER` | date | Data de internação | SIH | AAAA-MM-DD | Sim |
| `DT_SAIDA` | date | Data de alta | SIH | AAAA-MM-DD | Sim |
| `DIAG_PRINC` | string(4) | Diagnóstico principal (CID-10) | SIH | Código CID-10 | Sim |
| `DIAG_SECUN` | string(4) | Diagnóstico secundário | SIH | Código CID-10 | Sim |
| `PROC_REA` | string(10) | Procedimento realizado | SIH | Código SIGTAP | Sim |
| `VAL_SH` | float | Valor de serviços hospitalares (R$) | SIH | ≥ 0 | Sim |
| `VAL_SP` | float | Valor de serviços profissionais (R$) | SIH | ≥ 0 | Sim |
| `VAL_TOT` | float | Valor total da AIH (R$) | SIH | ≥ 0 | Sim |
| `MUNIC_RES` | string(6) | Município de residência | SIH | Código IBGE | Sim |
| `MUNIC_MOV` | string(6) | Município do estabelecimento | SIH | Código IBGE | Sim |
| `IDADE` | int | Idade do paciente | SIH | 0–120 | Sim |
| `SEXO` | categorical | Sexo | SIH | 1=Masculino, 3=Feminino | Sim |
| `DIAS_PERM` | int | Dias de permanência | SIH | 0–365 | Sim |
| `MARCA_UTI` | categorical | Marca de UTI | SIH | 0=Não utilizou, 1–7=Tipos de UTI | Sim |
| `CID_NOTI` | string(4) | CID de notificação (compulsória) | SIH | Código CID-10 | Sim |

### Boletim de Produção Ambulatorial (BPA)

| Nome | Tipo | Descrição | Fonte | Valores Possíveis | Sensível |
|:---|:---|:---|:---|:---|:---:|
| `PA_CMP` | string(6) | Competência (AAAAMM) | BPA | Ano e mês | Sim |
| `PA_CBOCOD` | string(6) | Código da ocupação do profissional | BPA | Código CBO 2002 | Não |
| `PA_PROC_ID` | string(10) | Procedimento realizado | BPA | Código SIGTAP | Não |
| `PA_QTDPRO` | int | Quantidade produzida | BPA | ≥ 1 | Não |
| `PA_SEXO` | categorical | Sexo do paciente | BPA | 1=M, 2=F | Sim |
| `PA_IDADE` | int | Idade do paciente | BPA | 0–120 | Sim |
| `PA_MUNPCN` | string(6) | Município de residência do paciente | BPA | Código IBGE | Sim |
| `PA_MVM` | string(6) | Mês de processamento | BPA | AAAAMM | Não |

---

## (c) Variáveis RAIS / CAGED

### RAIS — Relação Anual de Informações Sociais

| Nome | Tipo | Descrição | Fonte | Valores Possíveis | Sensível |
|:---|:---|:---|:---|:---|:---:|
| `id` | string(8) | Identificador único do vínculo | RAIS | Hash anonimizado | Sim |
| `pis` | string(11) | PIS/PASEP do trabalhador | RAIS | Número PIS (anonimizado) | Sim |
| `cpf` | string(11) | CPF do trabalhador | RAIS | Número CPF (anonimizado) | Sim |
| `nome` | string | Nome do trabalhador | RAIS | Texto (anonimizado) | Sim |
| `sexo` | categorical | Sexo | RAIS | 1=Masculino, 2=Feminino | Não |
| `idade` | int | Idade em 31/12 | RAIS | 10–80 | Não |
| `raca_cor` | categorical | Raça/cor | RAIS | 1=Indígena, 2=Branca, 4=Preta, 6=Amarela, 8=Parda, 9=Não ident. | Não |
| `grau_instrucao` | categorical | Grau de instrução | RAIS | 1=Analfabeto, ..., 9=Pós-graduação completa | Não |
| `cbo_ocupacao_2002` | string(6) | Código CBO 2002 | RAIS | Código CBO | Não |
| `cnae_2` | string(7) | Código CNAE 2.0 | RAIS | Código CNAE | Não |
| `cnae_2_classe` | string(5) | Classe CNAE | RAIS | Código de 5 dígitos | Não |
| `vinculo_ativo_31_12` | categorical | Vínculo ativo em 31/12 | RAIS | 0=Não, 1=Sim | Não |
| `vl_remun_dezembro_nom` | float | Remuneração dezembro (nominal) | RAIS | R$ | Não |
| `vl_remun_media_nom` | float | Remuneração média (nominal) | RAIS | R$ | Não |
| `tempo_emprego` | float | Tempo de emprego (meses) | RAIS | ≥ 0 | Não |
| `tipo_admissao` | categorical | Tipo de admissão | RAIS | 1=Primeiro emprego, ..., 6=Reintegração | Não |
| `tipo_vinculo` | categorical | Tipo de vínculo | RAIS | 10=CLT, 15=Diretor, ..., 90=Estagiário | Não |
| `municipio` | string(6) | Município do estabelecimento | RAIS | Código IBGE | Não |
| `ano` | int | Ano de referência | RAIS | 2018–2023 | Não |

### CAGED — Cadastro Geral de Empregados e Desempregados

| Nome | Tipo | Descrição | Fonte | Valores Possíveis | Sensível |
|:---|:---|:---|:---|:---|:---:|
| `competenciamov` | string(6) | Competência da movimentação | CAGED | AAAAMM | Não |
| `sigla_uf` | string(2) | UF do estabelecimento | CAGED | Sigla da UF | Não |
| `id_municipio` | string(6) | Município do trabalho | CAGED | Código IBGE | Não |
| `secao` | string(1) | Seção CNAE | CAGED | Letra (A–U) | Não |
| `subclasse` | string(7) | Subclasse CNAE | CAGED | Código CNAE | Não |
| `cbo2002ocupacao` | string(6) | CBO 2002 | CAGED | Código CBO | Não |
| `graudeinstrucao` | categorical | Grau de instrução | CAGED | 1=Analfabeto, ..., 8=Doutorado | Não |
| `idade` | int | Idade | CAGED | 14–100 | Não |
| `sexo` | categorical | Sexo | CAGED | 1=Masculino, 2=Feminino, 3=Não ident. | Não |
| `tipomovimentacao` | categorical | Tipo de movimentação | CAGED | 10=Admissão, 20=Desligamento, 25=Reclassificação, etc. | Não |
| `salario` | float | Salário (R$) | CAGED | ≥ 0 | Não |
| `saldomovimentacao` | int | Saldo (+1 admissão, -1 desligamento) | CAGED | -1, 0, +1 | Não |
| `categoria` | categorical | Categoria de trabalhador | CAGED | 101=Empregado, ..., 901=Trabalhador doméstico | Não |
| `horascontratuais` | float | Horas contratuais semanais | CAGED | 1–99 | Não |
| `tipodeficiencia` | categorical | Tipo de deficiência | CAGED | 0=Não, 1=Física, 2=Auditiva, ..., 9=Múltipla | Não |

---

## (d) Variáveis Educação

> **Nota:** As variáveis de educação dependem de acesso via LAI (Lei de Acesso à Informação) ou de bases públicas do QEdu / INEP. A tabela abaixo apresenta a estrutura esperada.

| Nome | Tipo | Descrição | Fonte | Valores Possíveis | Sensível |
|:---|:---|:---|:---|:---|:---:|
| `ano` | int | Ano de referência | SED/SC / INEP / Censo Escolar | 2018–2024 | Não |
| `cod_municipio` | string(6) | Município da escola | Censo Escolar / SED | Código IBGE | Não |
| `cod_escola` | string(8) | Código INEP da escola | Censo Escolar | Código INEP | Não |
| `etapa_ensino` | categorical | Etapa de ensino | Censo Escolar | 1=Pré-escola, 2=Fundamental, 3=Médio, 4=EJA, 5=Superior | Não |
| `modalidade` | categorical | Modalidade de ensino | Censo Escolar | 1=Regular, 2=Especial, 3=EJA, 4=Profissionalizante | Não |
| `sexo` | categorical | Sexo do estudante | Censo Escolar | 1=Masculino, 2=Feminino | Sim |
| `idade` | int | Idade do estudante | Censo Escolar | 0–100 | Sim |
| `cor_raca` | categorical | Cor ou raça | Censo Escolar | 0=Não declarada, 1=Branca, ..., 5=Indígena | Sim |
| `nacionalidade` | categorical | Nacionalidade | Censo Escolar | 1=Brasileira, 2=Naturalizado, 3=Estrangeira | Não |
| `pais_origem` | string(3) | País de origem | Censo Escolar | Código do país | Não |
| `deficiencia` | categorical | Possui alguma deficiência | Censo Escolar | 0=Não, 1=Sim | Sim |
| `transporte_publico` | categorical | Utiliza transporte público | Censo Escolar | 0=Não, 1=Sim | Não |
| `renda_familiar` | categorical | Faixa de renda familiar | Censo Escolar | 1=<½ SM, 2=½–1 SM, ..., 5=>3 SM | Sim |
| `matriculas` | int | Número de matrículas | Agregado SED / QEdu | ≥ 0 | Não |
| `concluintes` | int | Número de concluintes | Agregado SED / QEdu | ≥ 0 | Não |
| `abandono` | int | Número de evasões | Agregado SED / QEdu | ≥ 0 | Não |
| `taxa_rendimento` | float | Taxa de rendimento | Agregado SED / QEdu | 0–100 | Não |

---

## (e) Variáveis Assistência Social

> **Nota:** Dados do CadÚnico e de atendimentos em CRAS/CREAS dependem de acesso via LAI ou bases do MDS.

| Nome | Tipo | Descrição | Fonte | Valores Possíveis | Sensível |
|:---|:---|:---|:---|:---|:---:|
| `data_cadastro` | date | Data de cadastro no CadÚnico | CadÚnico / MDS | AAAA-MM-DD | Sim |
| `cod_municipio` | string(6) | Município de residência | CadÚnico | Código IBGE | Sim |
| `uf` | string(2) | UF de residência | CadÚnico | Sigla da UF | Sim |
| `qtd_pessoas` | int | Quantidade de pessoas na família | CadÚnico | 1–20 | Sim |
| `qtd_criancas` | int | Quantidade de crianças (< 14 anos) | CadÚnico | 0–15 | Sim |
| `renda_per_capita` | float | Renda per capita familiar (R$) | CadÚnico | ≥ 0 | Sim |
| `bolsa_familia` | categorical | Recebe Bolsa Família | CadÚnico | 0=Não, 1=Sim | Sim |
| `data_atualizacao` | date | Data da última atualização do cadastro | CadÚnico | AAAA-MM-DD | Sim |
| `tipo_logradouro` | string | Tipo de logradouro | CadÚnico | Texto | Sim |
| `nome_logradouro` | string | Nome do logradouro | CadÚnico | Texto | Sim |
| `numero` | string | Número do imóvel | CadÚnico | Texto | Sim |
| `pais_origem` | string(3) | País de origem da família | CadÚnico | Código do país | Sim |
| `cras_atendimento` | string(8) | Código do CRAS de referência | SAS/SC | Código do CRAS | Sim |
| `tipo_atendimento` | categorical | Tipo de atendimento | SAS/SC / CRAS | 1=PAIF, 2=SCFV, 3=Benefícios eventuais, etc. | Sim |
| `data_atendimento` | date | Data do atendimento | SAS/SC / CRAS | AAAA-MM-DD | Sim |

---

## Notas sobre Sensibilidade

- Variáveis marcadas como **Sim** em "Sensível" contêm dados pessoais ou sensíveis, conforme a LGPD (Lei nº 13.709/2018) e a Lei nº 12.527/2011 (LAI).
- Dados sensíveis **não serão publicados** em nível individual. Serão utilizados apenas para cálculos agregados e estatísticas descritivas.
- Para publicação em repositórios abertos (Zenodo, OSF), serão disponibilizadas apenas **tabelas agregadas** por município, ano e faixa etária, garantindo k-anonimato (k ≥ 5).
- Acesso a dados individuais sensíveis será restrito aos pesquisadores autorizados, em ambiente computacional seguro, com termo de responsabilidade.

---

*Última atualização: Abril de 2026. Para sugestões de novas variáveis ou correções, abra uma issue no repositório do projeto.*
