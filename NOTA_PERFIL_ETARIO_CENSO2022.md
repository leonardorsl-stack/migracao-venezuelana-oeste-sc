# Nota Metodológica Crítica: Perfil Etário e o Censo 2022

## Problema Identificado

O usuário (Prof. Vicente/Leonardo) corretamente apontou que o perfil etário comparativo
(Figura 12) deveria ser baseado nos **microdados do Censo 2022**, não em aproximações.

Após investigação exaustiva, confirmamos que **isto não é possível no momento**.

---

## Motivo 1: Microdados da Amostra NÃO Foram Divulgados

O IBGE **adiou indefinidamente** a divulgação dos microdados da amostra do Censo 2022.

- Data prevista: 4 de dezembro de 2025
- Status atual: **ADIADA para 2026, sem data definida**
- Razão oficial: Preocupações com LGPD e risco de quebra de sigilo via IA

Fonte: IBGE (nov/2025) + Folha de S.Paulo (dez/2025)

> "O IBGE divulgará, em data oportuna a ser definida, 'Censo Demográfico 2022: Microdados da amostra'"
> — IBGE, 04/11/2025 (alterado em 28/11/2025)

Sem os microdados da amostra, não é possível cruzar:
- Nacionalidade (V0620/V0621 do questionário da amostra)
- Idade (V0601)
- Sexo (V0605)
- Município de residência

---

## Motivo 2: Dados Agregados do SIDRA Estão SUPRIMIDOS

Tentamos extrair via API SIDRA a tabela 9606 (Pessoas × Sexo × Idade × Nacionalidade)
para Santa Catarina, filtrando Venezuela (código 79167).

Resultado: **Valores suprimidos ("...")**

```
V: "..."  ← Sigilo estatístico
```

O IBGE suprime dados quando a contagem é inferior a um limiar de sigilo
(geralmente n < 3 ou n < 5 por célula). Como o número de venezuelanos
em SC é relativamente pequeno no Censo 2022, os dados agregados também
não estão disponíveis.

---

## O Que Fizemos (e Por Que Está Limitado)

A Figura 12 usou uma **aproximação metodológica** composta por:

### Lado Esquerdo (População Total do Oeste SC)
- Fonte: Censo 2022 — UNIVERSO (dados completos, disponíveis)
- Variável: População residente por idade e sexo
- Fonte SIDRA/IBGE (tabela de população por idade)

### Lado Direito (Venezuelanos)
- Fonte: RAIS 2023–2024 (agregado)
- Variável: Vínculos de emprego por faixa etária e sexo
- **LIMITAÇÃO CRÍTICA:** A RAIS cobre apenas trabalhadores formais com vínculo CLT.
  NÃO inclui:
  - Crianças e adolescentes
  - Idosos (65+)
  - Desempregados
  - Trabalhadores informais
  - Dependentes familiares
  - Mulheres em licença maternidade ou fora do mercado formal

---

## Implicações

A pirâmide etária da RAIS mostra o perfil dos **TRABALHADORES VENEZUELANOS FORMALES**,
não do **TOTAL da população venezuelana residente** no Oeste SC.

Isso explica por que:
- 14–17 anos = 0% (menores não podem ter vínculo CLT)
- 18–24 anos = 0,8% (poucos com vínculo formal nessa idade)
- 65+ = 0,2% (quase nenhum idoso com vínculo formal)
- Pico em 25–49 = 70% (idade produtiva típica de migração laboral)

A população venezuelana REAL no Oeste SC certamente inclui:
- Crianças (filhos de migrantes)
- Adolescentes
- Idosos (pais que acompanharam)
- Desempregados
- Informais

---

## Alternativas Futuras

1. **Aguardar microdados do Censo 2022** (sem previsão)
2. **Usar Censo 2010** como baseline histórico (mas não captura a migração venezuelana)
3. **Usar PNAD Contínua** — mas NÃO tem campo de nacionalidade
4. **Usar Cadastro Único (CadÚnico)** — pode ter nacionalidade, mas acesso restrito
5. **Usar dados do SINCRE (Polícia Federal)** — registros de RNM, mas não é público
6. **Usar dados do SISNOM (Conare)** — registros de refugiados, mas incompleto

---

## Recomendação para o Site

Incluir uma **nota de rodapé/clarificação explícita** na Figura 12:

> "O perfil etário dos venezuelanos é baseado nos vínculos de emprego formais (RAIS),
> não na população residente total. Os microdados do Censo 2022 — única fonte que
> permitiria um perfil etário completo da população venezuelana — ainda não foram
> divulgados pelo IBGE. A pirâmide reflete o perfil dos trabalhadores formais, não
> da população total (que inclui crianças, idosos, desempregados e informais)."

---

*Documento elaborado em: abril de 2026*
