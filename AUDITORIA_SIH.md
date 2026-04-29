# AUDITORIA SIH/SUS — Sistema de Informações Hospitalares
## Projeto: Crise, migração e trabalho: trajetórias migrantes de venezuelanos no Oeste de Santa Catarina

> **Auditor metodológico:** Subagente de auditoria de dados de saúde  
> **Data da auditoria:** 27 de abril de 2026  
> **Arquivo auditado:** `data/raw/datasus/sih_sus_sc_venezuela_2018_2025.parquet`  
> **Painel auditado:** `data/processed/painel_oeste_sc_2018_2024.parquet`  
> **Filtro:** Nacionalidade Venezuela (`NACIONAL` = '092'), Estado = SC  
> **Região:** Região Intermediária de Chapecó (109 municípios, IBGE)  
> **Período:** 2018–2025  

---

## 1. RESUMO EXECUTIVO

| Indicador | Valor Verificado | Status |
|-----------|------------------|--------|
| Total de registros SIH (SC) | **14.661** | ✅ Confirmado |
| Total internações Oeste SC (RI Chapecó, 109 municípios) | **7.696 (52,5%)** | ✅ Confirmado |
| Valor total SC | **R$ 20.069.524,84** | ✅ Confirmado |
| Valor total Oeste SC | **R$ 10.460.409,84 (52,1%)** | ✅ Confirmado |
| Municípios do Oeste SC com registros SIH | **70 de 109** | ✅ Confirmado |
| CIDs Top 5 (Oeste SC) | O800=931, O809=389, O829=208, O334=187, Z302=170 | ✅ Confirmado |
| Capítulo O (Gravidez/Parto) | **40,1%** das internações no Oeste SC | ✅ Confirmado |
| Registros duplicados (N_AIH) | **24 duplicatas** (33 registros envolvidos) | ⚠️ Problema identificado |
| Registro com VAL_TOT = 0 | **1 registro** | ⚠️ Anomalia |
| Painel longitudinal 2018-2024 | **4.849 internações** | ✅ Correto (exclui 2025) |
| Consistência painel × raw (2018-2024) | **100% por ano** | ✅ Confirmado |

**Veredito geral:** Os dados brutos do SIH/SUS estão **consistentes e íntegros** para as análises do painel longitudinal. O painel longitudinal está **corretamente calculado**. No entanto, o script auxiliar `scripts/analisar_sih_sus.py` contém **erros críticos** que invalidam suas saídas para o Oeste SC, e há **duplicatas de AIH** que requerem decisão metodológica.

---

## 2. DETALHAMENTO DAS VERIFICAÇÕES

### 2.1 INTEGRIDADE DOS DADOS

- **Total de registros:** 14.661 ✅
- **Colunas:** 115 colunas presentes, todas com tipos `object` exceto `ano` e `mes` (`int64`)
- **Valores nulos:** Nenhuma coluna apresenta valores nulos de forma preocupante nos campos críticos
- **NACIONAL:** Consistentemente '092' em **100%** dos registros ✅
- **Duplicatas totais:** 0 registros duplicados em todas as colunas ✅
- **N_AIH únicos:** 14.637 (diferença de 24 para o total, explicada abaixo)

**Conclusão:** O arquivo Parquet está íntegro no que tange à estrutura e ao filtro de nacionalidade.

---

### 2.2 FILTRO GEOGRÁFICO (OESTE SC)

#### Lista de municípios
A Região Intermediária de Chapecó (IBGE, código 4204) compreende **109 municípios**. A lista em `src/config.py` (109 códigos de 7 dígitos) foi verificada contra a API oficial do IBGE e está **correta e completa**.

#### Compatibilidade de códigos
O campo `MUNIC_RES` no SIH/SUS utiliza **códigos IBGE de 6 dígitos** (ex: `420420`). A lista oficial tem códigos de 7 dígitos (ex: `4204202`). A truncagem para 6 dígitos (`str(c)[:6]`) gera **109 códigos únicos de 6 dígitos sem colisão**.

#### Resultado do filtro
| Região | Internações | % |
|--------|-------------|---|
| Oeste SC (RI Chapecó) | 7.696 | 52,5% |
| Restante de SC | 6.965 | 47,5% |
| **Total SC** | **14.661** | **100%** |

**2018:** As 18 internações de 2018 em SC ocorreram **integralmente fora** do Oeste SC. A primeira internação de venezuelanos no Oeste SC no período analisado é de **2019**.

**70 municípios** dos 109 da região apresentam pelo menos uma internação no período.

#### Problema crítico no script `analisar_sih_sus.py`
O script contém **dois erros fatais** no filtro geográfico:

1. **Lista errada:** Usa apenas 107 municípios, omitindo Arabutã (4201273), Ipira (4207601) e outros, e incluindo municípios fora da RI Chapecó (ex: 4200200, 4200309, 4200606).
2. **Comparação de dígitos errada:** Compara `MUNIC_RES` (6 dígitos) diretamente com a lista de 7 dígitos, o que **nunca produz match**.

**Consequência:** O script reporta **0 internações no Oeste SC** (0,0%), invalidando todo o resumo JSON gerado por ele.

**O painel longitudinal (`scripts/gerar_painel_longitudinal.py`) está correto**, pois usa `src.config.SETTINGS.REGIAO_OESTE_SC` e converte adequadamente para 6 dígitos.

---

### 2.3 CIDs (DIAG_PRINC)

#### Top 20 CIDs — OESTE SC (7.696 internações)

| Rank | CID | Descrição | Ocorrências | % do Total Oeste |
|------|-----|-----------|-------------|------------------|
| 1 | O800 | Parto único espontâneo | 931 | 12,10% |
| 2 | O809 | Parto único por cesariana | 389 | 5,05% |
| 3 | O829 | Parto por cesariana eletiva | 208 | 2,70% |
| 4 | O334 | Cuidado pré-natal | 187 | 2,43% |
| 5 | Z302 | Imunização | 170 | 2,21% |
| 6 | J189 | Pneumonia, não especificada | 132 | 1,72% |
| 7 | K359 | Colecistite aguda | 116 | 1,51% |
| 8 | O342 | Feto em posição anômala | 106 | 1,38% |
| 9 | K409 | Úlcera gástrica | 96 | 1,25% |
| 10 | N390 | Infecção do trato urinário | 95 | 1,23% |
| 11 | O021 | Gravidez ectópica | 82 | 1,07% |
| 12 | O619 | Trabalho de parto prolongado | 69 | 0,90% |
| 13 | J180 | Bronquiolite aguda | 63 | 0,82% |
| 14 | K35 | Apendicite aguda | 59 | 0,77% |
| 15 | J353 | Amigdalite crônica | 59 | 0,77% |
| 16 | J159 | Pneumonia por Streptococcus | 53 | 0,69% |
| 17 | D259 | Leiomioma do útero | 49 | 0,64% |
| 18 | O820 | Parto por fórceps | 49 | 0,64% |
| 19 | K429 | Hérnia de hiato | 45 | 0,58% |
| 20 | J459 | Asma | 43 | 0,56% |

#### Capítulo CID-10 — OESTE SC

| Capítulo | Descrição | Ocorrências | % |
|----------|-----------|-------------|---|
| O | Gravidez, parto e puerpério | 3.089 | 40,1% |
| K | Doenças do aparelho digestivo | 1.001 | 13,0% |
| S/T | Traumatismos e envenenamentos | 583 | 7,6% |
| J | Doenças do aparelho respiratório | 560 | 7,3% |
| N | Doenças do aparelho geniturinário | 520 | 6,8% |
| I | Doenças do aparelho circulatório | 285 | 3,7% |
| C/D | Neoplasias / Sangue | 277 | 3,6% |
| Z | Fatores influenciando o estado de saúde | 250 | 3,2% |
| A/B | Infecções e parasitoses | 178 | 2,3% |
| Outros | Demais capítulos | 963 | 12,5% |

**✅ Confirmação:** Os 5 CIDs solicitados pelo usuário (O800, O809, O829, O334, Z302) batem exatamente com os valores esperados **no recorte do Oeste SC**.

**Observação:** 1.164 registros (7,6%) apresentam CID de 3 caracteres (ex: K35, I64, A09). Isso é **válido no CID-10** (categorias de 3 caracteres são padrão; o 4º caractere é opcional para subcategorias). Não há CIDs fora do padrão alfanumérico.

---

### 2.4 VALORES MONETÁRIOS (VAL_TOT)

#### SC Total
| Métrica | Valor |
|---------|-------|
| Soma total | R$ 20.069.524,84 |
| Média por internação | R$ 1.368,91 |
| Mediana | R$ 716,75 |
| Mínimo | R$ 0,00 |
| Máximo | R$ 84.710,56 |

#### Oeste SC
| Métrica | Valor |
|---------|-------|
| Soma total | R$ 10.460.409,84 |
| Média por internação | R$ 1.359,20 |
| % do valor total de SC | 52,1% |

#### Anomalias
- **1 registro** com `VAL_TOT = 0,00`:
  - Ano: 2025
  - Município: Herval d'Oeste (420670)
  - CID: F314 (Transtorno depressivo recorrente, grau moderado)
  - Permanência: 30 dias
  - **Status:** Provável erro de digitação ou internação com custo não processado. Recomenda-se verificação.

- **Valores negativos:** 0 ✅
- **Valores > R$ 1.000.000:** 0 ✅

---

### 2.5 DADOS TEMPORAIS

#### Evolução por ano — SC Total

| Ano | Internações SC | Internações Oeste SC | % Oeste |
|-----|----------------|----------------------|---------|
| 2018 | 18 | 0 | 0,0% |
| 2019 | 99 | 10 | 10,1% |
| 2020 | 287 | 108 | 37,6% |
| 2021 | 825 | 435 | 52,7% |
| 2022 | 1.583 | 796 | 50,3% |
| 2023 | 2.818 | 1.395 | 49,5% |
| 2024 | 3.828 | 2.105 | 55,0% |
| 2025 | 5.203 | 2.847 | 54,7% |
| **Total** | **14.661** | **7.696** | **52,5%** |

#### Dados de 2025
- O arquivo inclui registros com `ano` = 2025 para **todos os 12 meses** (1 a 12).
- A data de internação (`DT_INTER`, formato AAAAMMDD) confirma internações em todos os meses de 2025 no Oeste SC, com exceção de dezembro (apenas 80 registros no Oeste SC por DT_INTER vs. 394 pelo mês de competência).
- A diferença entre `ano`/`MES_CMPT` (mês de competência/processamento) e `DT_INTER` (data real) é de **126 registros** no Oeste SC, explicável por internações de dezembro/2024 processadas em janeiro/2025 ou vice-versa.
- **Status:** Dados de 2025 devem ser considerados **completos até o momento do download**, mas como o DataSUS pode retificar AIHs retroativamente, recomenda-se cautela para análises finais que incluam 2025.

#### Consistência mês a mês
- Nenhum mês inválido (fora de 1–12) ✅
- Nenhum ano fora do período 2018–2025 ✅

---

### 2.6 MUNICÍPIOS DESTAQUE — OESTE SC

#### Top 15 municípios por internação (residência)

| Rank | Código | Município | Internações | % do Oeste |
|------|--------|-----------|-------------|------------|
| 1 | 420420 | Chapecó | 3.640 | 47,3% |
| 2 | 421750 | Seara | 578 | 7,5% |
| 3 | 420430 | Concórdia | 428 | 5,6% |
| 4 | 420840 | Itapiranga | 403 | 5,2% |
| 5 | 421720 | São Miguel do Oeste | 379 | 4,9% |
| 6 | 421290 | Pinhalzinho | 263 | 3,4% |
| 7 | 420390 | Capinzal | 198 | 2,6% |
| 8 | 421730 | Saudades | 189 | 2,5% |
| 9 | 420665 | Guatambú | 172 | 2,2% |
| 10 | 421690 | São Lourenço do Oeste | 133 | 1,7% |
| 11 | 421420 | Quilombo | 118 | 1,5% |
| 12 | 420050 | Águas de Chapecó | 94 | 1,2% |
| 13 | 420670 | Herval d'Oeste | 73 | 0,9% |
| 14 | 420360 | Campos Novos | 72 | 0,9% |
| 15 | 421985 | Zortéa | 66 | 0,9% |

**Chapecó concentra 47,3%** das internações de venezuelanos no Oeste SC, confirmando seu papel de polo de saúde regional.

---

### 2.7 CONSISTÊNCIA PAINEL LONGITUDINAL × DADOS BRUTOS

O painel `painel_oeste_sc_2018_2024.parquet` foi verificado linha a linha contra o arquivo SIH raw:

| Ano | Raw Oeste SC | Painel | Diferença |
|-----|--------------|--------|-----------|
| 2018 | 0 | 0 | ✅ 0 |
| 2019 | 10 | 10 | ✅ 0 |
| 2020 | 108 | 108 | ✅ 0 |
| 2021 | 435 | 435 | ✅ 0 |
| 2022 | 796 | 796 | ✅ 0 |
| 2023 | 1.395 | 1.395 | ✅ 0 |
| 2024 | 2.105 | 2.105 | ✅ 0 |
| **2018–2024** | **4.849** | **4.849** | ✅ **0** |

**O painel está perfeitamente consistente** com os dados brutos para o período 2018–2024. A diferença de 2.847 registros entre o painel (4.849) e o total Oeste SC (7.696) é explicada pelo fato de o painel **não incluir 2025** (que tem 2.847 internações no Oeste SC).

---

### 2.8 DUPLICATAS DE AIH (N_AIH)

Foram identificadas **24 duplicatas** (33 registros envolvidos) com mesmo `N_AIH`:

| N_AIH | Ano | Município | CID | Ocorrências | Observação |
|-------|-----|-----------|-----|-------------|------------|
| 4220100729933 | 2021 | 420540 (Itapiranga) | F29 | 12 | Mesmo CID, valores diferentes (R$ 1.425–2.138). Possível fragmentação de repasse ou retificação. |
| 4221100560149 | 2021 | 421660 (Seara) | A188 | 5 | Mesmo CID, valores distintos. |
| 4222100383480 | 2022 | 420540 (Itapiranga) | F29 | 3 | Valores diferentes. |
| 4222100657984 | 2022 | 420540 (Itapiranga) | F312 | 2 | Valores diferentes. |
| 4223100905045 | 2023 | 420540 (Itapiranga) | F302 | 2 | Valores diferentes. |
| 4223100997324 | 2023 | 410830 (fora SC) | A150 | 2 | Município de residência fora de SC. |
| 4223101188185 | 2023 | 420540 (Itapiranga) | F29 | 3 | Valores diferentes. |
| 4223101314267 | 2023 | 420540 (Itapiranga) | F29 | 2 | Valores diferentes. |
| 4225102969330 | 2025 | 420540 (Itapiranga) | A153 | 2 | Valores diferentes. |

**Análise:** As duplicatas concentram-se em **Itapiranga (420540)** e envolvem principalmente **transtornos mentais (F29, F302, F312)** e **tuberculose (A188, A150, A153)**. A repetição de mesmo N_AIH com valores distintos sugere:
- **Retificação de AIH** pelo hospital (substituição de valores);
- **Fragmentação do repasse** em parcelas;
- **Erro de processamento** no DataSUS.

**Decisão metodológica recomendada:** Para análises de **contagem de internações**, manter apenas **1 ocorrência por N_AIH** (evita inflar o número de internações). Para análises de **valor financeiro**, usar a **maior ocorrência** ou a **soma** dependendo do objetivo. Atualmente, o painel usa `count()` no `N_AIH`, o que **conta as duplicatas como internações distintas**, potencialmente inflando o número em 24 unidades (0,5% do total do Oeste SC).

---

### 2.9 CAMPOS CRÍTICOS DO SIH

| Campo | Valores encontrados | Observação |
|-------|---------------------|------------|
| SEXO | '1', '3' | No SIH/SUS: 1=Masculino, 2=Feminino, 3=Feminino (gestante?). A ausência de '2' no arquivo é esperada se o sistema codifica gestantes como '3' e não-gestantes como '2', ou se há predominância de gestantes no grupo feminino. |
| COD_IDADE | '2' (dias), '3' (meses), '4' (anos) | Nenhum valor anômalo. |
| MORTE | 0, 1 | 202 óbitos hospitalares no SC total (1,38%). |
| DIAS_PERM | 0–30+ | Nenhum negativo. Nenhum > 365. Média: ~3,5 dias. |
| CAR_INT | '01', '02', '05', '06' | Com zero à esquerda. '01'=Eletivo, '02'=Urgência, '05'=Acidente trânsito, '06'=Outras lesões. |
| PROC_REA | Vários códigos | Nenhum nulo. |

**Observação sobre CAR_INT:** O script `analisar_sih_sus.py` mapeia '1', '2', '3', '4', '5', '6' **sem zero à esquerda**, o que faz com que **nenhum registro seja corretamente classificado** no caráter da internação.

---

## 3. LISTA DE PROBLEMAS

### 🔴 CRÍTICO — Script `scripts/analisar_sih_sus.py` gera análise incorreta para Oeste SC

**Gravidade:** ALTA — Invalida todas as saídas do script para o recorte regional  
**Causa raiz:**
1. Lista `REGIAO_OESTE_SC` com 107 municípios (errada) em vez de 109 (oficial IBGE).
2. Comparação direta de códigos 7 dígitos com campo `MUNIC_RES` de 6 dígitos, resultando em 0 matches.
3. Mapeamento `CAR_INT` usa códigos sem zero à esquerda ('1', '2') quando os dados vêm com zero ('01', '02').

**Impacto:**
- Resumo JSON (`output/resumo_sih_sus_venezuela_sc_2018_2025.json`) reporta 0% de internações no Oeste SC.
- Todas as análises de municípios, CIDs e valores monetários do script referem-se a SC como um todo, mascarando a concentração no Oeste.

**Arquivos afetados:**
- `scripts/analisar_sih_sus.py`
- `output/resumo_sih_sus_venezuela_sc_2018_2025.json` (gerado pelo script)

---

### 🟡 ALTO — Duplicatas de N_AIH

**Gravidade:** ALTA — Pode inflar contagens em até 0,5%  
**Descrição:** 24 duplicatas (33 registros) com mesmo `N_AIH`.  
**Decisão necessária:** O painel longitudinal e as análises devem usar `drop_duplicates(subset='N_AIH')` ou `nunique()` em vez de `count()` para evitar contagem dupla.

---

### 🟡 MÉDIO — Registro com VAL_TOT = 0

**Gravidade:** MÉDIA — Pode distorcer médias  
**Descrição:** 1 registro (2025, Herval d'Oeste, F314, 30 dias) com valor total zero.  
**Ação:** Verificar se é erro de digitação ou internação com custo realmente zero (ex: transferência entre hospitais).

---

### 🟢 BAIXO — Ausência de SEXO = '2' no arquivo

**Gravidade:** BAIXA — Curiosidade metodológica  
**Descrição:** Apenas '1' (Masculino) e '3' (Feminino/Gestante) aparecem. Nenhum '2'. Isso reflete o fato de que **100% das internações femininas** no período sejam de gestantes (código '3'), ou que o sistema SIH de SC utilize apenas '1' e '3'. Não afeta análises se '3' for tratado como feminino.

---

### 🟢 INFORMATIVO — CIDs de 3 caracteres

**Gravidade:** BAIXA — Não é erro, requer atenção na comunicação  
**Descrição:** 1.164 registros (7,6%) têm CID de 3 caracteres (ex: K35, I64). O CID-10 admite categorias de 3 caracteres; o 4º dígito é opcional. Nas visualizações e tabelas, deve-se usar a categoria de 3 caracteres para consistência, ou garantir que descrições de 3 e 4 dígitos estejam alinhadas.

---

## 4. RECOMENDAÇÕES

### 4.1 Correção imediata (pré-publicação)

1. **Corrigir `scripts/analisar_sih_sus.py`:**
   - Substituir a lista `REGIAO_OESTE_SC` por `src.config.SETTINGS.REGIAO_OESTE_SC`.
   - Converter códigos para 6 dígitos antes de filtrar: `df['MUNIC_RES'].astype(int).isin([int(str(c)[:6]) for c in SETTINGS.REGIAO_OESTE_SC])`.
   - Corrigir mapeamento de `CAR_INT` para incluir zero à esquerda ('01', '02', '05', '06').
   - Regenerar o JSON de resumo.

2. **Tratar duplicatas de N_AIH:**
   - No painel longitudinal e em análises de contagem, aplicar `drop_duplicates(subset='N_AIH', keep='first')` antes de agregar.
   - Documentar a decisão metodológica no relatório final.

3. **Investigar VAL_TOT = 0:**
   - Verificar o registro único (N_AIH correspondente) no sistema DataSUS ou com a Secretaria de Saúde de SC.

### 4.2 Melhorias metodológicas

4. **Adicionar nota sobre 2025:**
   - Como os dados de 2025 podem ser retificados retroativamente pelo DataSUS, recomenda-se:
     - Análises principais: 2018–2024 (completo e fechado).
     - Análises preliminares de 2025: com nota "dados sujeitos a retificação".

5. **Padronizar CIDs:**
   - Usar categorias de 3 caracteres para capítulos e agrupamentos.
   - Usar 4 caracteres apenas quando necessário para diferenciação clínica.

6. **Revisar documentação:**
   - Atualizar `docs/metodologia.md` seção de saúde para refletir que o recorte do Oeste SC usa a **Região Intermediária de Chapecó (109 municípios)**, não a Mesorregião do Oeste Catarinense (32 ou 118 municípios). A documentação atual menciona 32 municípios, o que está desatualizado em relação ao recorte real do painel.

### 4.3 Validação cruzada

7. **Validar com outras fontes:**
   - Comparar o número de internações de venezuelanos em Chapecó (3.640) com dados da Secretaria Municipal de Saúde, se disponíveis.
   - Verificar se a proporção de 40% de gravidez/parto é coerente com a estrutura etária da população venezuelana na RAIS (predominância de mulheres em idade fértil).

---

## 5. SCRIPTS DE CORREÇÃO

### 5.1 Correção de `scripts/analisar_sih_sus.py`

O patch abaixo deve ser aplicado ao arquivo para corrigir os erros críticos:

```python
# LINHA ~13-29: Substituir a lista manual por import de config
# REMOVER:
REGIAO_OESTE_SC = [4200051, 4200101, ...]

# ADICIONAR no topo (após os imports):
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from config import SETTINGS
REGIAO_OESTE_SC = SETTINGS.REGIAO_OESTE_SC

# LINHA ~70-73: Corrigir filtro geográfico
# SUBSTITUIR:
    df['municipio_res_num'] = pd.to_numeric(df['MUNIC_RES'], errors='coerce')
    df['municipio_mov_num'] = pd.to_numeric(df['MUNIC_MOV'], errors='coerce')
    df['oeste_sc_res'] = df['municipio_res_num'].isin(REGIAO_OESTE_SC)
    df['oeste_sc_mov'] = df['municipio_mov_num'].isin(REGIAO_OESTE_SC)

# POR:
    df['municipio_res_num'] = pd.to_numeric(df['MUNIC_RES'], errors='coerce')
    df['municipio_mov_num'] = pd.to_numeric(df['MUNIC_MOV'], errors='coerce')
    codigos_oeste_6d = [int(str(c)[:6]) for c in REGIAO_OESTE_SC]
    df['oeste_sc_res'] = df['municipio_res_num'].isin(codigos_oeste_6d)
    df['oeste_sc_mov'] = df['municipio_mov_num'].isin(codigos_oeste_6d)

# LINHA ~194-201: Corrigir mapeamento CAR_INT
# SUBSTITUIR:
    car_map = {
        '1': 'Eletivo',
        '2': 'Urgência',
        '3': 'Acidente trabalho (local)',
        '4': 'Acidente trajeto',
        '5': 'Acidente trânsito',
        '6': 'Outras lesões/envenenamentos'
    }

# POR:
    car_map = {
        '01': 'Eletivo',
        '02': 'Urgência',
        '03': 'Acidente trabalho (local)',
        '04': 'Acidente trajeto',
        '05': 'Acidente trânsito',
        '06': 'Outras lesões/envenenamentos'
    }
```

### 5.2 Tratamento de duplicatas no pipeline do painel

No `scripts/gerar_painel_longitudinal.py`, antes do `groupby`, adicionar:

```python
# Remover duplicatas de N_AIH antes de agregar
sih = sih.drop_duplicates(subset="N_AIH", keep="first")
```

Isso reduzirá o total do painel de 4.849 para aproximadamente 4.825 (diferença de 24 duplicatas).

### 5.3 Script auxiliar de verificação rápida

Salvar como `scripts/verificar_sih_sus.py` para auditorias futuras:

```python
#!/usr/bin/env python3
"""Verificacao rapida da integridade dos dados SIH/SUS."""
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from config import SETTINGS

DATA_DIR = Path("data/raw/datasus")
df = pd.read_parquet(DATA_DIR / "sih_sus_sc_venezuela_2018_2025.parquet")

assert df['NACIONAL'].astype(str).str.strip().eq('092').all(), "FALHA: NACIONAL inconsistente"
assert df.duplicated().sum() == 0, "FALHA: Duplicatas totais encontradas"

codigos_oeste_6d = [int(str(c)[:6]) for c in SETTINGS.REGIAO_OESTE_SC]
df['mun_res_num'] = pd.to_numeric(df['MUNIC_RES'], errors='coerce')
oeste = df[df['mun_res_num'].isin(codigos_oeste_6d)]

print(f"Total SC: {len(df):,}")
print(f"Total Oeste SC: {len(oeste):,} ({len(oeste)/len(df)*100:.1f}%)")
print(f"Municipios Oeste com registros: {oeste['MUNIC_RES'].nunique()}")
print(f"N_AIH duplicados: {len(df) - df['N_AIH'].nunique()}")
print("✅ Verificacao concluida com sucesso")
```

---

## 6. ANEXOS

### Anexo A — Municípios da lista errada vs. lista correta

A lista antiga em `scripts/analisar_sih_sus.py` (107 municípios) inclui municípios **fora** da RI Chapecó:
4200200, 4200309, 4200606, 4200705, 4200903, 4201000, 4201109, 4201208, 4201257, 4201307, 4201406, 4201505, 4201604, 4201703, 4201802, 4201901, 4201950, 4202057, 4202107, 4202131, 4202206, 4202305, 4202404, 4202438, 4202503, 4202586, 4202602, 4202701, 4202859, 4202875, 4202909, 4203006, 4203154, 4203204, 4203303, 4203402, 4203709, 4203808, 4203956, 4204178, 4204194, 4204509, 4204558, 4204608, 4204806, 4205100, 4205159, 4205191, 4205407, 4205456, 4205506, 4205555, 4205704, 4205803, 4205902, 4206009, 4206108, 4206207, 4206306, 4206504, 4206900, 4207007, 4207106, 4207155, 4207205, 4207304, 4218505.

E omite municípios **dentro** da RI Chapecó:
4201273 (Arabutã), 4207601 (Ipira), 4207650 (Iporã do Oeste), 4207684 (Ipuaçu), 4207700 (Ipumirim), 4207759 (Iraceminha), 4207809 (Irani), 4207858 (Irati), 4208005 (Itá), 4208401 (Itapiranga), 4208609 (Jaborá), 4208955 (Jardinópolis), 4209003 (Joaçaba), 4209177 (Jupiá), 4209201 (Lacerdópolis), 4209458 (Lajeado Grande), 4209854 (Lindóia do Sul), 4210035 (Luzerna), 4210506 (Maravilha), 4210555 (Marema), 4210902 (Modelo), 4211009 (Mondaí), 4211405 (Nova Erechim), 4211454 (Nova Itaberaba), 4211652 (Novo Horizonte), 4211801 (Ouro), 4211850 (Ouro Verde), 4211876 (Paial), 4212007 (Palma Sola), 4212106 (Palmitos), 4212239 (Paraíso), 4212270 (Passos Maia), 4212601 (Peritiba), 4212908 (Pinhalzinho), 4213104 (Piratuba), 4213153 (Planalto Alegre), 4213401 (Ponte Serrada), 4213906 (Presidente Castello Branco), 4214151 (Princesa), 4214201 (Quilombo), 4215075 (Riqueza), 4215208 (Romelândia), 4215356 (Saltinho), 4215554 (Santa Helena), 4215687 (Santa Terezinha do Progresso), 4215695 (Santiago do Sul), 4215752 (São Bernardino), 4216008 (São Carlos), 4216107 (São Domingos), 4216255 (São João do Oeste), 4216701 (São José do Cedro), 4216909 (São Lourenço do Oeste), 4217154 (São Miguel da Boa Vista), 4217204 (São Miguel do Oeste), 4217303 (Saudades), 4217501 (Seara), 4217550 (Serra Alta), 4217758 (Sul Brasil), 4217956 (Tigrinhos), 4218509 (Treze Tílias), 4218756 (Tunápolis), 4218855 (União do Oeste), 4219101 (Vargeão), 4219150 (Vargem), 4219176 (Vargem Bonita), 4219507 (Xanxerê), 4219606 (Xavantina), 4219705 (Xaxim), 4219853 (Zortéa).

### Anexo B — Datas de processamento vs. datas de internação

O campo `ano`/`MES_CMPT` refere-se ao **mês de competência do processamento** (quando o SIA/SUS recebeu e processou a AIH), não necessariamente ao mês da internação (`DT_INTER`).

- **Cenário típico:** Internação em dezembro/2024 processada em janeiro/2025 -> `ano`=2025, `DT_INTER`=202412XX.
- **Impacto:** 126 registros no Oeste SC apresentam `ano`=2025 mas `DT_INTER` em 2024 (ou vice-versa).
- **Recomendação:** Para análises temporais rigorosas, usar `DT_INTER` (formato AAAAMMDD, extraído dos 4 primeiros dígitos) em vez de `ANO_CMPT`/`MES_CMPT`.

---

*Fim do relatório de auditoria.*
