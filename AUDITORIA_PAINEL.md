# Auditoria do Painel Longitudinal Oeste SC 2018-2024

**Data da auditoria:** 2026-04-27
**Arquivo auditado:** `data/processed/painel_oeste_sc_2018_2024.parquet`
**Arquivo corrigido:** `data/processed/painel_oeste_sc_2018_2024_corrigido.parquet`
**Script gerador corrigido:** `scripts/gerar_painel_longitudinal.py`

---

## Resumo Executivo

- **Painel:** 763 linhas, 109 municípios, anos 2018-2024
- **Problemas encontrados:** 1
- **Correções aplicadas:** SIM
- **Status pós-correção:** ✅ APROVADO

### Problema Identificado e Corrigido

1. **SINASC 2023 preenchido com 0.0 em vez de NaN**
   - A fonte SINASC só possui dados até 2022 (545 registros = 109 municípios × 5 anos).
   - O painel original preencheu `total_nascimentos=0.0` e `taxa_natalidade=0.0` para todos os 109 municípios em 2023.
   - **Correção aplicada:** Substituídos por `NaN` no arquivo corrigido, consistente com o tratamento de 2024.
   - **Script gerador corrigido:** Adicionada etapa explícita para garantir `NaN` em anos sem dados SINASC (≥2023) e SIM (≥2024).

---

# 1. ESTRUTURA E COMPLETUDE

## 1.1 Dimensões

| Métrica | Valor | Esperado | Status |
|---------|-------|----------|--------|
| Total de linhas | 763 | 763 | ✅ |
| Municípios únicos (7d) | 109 | 109 | ✅ |
| Municípios únicos (6d) | 109 | 109 | ✅ |
| Anos | 2018-2024 | 2018-2024 | ✅ |
| Duplicatas (município, ano) | 0 | 0 | ✅ |
| Municípios por ano | 109 em cada ano | 109 | ✅ |

## 1.2 Colunas

**Colunas presentes (16):**
```
codigo_ibge_7d, codigo_ibge_6d, municipio, ano, populacao_total,
total_vinculos_rais, taxa_vinculos_por_mil,
total_internacoes_sih, dias_permanencia_sih, valor_total_sih, obitos_hospitalares_sih, taxa_internacoes_por_mil,
total_obitos, total_nascimentos, taxa_mortalidade, taxa_natalidade
```

- **Colunas faltantes:** nenhuma ✅
- **Colunas extras:** nenhuma ✅

## 1.3 Valores Nulos (NaN)

| Coluna | NaNs (original) | NaNs (corrigido) | Justificativa |
|--------|-----------------|------------------|---------------|
| total_obitos | 109 | 109 | SIM sem dados para 2024 |
| total_nascimentos | 109 | 218 | SINASC sem dados para 2023-2024 |
| taxa_mortalidade | 109 | 109 | Derivado de total_obitos |
| taxa_natalidade | 109 | 218 | Derivado de total_nascimentos |

**Verificação estrutural pós-correção:**
- 2024: obitos=NaN ✅, nascimentos=NaN ✅
- 2023: nascimentos=NaN ✅ (corrigido de 0.0)

---

# 2. CONSISTÊNCIA COM DADOS FONTES

## 2.1 RAIS → painel ✅

| Ano | Painel | Bruto (filtrado Oeste SC) | Divergências |
|-----|--------|---------------------------|--------------|
| 2018 | 66 | 66 | 0 ✅ |
| 2019 | 1.095 | 1.095 | 0 ✅ |
| 2020 | 3.990 | 3.990 | 0 ✅ |
| 2021 | 10.365 | 10.365 | 0 ✅ |
| 2022 | 18.577 | 18.577 | 0 ✅ |
| 2023 | 28.959 | 28.959 | 0 ✅ |
| 2024 | 40.420 | 40.420 | 0 ✅ |

**Nota:** Os dados brutos RAIS (`rais_vinculos_sc_venezuela_YYYY.parquet`) cobrem TODO o estado de SC. Após filtrar para os 109 municípios do Oeste, os totais batem perfeitamente com o painel.

## 2.2 SIH/SUS → painel ✅

- **SIH total (2018-2025):** 14.661 registros
- **SIH filtrado Oeste SC:** 7.696 registros (70 municípios com internações)
- **39 municípios** dos 109 não possuem nenhum registro SIH (municípios pequenos sem internações de venezuelanos)

| Ano | total_internacoes | dias_permanencia | valor_total | obitos_hospitalares | Divergências |
|-----|-------------------|------------------|-------------|---------------------|--------------|
| 2018 | 0 | 0 | 0 | 0 | 0 ✅ |
| 2019 | 10 | 61 | 8.541 | 0 | 0 ✅ |
| 2020 | 108 | 333 | 173.376 | 1 | 0 ✅ |
| 2021 | 435 | 1.572 | 824.935 | 11 | 0 ✅ |
| 2022 | 796 | 2.616 | 940.206 | 13 | 0 ✅ |
| 2023 | 1.395 | 4.065 | 1.435.972 | 18 | 0 ✅ |
| 2024 | 2.105 | 6.154 | 2.949.224 | 34 | 0 ✅ |

## 2.3 População IBGE → painel ✅

- **Fonte:** `data/processed/ibge_populacao_estimada_oeste_sc.parquet` (763 registros)
- **Divergências:** 0 ✅
- **Anos cobertos:** 2018-2024

## 2.4 SIM → painel ✅

- **Fonte:** `data/processed/datasus_sim_oeste_sc.parquet` (654 registros = 109 × 6 anos)
- **Anos:** 2018-2023
- **Divergências:** 0 ✅
- **2024:** corretamente como NaN (sem dados)

## 2.5 SINASC → painel ✅ (após correção)

- **Fonte:** `data/processed/datasus_sinasc_oeste_sc.parquet` (545 registros = 109 × 5 anos)
- **Anos:** 2018-2022
- **Divergências (dados existentes):** 0 ✅
- **2023-2024:** corretamente como NaN no arquivo corrigido ✅

---

# 3. CÁLCULOS DERIVADOS

## 3.1 Fórmulas verificadas

| Taxa | Fórmula | Divergências | Status |
|------|---------|--------------|--------|
| taxa_vinculos_por_mil | (total_vinculos_rais / populacao_total) × 1000 | 0 | ✅ |
| taxa_internacoes_por_mil | (total_internacoes_sih / populacao_total) × 1000 | 0 | ✅ |
| taxa_mortalidade | (total_obitos / populacao_total) × 1000 | 0 (654 válidos) | ✅ |
| taxa_natalidade | (total_nascimentos / populacao_total) × 1000 | 0 (545 válidos) | ✅ |

---

# 4. ANOMALIAS

| Tipo de anomalia | Quantidade | Limite | Status |
|------------------|------------|--------|--------|
| taxa_vinculos_por_mil > 500 | 0 | 500 | ✅ |
| taxa_internacoes_por_mil > 50 | 0 | 50 | ✅ |
| populacao_total = 0 | 0 | - | ✅ |
| Valores negativos | 0 (em todas as colunas) | - | ✅ |

---

# 5. COMPARABILIDADE TEMPORAL

## 5.1 Quebra de série populacional 2021→2022

A população de 2021 é estimativa intercensitária e a de 2022 é do Censo 2022. Isso cria quebra de série.

### Municípios com salto populacional > 50%

| Código IBGE (7d) | Município | Pop 2021 | Pop 2022 | Variação (%) |
|------------------|-----------|----------|----------|--------------|
| 4206652 | Guatambú | 4.692 | 8.425 | +79,6% |
| 4213104 | Piratuba | 3.637 | 5.769 | +58,6% |

### Municípios com salto populacional 30-50%

| Código IBGE (7d) | Município | Pop 2021 | Pop 2022 | Variação (%) |
|------------------|-----------|----------|----------|--------------|
| 4217956 | Tigrinhos | 1.606 | 2.329 | +45,0% |
| 4215695 | Santiago do Sul | 1.211 | 1.651 | +36,3% |
| 4211876 | Paial | 1.444 | 1.927 | +33,4% |
| 4204103 | Caxambu do Sul | 3.462 | 4.614 | +33,3% |
| 4212239 | Paraíso | 3.284 | 4.267 | +29,9% |

### Municípios com população que dobrou

Nenhum município teve população que dobrou de 2021 para 2022. ✅

### Impacto nas taxas

ℹ️ **AVISO:** Municípios com grande salto populacional terão taxas artificialmente reduzidas em 2022. Recomenda-se cautela na interpretação de taxas para esses municípios no ano de 2022, especialmente Guatambú e Piratuba.

---

# 6. CORREÇÃO APLICADA

## 6.1 Problema

O painel original possuía `total_nascimentos=0.0` e `taxa_natalidade=0.0` para todos os 109 municípios em 2023, quando deveriam ser `NaN` (a fonte SINASC só possui dados até 2022).

## 6.2 Script de correção

```python
import pandas as pd
import numpy as np

df = pd.read_parquet("data/processed/painel_oeste_sc_2018_2024.parquet")

# SINASC só tem dados até 2022. 2023 estava como 0.0, deve ser NaN.
mask_2023 = df['ano'] == 2023
df.loc[mask_2023, 'total_nascimentos'] = np.nan
df.loc[mask_2023, 'taxa_natalidade'] = np.nan

df.to_parquet("data/processed/painel_oeste_sc_2018_2024_corrigido.parquet", index=False)
```

## 6.3 Correção no script gerador

O script `scripts/gerar_painel_longitudinal.py` foi modificado para incluir uma etapa explícita de garantia de `NaN` para anos sem dados:

```python
# SINASC só tem dados até 2022; SIM só tem dados até 2023
painel.loc[painel["ano"] >= 2023, "total_nascimentos"] = pd.NA
painel.loc[painel["ano"] >= 2023, "taxa_natalidade"] = pd.NA
painel.loc[painel["ano"] >= 2024, "total_obitos"] = pd.NA
painel.loc[painel["ano"] >= 2024, "taxa_mortalidade"] = pd.NA
```

## 6.4 Alterações no arquivo corrigido

| Variável | Ano | Valor original | Valor corrigido |
|----------|-----|----------------|-----------------|
| total_nascimentos | 2023 | 0.0 | NaN |
| taxa_natalidade | 2023 | 0.0 | NaN |

**Registros afetados:** 109 (todos os municípios em 2023)

---

# 7. RECOMENDAÇÕES

1. **Usar o arquivo corrigido:** `data/processed/painel_oeste_sc_2018_2024_corrigido.parquet` em todas as análises subsequentes.

2. **Cautela com quebra de série populacional:** As taxas de 2022 (e subsequentes, por extrapolação) podem ser distorcidas para municípios com grande salto populacional entre 2021→2022. Considerar análises em números absolutos ou deflacionar pela população usando métodos de suavização.

3. **Documentar missing data:** Sempre que apresentar taxas de natalidade, explicitar que 2023-2024 não possuem dados SINASC e portanto estão como NaN (não como zero).

4. **Verificar análises já produzidas:** Se figuras ou tabelas usaram o painel original, verificar se a taxa de natalidade de 2023 aparece como zero. Se sim, devem ser refeitas com o arquivo corrigido.

5. **Regenerar o painel:** Se for necessário regenerar o painel no futuro, usar o script `scripts/gerar_painel_longitudinal.py` já corrigido.

---

*Auditoria concluída. Painel corrigido aprovado para uso.*
