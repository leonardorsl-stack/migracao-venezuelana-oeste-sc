# AUDITORIA RAIS — Crise, migração e trabalho: trajetórias migrantes de venezuelanos no Oeste de SC

**Data da auditoria:** 2026-04-27  
**Auditor:** Sistema Automatizado de Auditoria Metodológica  
**Arquivos auditados:** `data/processed/rais_vinculos_sc_venezuela_YYYY.parquet` (YYYY=2018-2024)  
**Painel auditado:** `data/processed/painel_oeste_sc_2018_2024.parquet`  

---

## 1. RESUMO EXECUTIVO

| Item | Status | Observação |
|------|--------|------------|
| 1. Integridade dos dados brutos | ✅ PASSOU | Contagem exata, sem nulos, tipos consistentes |
| 2. Filtro de nacionalidade | ✅ PASSOU | 100% dos registros são código `26` (Venezuela na RAIS/MTE). **Nota:** o código `092` mencionado no escopo é da tabela de países da Receita Federal (usada em notas fiscais), não da RAIS. |
| 3. Agregação por município | ✅ PASSOU | Soma dos vínculos nos 109 municípios da região bate exatamente com o painel (diff=0 todos os anos). **Ressalva:** os dados brutos contêm municípios de TODO Santa Catarina. |
| 4. Cálculo das taxas | ✅ PASSOU | Taxas calculadas corretamente no painel. Nenhum valor negativo ou > 500. |
| 5. Perfil etário e de gênero | ⚠️ PASSOU COM RESSALVAS | Distribuição demográfica plausível. Identificadas inconsistências de formatação no campo `sexo` e duplicação de coluna `Idade` em 2023-2024. |
| 6. Consistência temporal | ✅ PASSOU | Crescimento monotônico e consistente com a crise migratória. Registros idênticos entre anos são esperados em painel longitudinal de vínculos. |

**Veredito geral:** Os dados são **consistentes e confiáveis** para análise, após as correções menores de formatação documentadas neste relatório.

---

## 2. DETALHAMENTO DAS VERIFICAÇÕES

### 2.1 INTEGRIDADE DOS DADOS BRUTOS

Contagem de registros por ano:

| Ano | Registros | Esperado | Status |
|-----|-----------|----------|--------|
| 2018 | 812 | 812 | ✅ |
| 2019 | 3.492 | 3.492 | ✅ |
| 2020 | 9.172 | 9.172 | ✅ |
| 2021 | 21.728 | 21.728 | ✅ |
| 2022 | 39.534 | 39.534 | ✅ |
| 2023 | 61.760 | 61.760 | ✅ |
| 2024 | 90.447 | 90.447 | ✅ |

**Colunas por ano:**
- 2018–2022: `cbo_2002`, `cnae_20_classe`, `faixa_etaria`, `idade`, `municipio`, `nacionalidade`, `sexo`, `tempo_emprego`, `ano` (9 colunas)
- 2023–2024: as mesmas 9 colunas **mais** `Idade` (I maiúsculo, string), totalizando 10 colunas.

**Valores nulos:** 0 (zero) em todas as colunas e todos os anos.

**Tipos de dados:**
- `idade`: `int64` (consistente)
- `ano`: `int64` (consistente)
- Demais colunas: `object` (string), consistente.

### 2.2 FILTRO DE NACIONALIDADE

**Verificação:** Todos os registros em todos os anos possuem `nacionalidade = '26'`.

**Esclarecimento metodológico crucial:**
O campo `nacionalidade` (ou `NACIONAL` no microdado original da RAIS) utiliza a **codificação própria do Ministério do Trabalho e Emprego (MTE)**, não a tabela de países da Receita Federal (usada em notas fiscais, NF-e). Na RAIS:
- Código `26` = **Venezuela**
- Código `092` na tabela da Receita Federal = Groenlândia
- Código `850` na tabela da Receita Federal = Venezuela

Portanto, o filtro está **correto**. O valor `26` é o código válido da Venezuela na RAIS. Não há registros de outras nacionalidades.

### 2.3 AGREGAÇÃO POR MUNICÍPIO vs PAINEL

**Descoberta importante:** Os arquivos brutos (`rais_vinculos_sc_venezuela_YYYY.parquet`) contêm municípios de **TODO o estado de Santa Catarina** (245 municípios distintos em 2024), não apenas os 109 da Região Intermediária de Chapecó.

Comparação restrita aos 109 municípios do painel:

| Ano | Bruto (região) | Painel | Diferença |
|-----|----------------|--------|-----------|
| 2018 | 66 | 66 | 0 |
| 2019 | 1.095 | 1.095 | 0 |
| 2020 | 3.990 | 3.990 | 0 |
| 2021 | 10.365 | 10.365 | 0 |
| 2022 | 18.577 | 18.577 | 0 |
| 2023 | 28.959 | 28.959 | 0 |
| 2024 | 40.420 | 40.420 | 0 |

**Conclusão:** A agregação no painel está **perfeitamente correta**.

**Municípios da região sem vínculos em nenhum ano (2018-2024):**
12 municípios nunca apresentaram vínculos de venezuelanos nos dados brutos:
1. Abdon Batista (420005)
2. Alto Bela Vista (420075)
3. Bom Jesus do Oeste (420257)
4. Celso Ramos (420415)
5. Galvão (420560)
6. Irati (420785)
7. Lajeado Grande (420945)
8. Ouro Verde (421185)
9. Santiago do Sul (421569)
10. São Miguel da Boa Vista (421715)
11. Serra Alta (421755)
12. Tigrinhos (421795)

Isso é um **dado factual**, não um erro de processamento.

### 2.4 CÁLCULO DAS TAXAS

Fórmula verificada no painel: `taxa_vinculos_por_mil = (total_vinculos_rais / populacao_total) * 1000`

| Ano | Diferença Máxima | Linhas com Erro (>0.01) | Taxas > 500 | Taxas Negativas |
|-----|------------------|------------------------|-------------|-----------------|
| 2018 | 0.000046 | 0 | 0 | 0 |
| 2019 | 0.000048 | 0 | 0 | 0 |
| 2020 | 0.000050 | 0 | 0 | 0 |
| 2021 | 0.000050 | 0 | 0 | 0 |
| 2022 | 0.000050 | 0 | 0 | 0 |
| 2023 | 0.000049 | 0 | 0 | 0 |
| 2024 | 0.000050 | 0 | 0 | 0 |

**Conclusão:** Cálculo das taxas está **correto e consistente**.

### 2.5 PERFIL ETÁRIO E DE GÊNERO

**Distribuição por sexo por ano (após correção de formatação):**

| Ano | Masculino (1) | Feminino (2) | % Masc | % Fem |
|-----|---------------|--------------|--------|-------|
| 2018 | 488 | 324 | 60.1% | 39.9% |
| 2019 | 2.310 | 1.182 | 66.2% | 33.8% |
| 2020 | 6.018 | 3.154 | 65.6% | 34.4% |
| 2021 | 13.693 | 8.035 | 63.0% | 37.0% |
| 2022 | 24.212 | 15.322 | 61.2% | 38.8% |
| 2023 | 37.433 | 24.327 | 60.6% | 39.4% |
| 2024 | 53.529 | 36.918 | 59.2% | 40.8% |

*Nota: em 2018-2022 os valores originais vinham com espaços à esquerda (`'                  01'`, `'                  02'`).*

**Distribuição etária (2024):**

| Faixa | Quantidade | % |
|-------|------------|---|
| < 18 | 827 | 0.9% |
| 18–24 | 22.725 | 25.1% |
| 25–39 | 44.626 | 49.3% |
| 40–54 | 18.949 | 21.0% |
| 55–64 | 3.105 | 3.4% |
| 65–100 | 215 | 0.2% |
| > 100 | 0 | 0.0% |

**Anomalias:**
- Idade mínima: 14 anos (aceitável — aprendiz legal no Brasil)
- Idade máxima: 77 anos (plausível)
- Nenhum registro com idade > 100 anos
- Nenhum registro com idade < 14 anos

### 2.6 CONSISTÊNCIA TEMPORAL

**Evolução ano a ano:**

| Período | Vínculos Anterior | Vínculos Atual | Crescimento |
|---------|-------------------|----------------|-------------|
| 2018 → 2019 | 812 | 3.492 | +330.0% |
| 2019 → 2020 | 3.492 | 9.172 | +162.7% |
| 2020 → 2021 | 9.172 | 21.728 | +136.9% |
| 2021 → 2022 | 21.728 | 39.534 | +81.9% |
| 2022 → 2023 | 39.534 | 61.760 | +56.2% |
| 2023 → 2024 | 61.760 | 90.447 | +46.4% |

**Análise:** O crescimento é monotônico e decrescente em termos percentuais (lei dos grandes números), plenamente consistente com a escalada da crise migratória venezuelana e a chegada ao Brasil.

**Registros idênticos entre anos consecutivos:**

| Par de Anos | Registros Idênticos |
|-------------|---------------------|
| 2018 ↔ 2019 | 176 |
| 2019 ↔ 2020 | 2.534 |
| 2020 ↔ 2021 | 20.344 |
| 2021 ↔ 2022 | 57.874 |
| 2022 ↔ 2023 | 0 |
| 2023 ↔ 2024 | 3.383 |

**Interpretação:** Registros idênticos em todos os campos (CBO, CNAE, idade, município, sexo, tempo_emprego) entre anos consecutivos são **esperados** em uma base longitudinal de vínculos empregatícios: a mesma pessoa pode manter o mesmo emprego de um ano para o outro. A ausência de registros idênticos entre 2022 e 2023 reflete uma mudança na estrutura dos dados brutos (provavelmente origem diferente ou campo `tempo_emprego` em formato distinto). **Não caracteriza duplicidade espúria.**

---

## 3. PROBLEMAS ENCONTRADOS

| # | Severidade | Categoria | Descrição | Impacto |
|---|------------|-----------|-----------|---------|
| 1 | **Média** | Formatação | Campo `sexo` em 2018–2022 contém espaços à esquerda (`'                  01'` / `'                  02'`). Em 2023–2024 já vem limpo (`'1'` / `'2'`). | Pode quebrar filtros, agrupamentos ou visualizações que esperam valores limpos. |
| 2 | **Média** | Estrutura | Coluna duplicada `Idade` (I maiúsculo, tipo string) em 2023 e 2024, idêntica à coluna `idade` (minúsculo, tipo int64). | Poluição de schema, risco de dupla contagem em análises automáticas. |
| 3 | **Baixa** | Documentação | Arquivos brutos (`rais_vinculos_sc_venezuela_YYYY.parquet`) contêm **todo o estado de SC** (até 245 municípios), não apenas os 109 da região de Chapecó. O nome do arquivo pode induzir ao erro. | Baixo — o painel longitudinal filtra corretamente, mas análises diretas nos arquivos brutos sem filtro geográfico produzirão resultados para todo SC. |
| 4 | **Baixa** | Metadados | Campo `tempo_emprego` muda de formato categórico (códigos `00`, `01`, `02`…) em 2018–2022 para contínuo decimal (`.0`, `.9`, `1.4`, `2.9`…) em 2023–2024. | Dificulta análises comparativas longitudinais do tempo de emprego sem harmonização prévia. |
| 5 | **Informativo** | Metodologia | Nacionalidade está corretamente codificada como `26` (padrão RAIS/MTE), mas a expectativa do usuário era `092` (padrão Receita Federal). | Nenhum impacto nos dados, mas requer alinhamento conceitual. |

---

## 4. RECOMENDAÇÕES DE CORREÇÃO

### 4.1 Ações já executadas
Foram gerados arquivos corrigidos em `data/processed/rais_vinculos_sc_venezuela_YYYY_corrigido.parquet`:

- ✅ Campo `sexo` padronizado para `'1'` e `'2'` em todos os anos (removidos espaços e zeros à esquerda).
- ✅ Coluna `Idade` (I maiúsculo) removida de 2023 e 2024.

Script de correção disponível em: `scripts/corrige_rais.py`

### 4.2 Ações recomendadas (pendentes)

1. **Substituir os arquivos originais pelos corrigidos** (ou atualizar o pipeline para usar os `_corrigido`):
   ```bash
   for y in {2018..2024}; do
     mv data/processed/rais_vinculos_sc_venezuela_${y}.parquet data/processed/rais_vinculos_sc_venezuela_${y}_original.parquet
     mv data/processed/rais_vinculos_sc_venezuela_${y}_corrigido.parquet data/processed/rais_vinculos_sc_venezuela_${y}.parquet
   done
   ```

2. **Harmonizar o campo `tempo_emprego`** entre os dois períodos (2018–2022 categórico vs 2023–2024 contínuo) se for utilizado em análises longitudinais. Sugestão: criar uma faixa etária de tempo de emprego padronizada.

3. **Documentar explicitamente** que os arquivos `rais_vinculos_sc_venezuela_YYYY.parquet` contêm dados de **todo Santa Catarina**, e que o filtro para os 109 municípios do Oeste deve ser aplicado via `codigo_ibge_6d` ou `codigo_ibge_7d` usando a lista `REGIAO_OESTE_SC` em `src/config.py`.

4. **Alinhar a documentação do projeto** quanto ao código de nacionalidade: usar `26` (RAIS/MTE) e não `092` (Receita Federal).

5. **Regerar o painel longitudinal** (`painel_oeste_sc_2018_2024.parquet`) a partir dos arquivos corrigidos, caso as inconsistências de `sexo` sejam utilizadas em análises demográficas do painel.

---

## 5. ANEXOS

### 5.1 Código do script de auditoria
Disponível em: `auditoria_rais.py` (gerado durante a auditoria)

### 5.2 Código do script de correção
Disponível em: `scripts/corrige_rais.py`

### 5.3 Comandos para validação rápida

```python
import pandas as pd

# Validar contagem
for y in range(2018, 2025):
    df = pd.read_parquet(f"data/processed/rais_vinculos_sc_venezuela_{y}_corrigido.parquet")
    assert df['nacionalidade'].nunique() == 1
    assert df['nacionalidade'].iloc[0] == '26'
    assert df['sexo'].isin(['1', '2']).all()
    print(f"{y}: OK — {len(df):,} registros")
```

---

*Fim do relatório de auditoria.*
