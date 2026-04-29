# Verificação de Campos de Nacionalidade nos Dados Brutos do SIM e SINASC

**Projeto:** `migracao-venezuelana-oeste-sc`  
**Data da verificação:** 27 de abril de 2026  
**Responsável:** Leonardo Rafael Santos Leitão (UFFS)  

---

## 1. Objetivo

Verificar se os microdados do SIM (mortalidade) e SINASC (nascidos vivos) processados para Santa Catarina (SC) contêm campos que permitam identificar a nacionalidade ou país de origem do falecido (SIM) ou da mãe (SINASC), com foco específico na possibilidade de filtrar indivíduos de nacionalidade venezuelana.

---

## 2. Metodologia da Verificação

- **Fonte dos dados:** arquivos Parquet em `data/raw/datasus/SIM/` (2018–2023) e `data/raw/datasus/SINASC/` (2018–2022), gerados via PySUS.
- **DBC bruto verificado:** `data/raw/datasus/DOSC2024.dbc` (SIM SC 2024) para comparar colunas disponíveis no formato nativo do DataSUS.
- **Pesquisa complementar:** dicionário de dados do IBGE/DATASUS para decodificação dos códigos de naturalidade de 3 dígitos.

---

## 3. Resultados — SIM (Mortalidade)

### 3.1 Colunas disponíveis

O arquivo `DO_SC_2023.parquet` possui **88 colunas**. A listagem completa é:

```
ORIGEM, TIPOBITO, DTOBITO, HORAOBITO, NATURAL, CODMUNNATU, DTNASC, IDADE,
SEXO, RACACOR, ESTCIV, ESC, ESC2010, SERIESCFAL, OCUP, CODMUNRES, LOCOCOR,
CODESTAB, ESTABDESCR, CODMUNOCOR, IDADEMAE, ESCMAE, ESCMAE2010, SERIESCMAE,
OCUPMAE, QTDFILVIVO, QTDFILMORT, GRAVIDEZ, SEMAGESTAC, GESTACAO, PARTO,
OBITOPARTO, PESO, TPMORTEOCO, OBITOGRAV, OBITOPUERP, ASSISTMED, EXAME,
CIRURGIA, NECROPSIA, LINHAA, LINHAB, LINHAC, LINHAD, LINHAII, CAUSABAS,
CB_PRE, COMUNSVOIM, DTATESTADO, CIRCOBITO, ACIDTRAB, FONTE, NUMEROLOTE,
TPPOS, DTINVESTIG, CAUSABAS_O, DTCADASTRO, ATESTANTE, STCODIFICA,
CODIFICADO, VERSAOSIST, VERSAOSCB, FONTEINV, DTRECEBIM, ATESTADO,
DTRECORIGA, CAUSAMAT, ESCMAEAGR1, ESCFALAGR1, STDOEPIDEM, STDONOVA,
DIFDATA, NUDIASOBCO, NUDIASOBIN, DTCADINV, TPOBITOCOR, DTCONINV, FONTES,
TPRESGINFO, TPNIVELINV, NUDIASINF, DTCADINF, MORTEPARTO, DTCONCASO,
FONTESINF, ALTCAUSA, CONTADOR, ano_sim
```

### 3.2 Campos relacionados a nacionalidade

Após busca por variações (`NACIONAL`, `NACIONALIDADE`, `PAIS`, `NATURAL`, `NASC`, `VEN`, `ESTRANG`), **não foi encontrado nenhum campo explícito de nacionalidade** nos arquivos Parquet processados.

O único campo relacionado à origem geográfica do falecido é:

| Campo | Descrição | Tipo |
|:---|:---|:---|
| `NATURAL` | Naturalidade do falecido (código de 3 dígitos) | string(3) |
| `CODMUNNATU` | Código do município de naturalidade | string(6) |

> **Nota:** O arquivo DBC bruto `DOSC2024.dbc` (SIM SC 2024) foi lido via R (`read.dbc`) e apresenta **exatamente as mesmas 86 colunas**, confirmando que o PySUS não removeu campos de nacionalidade — eles simplesmente **não constam na versão atual do SIM** disponibilizada pelo DataSUS para SC.

### 3.3 Decodificação do campo `NATURAL`

O campo `NATURAL` utiliza códigos de 3 dígitos do IBGE/DATASUS:

- **Códigos 001–499:** Países estrangeiros
- **Códigos 800–899:** Unidades da Federação brasileiras (ex.: 842 = SC, 841 = PR, 843 = RS)
- **800:** Ignorado / não informado

A distribuição de valores no SIM SC 2023 é:

| Código | Frequência | Provável origem |
|:---|---:|:---|
| 842 | 36.058 | Santa Catarina |
| 843 | 5.959 | Rio Grande do Sul |
| 841 | 2.811 | Paraná |
| 835 | 1.008 | Minas Gerais |
| *(vazio)* | 513 | Não informado |
| 831 | 318 | São Paulo |
| ... | ... | ... |
| **< 800 (estrangeiros)** | **404** | **Vários países** |

### 3.4 Registros estrangeiros no SIM

| Ano | Total de óbitos | Estrangeiros | % |
|---:|---:|---:|---:|
| 2018 | 41.268 | 298 | 0,722% |
| 2019 | 42.282 | 285 | 0,674% |
| 2020 | 46.444 | 315 | 0,678% |
| 2021 | 59.898 | 416 | 0,695% |
| 2022 | 51.317 | 386 | 0,752% |
| 2023 | 48.589 | 404 | 0,831% |

**Principais códigos estrangeiros observados** (top 5, 2018–2023):

| Código | Frequência média anual | País (segundo dicionário IBGE) |
|:---:|---:|:---|
| 016 | ~45 | Argentina |
| 109 | ~44 | Ilhas do Canal |
| 253 | ~34 | Hong Kong |
| 008 | ~28 | África do Sul?¹ |
| 190 | ~29 | *Não consta no dicionário oficial* |

¹ O código 008 não é explicitamente listado no dicionário de 3 dígitos consultado; pode ser um código legacy ou de território não listado.

### 3.5 Venezuela no SIM

**Código oficial da Venezuela no dicionário IBGE/DATASUS: `092`.**

Verificação em todos os anos disponíveis:

```python
SIM 2018: NAO TEM 092
SIM 2019: NAO TEM 092
SIM 2020: NAO TEM 092
SIM 2021: NAO TEM 092
SIM 2022: NAO TEM 092
SIM 2023: NAO TEM 092
SIM 2024: NAO TEM 092
```

**Conclusão SIM:** Não há registros de falecidos com naturalidade/nacionalidade venezuelana na base do SIM para SC no período 2018–2024.

---

## 4. Resultados — SINASC (Nascidos Vivos)

### 4.1 Colunas disponíveis

O arquivo `DN_SC_2022.parquet` possui **63 colunas**. A listagem completa é:

```
ORIGEM, CODESTAB, CODMUNNASC, LOCNASC, IDADEMAE, ESTCIVMAE, ESCMAE,
CODOCUPMAE, QTDFILVIVO, QTDFILMORT, CODMUNRES, GESTACAO, GRAVIDEZ,
PARTO, CONSULTAS, DTNASC, HORANASC, SEXO, APGAR1, APGAR5, RACACOR, PESO,
IDANOMAL, DTCADASTRO, CODANOMAL, NUMEROLOTE, VERSAOSIST, DTRECEBIM,
DIFDATA, DTRECORIGA, NATURALMAE, CODMUNNATU, CODUFNATU, ESCMAE2010,
SERIESCMAE, DTNASCMAE, RACACORMAE, QTDGESTANT, QTDPARTNOR, QTDPARTCES,
IDADEPAI, DTULTMENST, SEMAGESTAC, TPMETESTIM, CONSPRENAT, MESPRENAT,
TPAPRESENT, STTRABPART, STCESPARTO, TPNASCASSI, TPFUNCRESP, TPDOCRESP,
DTDECLARAC, ESCMAEAGR1, STDNEPIDEM, STDNNOVA, CODPAISRES, TPROBSON,
PARIDADE, KOTELCHUCK, CONTADOR, ano_sinasc
```

### 4.2 Campos relacionados a nacionalidade

Após busca por variações, os seguintes campos foram identificados como potencialmente relacionados à nacionalidade da mãe:

| Campo | Descrição | Observação |
|:---|:---|:---|
| `NATURALMAE` | Naturalidade da mãe (código de 3 dígitos) | Mesma codificação do SIM |
| `CODMUNNATU` | Código do município de naturalidade da mãe | — |
| `CODUFNATU` | Código da UF de naturalidade da mãe | — |
| `CODPAISRES` | Código do país de residência | **Apenas valor `'1  '` (Brasil)** em 100% dos registros |

> **Ausências notáveis:** Não há campo `NACIONALIDADE_MAE`, `PAISNASC`, `PAIS_MAE` ou similar nos arquivos processados.

### 4.3 Decodificação do campo `NATURALMAE`

A distribuição em 2022:

| Código | Frequência | Provável origem |
|:---|---:|:---|
| 842 | 65.229 | Santa Catarina |
| 841 | 8.997 | Paraná |
| 843 | 7.594 | Rio Grande do Sul |
| 835 | 3.009 | Minas Gerais |
| *(vazio)* | 2.754 | Não informado |
| ... | ... | ... |
| **< 800 (estrangeiros)** | **3** | **2×109, 1×58** |

### 4.4 Registros estrangeiros no SINASC

| Ano | Total de nascimentos | Estrangeiros | % |
|---:|---:|---:|---:|
| 2018 | 99.609 | 0 | 0,0000% |
| 2019 | 98.032 | 0 | 0,0000% |
| 2020 | 97.916 | 0 | 0,0000% |
| 2021 | 96.499 | 0 | 0,0000% |
| 2022 | 98.202 | 3 | 0,0031% |

Os únicos 3 registros estrangeiros em 2022 usam os códigos `109` (Ilhas do Canal) e `58` (Malvinas/Falklands).

### 4.5 Venezuela no SINASC

**Código oficial da Venezuela: `092`.**

Verificação em todos os anos disponíveis:

```python
SINASC 2018: NAO TEM 092
SINASC 2019: NAO TEM 092
SINASC 2020: NAO TEM 092
SINASC 2021: NAO TEM 092
SINASC 2022: NAO TEM 092
```

**Conclusão SINASC:** Não há registros de mães com naturalidade/nacionalidade venezuelana na base do SINASC para SC no período 2018–2022.

---

## 5. Discussão e Limitações

### 5.1 Ausência do campo explícito de nacionalidade

Embora o dicionário de dados do projeto (`docs/dicionario_dados.md`) mencione campos como `PAISRES` (SIM) e `PAISNASC` (SINASC), **esses campos não estão presentes nos microdados reais** processados via PySUS para o estado de Santa Catarina. Isso pode ocorrer porque:

1. O DataSUS removeu ou não coleta esses campos em versões mais recentes do SIM/SINASC para SC;
2. O PySUS pode não expor esses campos na conversão DBC → DataFrame (embora a verificação no DBC bruto indique que eles realmente não existem);
3. O dicionário de dados do projeto pode estar referenciando uma versão antiga ou outra base (ex.: SIH, que possui `NACIONAL`).

### 5.2 Campo `NATURAL` / `NATURALMAE` como proxy

O campo de naturalidade pode ser usado como **proxy indireta** para identificar estrangeiros, com as seguintes ressalvas:

- **Subnotificação:** imigrantes podem ter sido registrados com naturalidade brasileira (ex.: SC = 842) se o preenchimento foi incorreto ou baseado na nacionalidade adquirida;
- **Codificação inconsistente:** o código `190` aparece com frequência no SIM mas não consta no dicionário oficial IBGE de 3 dígitos, indicando possíveis erros de digitação ou uso de tabela alternativa;
- **Não identifica venezuelanos:** como demonstrado, o código `092` (Venezuela) não aparece em nenhum registro do SIM ou SINASC para SC no período analisado.

### 5.3 Campo `CODPAISRES` no SINASC

O campo `CODPAISRES` é teoricamente o campo de país de residência, mas em todos os registros analisados (2018–2022) ele contém exclusivamente o valor `'1  '`, que corresponde ao Brasil. Isso o torna inútil para identificar mães estrangeiras, incluindo venezuelanas.

---

## 6. Conclusão

| Questão | Resposta |
|:---|:---|
| Há campo de nacionalidade no SIM? | **Não.** Apenas `NATURAL` (naturalidade, 3 dígitos). |
| Há campo de nacionalidade no SINASC? | **Não.** Apenas `NATURALMAE` e `CODPAISRES` (sempre = Brasil). |
| É possível filtrar venezuelanos no SIM? | **Não.** O código `092` (Venezuela) não aparece em 2018–2024. |
| É possível filtrar venezuelanos no SINASC? | **Não.** O código `092` não aparece em 2018–2022. |
| Qual a melhor alternativa? | Usar `NATURAL`/`NATURALMAE` como proxy para estrangeiros, aceitando que venezuelanos estarão sub-representados ou invisíveis. |

### Recomendações para o projeto

1. **Não utilizar SIM/SINASC como fonte primária** para quantificar óbitos ou nascimentos de venezuelanos em SC no período 2018–2023.
2. **Priorizar o SIH (AIH)** para análise de saúde da população venezuelana, pois essa base possui o campo `NACIONAL` (código de 2/3 dígitos) que permite identificar estrangeiros — já demonstrado no projeto com os arquivos `sih_sus_sc_venezuela_*.parquet`.
3. **Se necessário incluir SIM/SINASC**, considerar apenas análise agregada de "estrangeiros" via `NATURAL` < 800, sem desagregação por país, e discutir explicitamente a limitação de subnotificação no relatório metodológico.

---

## 7. Referências

- DataSUS / MS. *Dicionário de dados do SIM (CID-10)*. Disponível em: ftp://ftp.datasus.gov.br/dissemin/publicos/SIM/CID10/
- DataSUS / MS. *Dicionário de dados do SINASC*. Disponível em: ftp://ftp.datasus.gov.br/dissemin/publicos/SINASC/
- IBGE. *Tabela de códigos de naturalidade (3 dígitos)*. Utilizada nos sistemas DataSUS.
- Documento interno do projeto: `docs/dicionario_dados.md`.
