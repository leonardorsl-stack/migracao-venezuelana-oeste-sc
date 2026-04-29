# Relatório de Auditoria dos Dados
> Elaborado em: abril de 2026
> Projeto: Crise, migração e trabalho — Venezuelanos no Oeste de SC

---

## ✅ DADOS VERIFICADOS E CORRETOS

### 1. RAIS (Emprego)
| Ano | Vínculos SC | Vínculos Oeste SC (painel) | Status |
|-----|-------------|---------------------------|--------|
| 2018 | 812 | 66 | ✓ |
| 2019 | 3.492 | 1.095 | ✓ |
| 2020 | 9.172 | 3.990 | ✓ |
| 2021 | 21.728 | 10.365 | ✓ |
| 2022 | 39.534 | 18.577 | ✓ |
| 2023 | 61.760 | 28.959 | ✓ |
| 2024 | 90.447 | 40.420 | ✓ |
| **Total** | **226.945** | — | ✓ |

- Taxas per mil calculadas corretamente (diferença < 0.0001)
- 109 municípios no painel, 104 com vínculos em 2024
- 18 municípios sem vínculos em 2024 (pequenos, rurais)

### 2. SIH/SUS (Internações)
| Métrica | Valor | Status |
|---------|-------|--------|
| Total SC | 14.661 | ✓ |
| Total Oeste SC | 7.696 (52,5%) | ✓ |
| Valor total SC | R$ 20.069.524,84 | ✓ |
| Valor Oeste SC | R$ 10.460.409,84 (52,1%) | ✓ |

- Top 5 CIDs verificados e corretos
- Filtro de municípios: 70 municípios do Oeste com registros

### 3. Mapas Coropléticos
- Shapefile IBGE 2022: 5.572 municípios
- Interseção painel × shapefile: **109 de 109** municípios ✓

### 4. CIDs (Relatório)
| CID | Relatório | Dados Brutos | Status |
|-----|-----------|--------------|--------|
| O800 | 931 | 931 | ✓ |
| O809 | 389 | 389 | ✓ |
| O829 | 208 | 208 | ✓ |
| O334 | 187 | 187 | ✓ |
| Z302 | 170 | 170 | ✓ |

---

## ⚠️ PROBLEMAS IDENTIFICADOS

### PROBLEMA 1 — Perfil Etário (Figura 12): NÃO é do Censo 2022
**Gravidade: ALTA (limitação metodológica)**

A pirâmide etária dos venezuelanos usa dados da **RAIS** (vínculos formais), não do Censo 2022.

**Por que isso é um problema:**
- A RAIS só cobre trabalhadores com vínculo CLT
- NÃO inclui: crianças, adolescentes, idosos, desempregados, informais
- A pirâmide mostra 0% em 14-17 anos e 65+ porque esses grupos não têm vínculo formal
- O perfil real da população venezuelana residente é diferente

**Causa raiz:**
- Os microdados da amostra do Censo 2022 **ainda não foram divulgados** pelo IBGE
- Adiados de dezembro/2025 para data indefinida em 2026 (motivo: LGPD)
- Dados agregados do SIDRA estão suprimidos por sigilo estatístico

**Ação necessária:**
- Adicionar nota explicativa em todas as figuras de perfil etário
- Título deve ser: "Perfil Etário dos Trabalhadores Venezuelanos (RAIS)"
- NÃO "Perfil Etário da População Venezuelana"

---

### PROBLEMA 2 — Saltos de População em 2022 (Censo vs Estimativas)
**Gravidade: MÉDIA (quebra de série)**

12 municípios tiveram saltos de população > 20% entre 2021 e 2022.

**Exemplo mais extremo — Guatambú:**
| Ano | População | Fonte | Vínculos | Taxa per mil |
|-----|-----------|-------|----------|--------------|
| 2021 | 4.692 | Estimativa intercensitária | 395 | 84.2 |
| 2022 | 8.425 | **Censo 2022** | 747 | 88.7 |
| 2024 | 9.267 | Estimativa pós-censo | 2.583 | 278.7 |

**Por que aconteceu:**
- 2018-2021: estimativas intercensitárias (baseadas no Censo 2010)
- 2022: população residente contada no Censo 2022
- As estimativas subestimavam a população real de municípios pequenos
- Isso é um fenômeno conhecido e esperado

**Impacto:**
- As taxas per mil de 2021 vs 2022 **não são diretamente comparáveis** para esses municípios
- O salto em Guatambú de 84 → 89 per mil é pequeno, mas o salto populacional é grande
- A taxa de 278.7 em 2024 é real (2.583 vínculos / 9.267 hab)

**Outros municípios afetados:**
Piratuba (+58,6%), Caxambu do Sul (+33,3%), Paial (+33,4%), Marema (+28,2%), etc.

**Ação necessária:**
- Adicionar nota sobre quebra de série em 2022 devido ao Censo
- Usar população do Censo 2022 como referência para análises de 2022-2024
- Ser cauteloso ao comparar taxas 2021 vs 2022

---

### PROBLEMA 3 — Dados de Nascimentos (SINASC) Só Até 2022
**Gravidade: BAIXA (dados faltantes, não erro)**

| Ano | Óbitos (SIM) | Nascimentos (SINASC) | Status |
|-----|-------------|---------------------|--------|
| 2018 | 6.703 | 16.063 | ✓ |
| 2019 | 6.900 | 16.120 | ✓ |
| 2020 | 7.268 | 15.890 | ✓ |
| 2021 | 10.335 | 15.884 | ✓ |
| 2022 | 8.803 | 16.106 | ✓ |
| 2023 | 7.913 | **0** | ⚠️ SINASC 2023 não disponível |
| 2024 | **0** | **0** | ⚠️ SIM 2024 e SINASC 2024 não disponíveis |

**Causa:**
- SIM 2024: `DOSC2024.dbc` foi convertido (52.224 óbitos em SC), mas **sem filtro de nacionalidade**
- SINASC 2023-2024: não processados (campo de nacionalidade não funcional)

**Ação necessária:**
- Ocultar ou desativar indicadores de mortalidade/natalidade no site/dashboard
- Ou adicionar nota: "Dados de mortalidade e natalidade disponíveis até 2023/2022"

---

## 📊 RESUMO DA QUALIDADE DOS DADOS

| Base de Dados | Período | Qualidade | Problemas |
|---------------|---------|-----------|-----------|
| RAIS | 2018-2024 | ✅ Excelente | — |
| SIH/SUS | 2018-2025 | ✅ Excelente | — |
| População (IBGE) | 2018-2024 | ⚠️ Boa | Quebra de série 2022 (Censo) |
| SIM (óbitos) | 2018-2023 | ⚠️ Regular | Sem filtro de nacionalidade; 2024 indisponível |
| SINASC (nascimentos) | 2018-2022 | ⚠️ Regular | Sem filtro de nacionalidade; 2023-2024 indisponível |
| Censo 2022 (perfil etário) | — | ❌ Indisponível | Microdados não divulgados |

---

## ✅ RECOMENDAÇÕES PARA O SITE

1. **Figura 12 (Pirâmide Etária):**
   - Título: "Perfil Etário dos Trabalhadores Venezuelanos na RAIS vs População Total"
   - Nota: "Fonte RAIS: apenas vínculos formais. Não inclui crianças, idosos, informais."

2. **Figuras 13 e 17 (Distribuição etária):**
   - Mesma nota metodológica
   - Destacar que é o perfil da **força de trabalho formal**

3. **Mapas e taxas:**
   - Nota sobre quebra de série populacional em 2022
   - Taxas per mil de 2022 em diante usam Censo 2022 como denominador

4. **Indicadores de mortalidade/natalidade:**
   - Ocultar no dashboard ou limitar a 2018-2022/2023
   - Explicar indisponibilidade de dados mais recentes

5. **Geral:**
   - Todas as visualizações devem ter fonte e nota metodológica visível
   - Ser transparente sobre limitações

---

*Relatório elaborado para revisão pelos Professores Vicente Neves da Silva Ribeiro e Leonardo Rafael Santos Leitão (UFFS)*
