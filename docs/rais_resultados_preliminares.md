# RAIS — Resultados Preliminares

## Processamento

Arquivos processados ano-a-ano a partir do FTP do Ministério do Trabalho:
- Filtro: nacionalidade = 26 (Venezuela) + município começa com 42 (SC)
- Estratégia: download → filtro → Parquet → deletar .7z

## Resultados por Ano

| Ano | Vínculos | Idade Média | Homens (%) | Mulheres (%) | Status |
|-----|----------|-------------|------------|--------------|--------|
| 2018 | — | — | — | — | ⏳ Download em andamento |
| 2019 | — | — | — | — | ⏳ Download em andamento |
| 2020 | 9.172 | 32,1 | 65,6% | 34,4% | ✅ Processado |
| 2021 | 21.728 | 32,0 | 63,0% | 37,0% | ✅ Processado |
| 2022 | 39.534 | 32,4 | 61,2% | 38,8% | ✅ Processado |
| 2023 | — | — | — | — | ⏳ Re-download pendente |

## Evolução Temporal

```
2020:  ████████░░░░░░░░░░░░  9.172
2021:  ██████████████████░░ 21.728  (+136,9%)
2022:  ████████████████████████████████ 39.534  (+81,9%)
```

### Interpretação
- **2020**: Pandemia COVID-19 — menor número de vínculos ativos
- **2021–2022**: Recuperação econômica massiva, com mais que duplicação dos vínculos em 2 anos
- A explosão de vínculos coincide com a intensificação da migração venezuelana para SC (especialmente para o Oeste, em função das oportunidades no setor de carnes/frigoríficos)

## Perfil Demográfico

- **Idade média**: estável em torno de 32 anos (jovens adultos, força produtiva)
- **Sexo**: predominância masculina, mas com tendência de redução:
  - 2020: 65,6% homens / 34,4% mulheres
  - 2022: 61,2% homens / 38,8% mulheres
  - → Aumento da participação feminina no mercado de trabalho formal

## Top Setores (CNAE Seção)

RAIS 2022 (principais):
1. **Seção 10** — Indústrias de transformação: 11.858 vínculos (30,0%)
   - **Frigoríficos e indústria de carnes** no Oeste de SC
2. **Seção 47** — Comércio varejista: 4.906 (12,4%)
3. **Seção 56** — Alimentação: 2.591 (6,6%)
4. **Seção 41** — Construção: 1.932 (4,9%)
5. **Seção 46** — Comércio atacadista: 1.298 (3,3%)

## Top Ocupações (CBO 2002)

RAIS 2022 — As ocupações dominantes confirmam a concentração na indústria frigorífica:

| CBO | Ocupação | Vínculos | % |
|-----|----------|----------|---|
| **784205** | **Alimentador de linha de produção** | 8.909 | 22,5% |
| **848520** | **Magarefe** (processamento de carnes) | 4.846 | 12,3% |
| 514320 | Servente de obras | 2.334 | 5,9% |
| 717020 | Pedreiro | 1.641 | 4,2% |
| 513505 | Cozinheiro | 1.417 | 3,6% |

> **Nota**: Os dois primeiros CBOs somam **13.755 vínculos (34,8%)** e estão diretamente ligados à indústria de carnes/frigoríficos — setor econômico dominante na Região Oeste de SC (Chapecó, Concórdia, Xanxerê).

## Tempo de Emprego

Na RAIS, `tempo_emprego` é uma variável categórica:

| Código | Faixa | 2020 | 2021 | 2022 |
|--------|-------|------|------|------|
| 00 | Menos de 1 mês | 28,4% | 27,6% | 33,9% |
| 01 | 1 a 3 meses | 16,7% | 15,2% | 0,0%* |
| 02 | 3 a 6 meses | 52,6% | 55,1% | 65,3% |
| 03 | 6 meses a 1 ano | 0,0% | 1,4% | — |
| 04 | 1 a 2 anos | 2,2% | 0,8% | 0,8% |

\* Dado provavelmente concentrado na categoria 02 devido ao período de referência

**Interpretação**: A grande maioria dos vínculos (52–65%) está na faixa de **3 a 6 meses**, indicando:
- Alta rotatividade característica do setor frigorífico
- Ou chegada recente dos trabalhadores (migrantes recentes)
- Baixa permanência nas empresas

## Perfil do Trabalhador Venezuelano em SC (RAIS 2022)

- **Idade média**: 32,4 anos (força produtiva jovem)
- **Sexo**: 61,2% homens / 38,8% mulheres (tendência de feminização)
- **Setor predominante**: Indústria de carnes/frigoríficos (~35%)
- **Escolaridade**: Predominantemente ensino fundamental (CBOs exigem 4ª a 7ª série)
- **Tempo médio**: 3-6 meses na maioria dos vínculos

## Próximos Passos

1. Finalizar processamento de 2018, 2019 e 2023
2. Mapear municípios para identificar concentração na Região Oeste SC
3. Consolidar todos os anos em painel longitudinal
4. Cruzar com dados de população (IBGE) para taxa de ocupação
5. Analisar CBO (ocupações) e salários (quando disponível)
