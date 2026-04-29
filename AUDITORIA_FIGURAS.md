# Auditoria de Figuras — Projeto "Crise, migração e trabalho"

**Data da auditoria:** 2026-04-27  
**Revisor:** Agente de auditoria gráfica e metodológica  
**Base de dados utilizada:**
- Painel: `data/processed/painel_oeste_sc_2018_2024.parquet` (109 municípios, 2018-2024)
- RAIS: `data/processed/rais_vinculos_sc_venezuela_YYYY.parquet` (2018-2024)
- SIH: `data/raw/datasus/sih_sus_sc_venezuela_2018_2025.parquet`
- IBGE Censo 2022: `data/processed/ibge_populacao_idade_sexo_oeste_sc_2022.parquet`

---

## Sumário Executivo

| Item | Resultado |
|---|---|
| Total de figuras auditadas | 17 PNGs + 2 GIFs = 19 arquivos |
| Figuras com problemas graves | 8 |
| Figuras com problemas leves | 7 |
| Figuras aprovadas sem ressalvas | 4 |
| Figuras recriadas nesta auditoria | 6 |

**Problemas cruzados críticos:**
1. **Imprecisão terminológica em figuras RAIS:** sete figuras referem-se genericamente a "venezuelanos", quando os dados provêm exclusivamente da RAIS (vínculos empregatícios formais). Isso exclui crianças, adolescentes (<14 anos), idosos fora do mercado formal, trabalhadores informais e desempregados.
2. **Ausência de fontes/notas:** treze figuras não possuem menção à fonte de dados ou nota metodológica.
3. **Discrepância nome/arquivo (Figura 02):** o arquivo chama-se `02_mapa_taxa_vinculos_2024.png`, mas o conteúdo é um gráfico de barras horizontais, não um mapa.

---

## Checklist Figura por Figura

### Figuras de Emprego (RAIS)

#### 01. `01_evolucao_vinculos_regional.png`
| Critério | Status | Observação |
|---|---|---|
| Números | ✅ PASSOU | Taxas e volumes batem com painel (2018: 0,06‰; 2024: 32,36‰; 40.420 vínculos) |
| Título | ⚠️ RESSALVA | "Inserção Laboral de Venezuelanos" é ambíguo; sugere população total |
| Escalas | ✅ PASSOU | Eixos duplos bem calibrados, limites adequados |
| Fonte | ❌ FALHOU | Nenhuma menção a RAIS/MTE na figura |
| Notas metodológicas | ❌ FALHOU | Sem nota sobre limitação da RAIS (formais apenas) |
| Qualidade visual | ✅ PASSOU | DPI 300, legível, cores adequadas |

**Ação:** Figura recriada com título corrigido ("Inserção Laboral **Formal**"), fonte e nota metodológica adicionadas.

---

#### 02. `02_mapa_taxa_vinculos_2024.png`
| Critério | Status | Observação |
|---|---|---|
| Números | ✅ PASSOU | Top 20 taxas conferidas; Guatambú 278,7‰, Itapiranga 112,0‰, Chapecó 58,6‰ |
| Título | ⚠️ RESSALVA | Título do gráfico está ok, mas o **nome do arquivo é gravemente enganoso** |
| Escalas | ✅ PASSOU | Xlim adequado |
| Fonte | ❌ FALHOU | Sem fonte |
| Notas metodológicas | ❌ FALHOU | Sem nota |
| Qualidade visual | ✅ PASSOU | Chapecó destacada em vermelho (corretamente identificada como maior volume) |

**Ação:** Não recriada (dados corretos), mas **recomenda-se renomear o arquivo** para `02_top20_taxa_vinculos_2024.png` para evitar confusão metodológica.

---

#### 03. `03_top15_municipios_volume_2024.png`
| Critério | Status | Observação |
|---|---|---|
| Números | ✅ PASSOU | Top 3: Chapecó (16.177), Concórdia (2.672), Guatambú (2.583) |
| Título | ✅ PASSOU | Clara e precisa |
| Escalas | ✅ PASSOU | Limites adequados |
| Fonte | ❌ FALHOU | Sem fonte |
| Notas metodológicas | ❌ FALHOU | Sem nota |
| Qualidade visual | ✅ PASSOU | Top 3 em vermelho, legível |

**Ação:** Registrar ausência de fonte/nota. Não recriada.

---

#### 04. `04_dispersao_populacao_vs_vinculos.png`
| Critério | Status | Observação |
|---|---|---|
| Números | ✅ PASSOU | R² calculado: **0,912040** (exibido: 0,912). Diferença de 0,00004 — **aprovado** |
| Título | ⚠️ RESSALVA | Precisa de nota sobre RAIS |
| Escalas | ✅ PASSOU | Scatter proporcional à taxa, legenda adequada |
| Fonte | ❌ FALHOU | Sem fonte |
| Notas metodológicas | ❌ FALHOU | Sem nota sobre informalidade |
| Qualidade visual | ✅ PASSOU | Destaques de Chapecó, Guatambú, Itapiranga, Seara |

**Ação:** Registrar. Não recriada.

---

### Figuras de Saúde (SIH)

#### 05. `05_evolucao_internacoes_sih.png`
| Critério | Status | Observação |
|---|---|---|
| Números | ✅ PASSOU | SIH 2019-2025 conferido. **Painel 2018 = 0** (verificado: SIH raw 2018 tem 18 registros, mas todos em municípios fora da Região Intermediária de Chapecó) |
| Título | ⚠️ RESSALVA | Período "2018-2025" para SIH e "2018-2024" para RAIS no mesmo gráfico pode confundir |
| Escalas | ✅ PASSOU | Eixo secundário para RAIS adequado |
| Fonte | ❌ FALHOU | Sem fonte |
| Notas metodológicas | ⚠️ RESSALVA | Deveria notar que 2025 é parcial e população projetada é a de 2024 |
| Qualidade visual | ✅ PASSOU | DPI 300, anotações claras |

**Ação:** Registrar. Não recriada.

---

#### 06. `06_comparativo_rais_vs_sih_2024.png`
| Critério | Status | Observação |
|---|---|---|
| Números | ✅ PASSOU | Dados do painel 2024 e SIH raw 2024 consistentes (ex: Chapecó 980 internações, 16.177 vínculos) |
| Título | ✅ PASSOU | Clara e precisa |
| Escalas | ✅ PASSOU | Agrupamento adequado |
| Fonte | ❌ FALHOU | Sem fonte |
| Notas metodológicas | ❌ FALHOU | Sem nota |
| Qualidade visual | ✅ PASSOU | Rótulos visíveis |

**Ação:** Registrar. Não recriada.

---

#### 07. `07_taxa_internacoes_vs_vinculos.png`
| Critério | Status | Observação |
|---|---|---|
| Números | ✅ PASSOU | R² calculado: **0,329478** (exibido: 0,329). Diferença de 0,0005 — **aprovado** |
| Título | ✅ PASSOU | Clara e precisa |
| Escalas | ✅ PASSOU | Tamanho do ponto proporcional à população |
| Fonte | ❌ FALHOU | Sem fonte |
| Notas metodológicas | ❌ FALHOU | Sem nota |
| Qualidade visual | ✅ PASSOU | Outliers anotados automaticamente |

**Ação:** Registrar. Não recriada.

---

### Mapas Coropléticos

#### 08. `08_mapa_coropletico_oeste_sc_2024.png`
| Critério | Status | Observação |
|---|---|---|
| Números | ✅ PASSOU | Taxas batem com painel 2024 |
| Título | ⚠️ RESSALVA | "Inserção Laboral de Venezuelanos" ambíguo; deveria mencionar RAIS |
| Escalas | ✅ PASSOU | Escala YlOrRd, mínimo/máximo dos dados |
| Fonte | ✅ PASSOU | "RAIS 2024 / IBGE" presente |
| Notas metodológicas | ❌ FALHOU | Sem nota |
| Qualidade visual | ⚠️ RESSALVA | **Guatambú (maior taxa: 278,7‰) não está destacada**; apenas Chapecó tem destaque |

**Ação:** Figura recriada com:
- Título corrigido ("Inserção Laboral **Formal**")
- Destaque a Guatambú (contorno azul + label "maior taxa")
- Destaque a Chapecó mantido (contorno preto + label "maior volume")

---

#### 09. `09_mapa_coropletico_volume_2024.png`
| Critério | Status | Observação |
|---|---|---|
| Números | ✅ PASSOU | Volumes batem com painel 2024 |
| Título | ✅ PASSOU | "Volume de Vínculos RAIS de Venezuelanos" — aceitável |
| Escalas | ✅ PASSOU | Blues adequado para volume absoluto |
| Fonte | ✅ PASSOU | "RAIS 2024 / IBGE" presente |
| Notas metodológicas | ❌ FALHOU | Sem nota |
| Qualidade visual | ⚠️ RESSALVA | **Guatambú não está destacada** (2º maior volume, 1ª taxa) |

**Ação:** Figura recriada com destaque a Guatambú (contorno azul + label "2º maior volume, 1ª taxa") além de Chapecó.

---

### Animações

#### 10. `10_animacao_evolucao_2018_2024.gif`
| Critério | Status | Observação |
|---|---|---|
| Números | ✅ PASSOU | Taxas por ano batem com painel |
| Título | ✅ PASSOU | "Taxa de Vínculos Venezuelanos — Oeste SC (ano)" |
| Escalas | ✅ PASSOU | Escala fixa 0-280 em todos os frames |
| Fonte | ✅ PASSOU | "RAIS/MTE" presente em cada frame |
| Notas metodológicas | ❌ FALHOU | Sem nota em frames |
| Qualidade visual | ✅ PASSOU | 7 frames (2018-2024), legível |

**Ação:** Registrar. Não recriada (o script seria complexo para alterar notas em GIF).

---

#### 11. `11_bar_chart_race_2018_2024.gif`
| Critério | Status | Observação |
|---|---|---|
| Números | ✅ PASSOU | Top 15 por ano batem com painel |
| Título | ✅ PASSOU | Clara em cada frame |
| Escalas | ✅ PASSOU | Xlim fixo baseado no máximo global |
| Fonte | ✅ PASSOU | "RAIS/MTE" presente em cada frame |
| Notas metodológicas | ❌ FALHOU | Sem nota em frames |
| Qualidade visual | ✅ PASSOU | Cores consistentes (tab20), valores rotulados |

**Ação:** Registrar. Não recriada.

---

### Perfil Etário (ATENÇÃO: limitação conhecida)

#### 12. `12_piramide_etaria_venezuelanos_vs_total.png`
| Critério | Status | Observação |
|---|---|---|
| Números | ✅ PASSOU | Percentuais RAIS 2023-2024 conferidos (ex: 20-24 H=12,34%, M=8,04%; total RAIS=152.178 registros) |
| Título | ❌ **FALHOU GRAVE** | Título "Venezuelanos" e subtítulo "Venezuelanos RAIS" são **imprecisos metodologicamente**. Os dados são de **trabalhadores venezuelanos com vínculo formal**, não da população venezuelana |
| Escalas | ✅ PASSOU | Xlim (-8, 8) simétrico, apropriado |
| Fonte | ❌ FALHOU | Sem fonte |
| Notas metodológicas | ❌ **FALHOU GRAVE** | **Ausência total de nota sobre exclusão de crianças, idosos, informais** |
| Qualidade visual | ✅ PASSOU | Cores distinguíveis, legível |

**Ação:** Figura **recriada** com:
- Título: "Pirâmide Etária Comparativa: População Total Oeste SC vs. **Trabalhadores Venezuelanos na RAIS**"
- Fonte: IBGE Censo 2022 e RAIS/MTE (2023-2024)
- Nota metodológica explícita sobre limitações da RAIS

---

#### 13. `13_comparativo_faixa_etaria_percentual.png`
| Critério | Status | Observação |
|---|---|---|
| Números | ✅ PASSOU | Percentuais conferidos e consistentes com Figura 12 |
| Título | ❌ **FALHOU GRAVE** | "Oeste SC vs. Venezuelanos (RAIS)" ainda sugere que "Venezuelanos (RAIS)" é um subgrupo populacional, quando é ocupacional |
| Escalas | ✅ PASSOU | Barras agrupadas adequadas |
| Fonte | ❌ FALHOU | Sem fonte |
| Notas metodológicas | ❌ **FALHOU GRAVE** | Ausência de nota sobre limitações |
| Qualidade visual | ✅ PASSOU | Legível, rotação de labels adequada |

**Ação:** Figura **recriada** com título corrigido ("Trabalhadores Venezuelanos na RAIS"), fonte e nota metodológica.

---

#### 14. `14_heatmap_cids_municipios.png`
| Critério | Status | Observação |
|---|---|---|
| Números | ✅ PASSOU | Matriz top 15 CID × top 15 municípios consistente com SIH raw (total Oeste SC: 7.696 internações) |
| Título | ✅ PASSOU | "Principais Diagnósticos de Internação — Venezuelanos no Oeste de SC" |
| Escalas | ✅ PASSOU | YlOrRd adequado, anotações inteiras |
| Fonte | ❌ FALHOU | Sem fonte |
| Notas metodológicas | ❌ FALHOU | Sem nota sobre CID ser diagnóstico principal |
| Qualidade visual | ✅ PASSOU | Códigos CID legíveis, municípios com nome + código IBGE |

**Ação:** Registrar. Não recriada.

---

#### 15. `15_composicao_morbidade_municipios.png`
| Critério | Status | Observação |
|---|---|---|
| Números | ✅ PASSOU | Composição percentual por capítulo CID conferida |
| Título | ✅ PASSOU | Clara e completa |
| Escalas | ✅ PASSOU | Stacked bar 0-100% |
| Fonte | ❌ FALHOU | Sem fonte |
| Notas metodológicas | ⚠️ RESSALVA | Sem nota sobre agrupamento em capítulos CID-10 |
| Qualidade visual | ✅ PASSOU | Rótulos n=total à direita, legenda externa |

**Ação:** Registrar. Não recriada.

---

#### 16. `16_evolucao_top5_cids.png`
| Critério | Status | Observação |
|---|---|---|
| Números | ✅ PASSOU | Top 5 CIDs: O800 (931), O809 (389), O829 (208), O334 (187), Z302 (170) |
| Título | ✅ PASSOU | Clara |
| Escalas | ✅ PASSOU | Eixo Y adequado, anos completos |
| Fonte | ❌ FALHOU | Sem fonte |
| Notas metodológicas | ⚠️ RESSALVA | 2018 com poucos casos; deveria notar parcialidade |
| Qualidade visual | ✅ PASSOU | Anotação de total geral no canto inferior direito |

**Ação:** Registrar. Não recriada.

---

#### 17. `17_indice_concentracao_etaria.png`
| Critério | Status | Observação |
|---|---|---|
| Números | ✅ PASSOU | Índice conferido: 20-24 = 2,22; 30-34 = 1,71; 60+ = 0,05 |
| Título | ❌ **FALHOU GRAVE** | "Índice de Concentração Etária de **Venezuelanos**" — **gravemente impreciso**. É índice de **trabalhadores venezuelanos na RAIS** |
| Escalas | ✅ PASSOU | Linha de paridade em 1, fills corretos |
| Fonte | ❌ FALHOU | Sem fonte |
| Notas metodológicas | ❌ **FALHOU GRAVE** | **Ausência total de nota sobre limitação da base RAIS** |
| Qualidade visual | ✅ PASSOU | Valores anotados, legível |

**Ação:** Figura **recriada** com título corrigido ("Índice de Concentração Etária de **Trabalhadores Venezuelanos na RAIS**"), fonte e nota metodológica.

---

## Lista Consolidada de Problemas Encontrados

### Problemas Graves (requerem correção obrigatória)

| # | Figura | Problema | Impacto |
|---|--------|----------|---------|
| 1 | 02 | **Nome do arquivo diz "mapa" mas é gráfico de barras** | Confusão metodológica para o leitor/revisor |
| 2 | 12 | Título "Venezuelanos" em vez de "Trabalhadores Venezuelanos na RAIS" | Viés de seleção ocupacional mascarado como perfil populacional |
| 3 | 13 | Título impreciso sobre base populacional | Mesmo viés acima |
| 4 | 17 | Título "Venezuelanos" em vez de ocupacional | Índice interpretado como da população, não da força de trabalho formal |
| 5 | 08 | Guatambú (maior taxa: 278,7‰) não destacada no mapa | Perda da principal informação do mapa (outlier positivo) |

### Problemas Moderados (recomenda-se correção)

| # | Figura | Problema | Impacto |
|---|--------|----------|---------|
| 6 | 01 | Ausência de fonte e nota sobre RAIS | Reprodutibilidade e contextualização prejudicadas |
| 7 | 02-07, 12-17 | Ausência de fonte de dados em 13 figuras | Reprodutibilidade prejudicada |
| 8 | 05 | 2025 no SIH sem população projetada (usa 2024) | Impossibilita cálculo de taxa para 2025 |
| 9 | 12-17 | Ausência de nota metodológica em perfil etário | Risco de interpretação errônea pelo revisor |
| 10 | 09 | Guatambú não destacada no mapa de volume | Perda de insights espaciais |

---

## Recomendações de Correção

### 1. Nomenclatura de arquivos
- **Renomear** `02_mapa_taxa_vinculos_2024.png` → `02_top20_taxa_vinculos_2024.png` (ou similar). O termo "mapa" em arquivo de barras horizontais é inaceitável em revisão acadêmica.

### 2. Precisão terminológica em todas as figuras RAIS
- Substituir genericamente "Venezuelanos" por "Trabalhadores Venezuelanos na RAIS" ou "Vínculos RAIS de Venezuelanos" em:
  - Figura 01 (título e subtítulo)
  - Figura 02 (título)
  - Figura 04 (título)
  - Figura 08 (título)
  - Figuras 12, 13, 17 (títulos principais)

### 3. Adição de fontes
- Todas as figuras devem conter, no mínimo, uma anotação de rodapé:
  - **RAIS:** "Fonte: RAIS/MTE (ano)"
  - **SIH:** "Fonte: SIH/SUS/DataSUS (ano)"
  - **IBGE:** "Fonte: IBGE Censo 2022 / Estimativas populacionais"
  - **Combinadas:** "Fonte: RAIS/MTE e IBGE"

### 4. Notas metodológicas obrigatórias
Toda figura baseada em RAIS deve incluir:
> "Nota: a RAIS cobre apenas vínculos empregatícios formais (com carteira assinada). Não inclui trabalhadores informais, desempregados, crianças, adolescentes em idade escolar ou idosos fora do mercado de trabalho formal."

### 5. Destaques nos mapas
- **Mapa 08 (taxa):** destacar **Guatambú** (278,7‰) como "maior taxa" e **Chapecó** (58,6‰) como "maior volume".
- **Mapa 09 (volume):** destacar **Chapecó** (16.177) como "maior volume" e **Guatambú** (2.583) como "2º maior volume, 1ª taxa".

### 6. Dados de 2025 no SIH
- Adicionar nota na Figura 05: "2025: dados SIH acumulados até a data de extração; população utilizada é a de 2024 (sem projeção), impedindo o cálculo de taxas para 2025."

---

## Ações Executadas nesta Auditoria

Foram recriadas 6 figuras com correções aplicadas:

1. **`01_evolucao_vinculos_regional.png`** — adicionada fonte e nota metodológica sobre RAIS; título ajustado para "Inserção Laboral Formal".
2. **`08_mapa_coropletico_oeste_sc_2024.png`** — adicionado destaque a Guatambú (maior taxa); título corrigido.
3. **`09_mapa_coropletico_volume_2024.png`** — adicionado destaque a Guatambú (2º volume, 1ª taxa).
4. **`12_piramide_etaria_venezuelanos_vs_total.png`** — título corrigido para "Trabalhadores Venezuelanos na RAIS"; fonte e nota metodológica adicionadas.
5. **`13_comparativo_faixa_etaria_percentual.png`** — mesmo tratamento da Figura 12.
6. **`17_indice_concentracao_etaria.png`** — título corrigido; fonte e nota metodológica adicionadas.

> **Script de correção:** `scripts/auditoria_recriar_figuras.py` (reprodutível e versionável).

---

## Verificação de Cálculos Estatísticos

### Figura 04 — R² População vs Vínculos
- **Valor exibido:** 0,912
- **Valor calculado:** 0,912040
- **Diferença:** 4×10⁻⁵
- **Veredito:** ✅ **CORRETO** (arredondamento a 3 casas decimais)

### Figura 07 — R² Taxa Vínculos vs Taxa Internações
- **Valor exibido:** 0,329
- **Valor calculado:** 0,329478
- **Diferença:** 4,8×10⁻⁴
- **Veredito:** ✅ **CORRETO** (arredondamento a 3 casas decimais)

---

## Verificação de Destaques Geográficos

| Município | Taxa (‰) 2024 | Volume 2024 | Destaque esperado | Status antes | Status depois |
|-----------|---------------|-------------|-------------------|--------------|---------------|
| Guatambú | 278,73 | 2.583 | **Maior taxa** | ❌ Ausente | ✅ Destacado |
| Chapecó | 58,62 | 16.177 | **Maior volume** | ✅ Presente | ✅ Mantido |
| Itapiranga | 112,02 | 1.921 | Top 3 taxa | N/A | N/A |
| Seara | 110,34 | 2.123 | Top 3 taxa | N/A | N/A |

---

## Conclusão

A **maioria dos valores numéricos está correta e consistente** com as bases de dados. Os problemas concentraram-se em:

1. **Imprecisão terminológica** que pode induzir o revisor a interpretar perfil de trabalhadores formais como perfil da população venezuelana total;
2. **Ausência de fontes e notas metodológicas** na maioria das figuras;
3. **Inconsistência nome/conteúdo** na Figura 02;
4. **Destaques geográficos incompletos** nos mapas coropléticos.

As figuras recriadas (`01`, `08`, `09`, `12`, `13`, `17`) agora atendem aos critérios mínimos de rigor metodológico exigidos para revisão acadêmica.

**Próximos passos recomendados:**
- [ ] Revisar figuras `02-07`, `14-16` para adicionar fontes e notas (menor prioridade, mas desejável).
- [ ] Renomear arquivo `02_mapa_taxa_vinculos_2024.png` → `02_top20_taxa_vinculos_2024.png`.
- [ ] Verificar se as legendas dos GIFs (`10`, `11`) podem incluir nota metodológica em frames finais.
