# CAGED — Limitações para o Estudo

## Estrutura dos Dados

O FTP do MTE disponibiliza dois conjuntos de dados do CAGED:

### 1. CAGEDEST (até 2019)
- Arquivos mensais (`CAGEDEST_MMYYYY.7z`)
- Cobertura: 2007–2019
- **Não possui coluna de nacionalidade**

### 2. Novo CAGED (a partir de 2020)
- Arquivos mensais por competência (`CAGEDMOVAAAAMM.7z`, `CAGEDFORAAAAMM.7z`, `CAGEDEXCAAAAMM.7z`)
- Cobertura: 2020–2026
- **28 colunas, incluindo:**
  - `competênciamov`, `região`, `uf`, `município`
  - `seção`, `subclasse` (CNAE)
  - `cbo2002ocupação`, `graudeinstrução`, `idade`
  - `sexo`, `raçacor`, `salário`, `horascontratuais`
  - `tipomovimentação` (admisão/demissão), `saldomovimentação`
- **NÃO possui coluna de nacionalidade**

## Implicações para o Estudo

| Base | Identifica Venezuelanos? | Utilidade para o Estudo |
|------|-------------------------|------------------------|
| RAIS | ✅ Sim (código 26) | **Principal fonte** de vínculos empregatícios |
| CAGED | ❌ Não | Contexto geral do mercado de trabalho em SC |

## Decisão Metodológica

O CAGED **não será utilizado** como fonte primária para identificar vínculos de venezuelanos, pois não dispõe da variável `nacionalidade`. Ele poderia ser utilizado apenas para:

1. **Contextualização**: dinâmica geral do mercado de trabalho em SC (admisões/demisões totais)
2. **Análise comparativa**: comparar a evolução do emprego geral vs. o emprego de venezuelanos (via RAIS)
3. **Setores de atividade**: identificar quais setores estão mais dinâmicos em SC

No entanto, dado o escopo do projeto e a disponibilidade da RAIS (que cobre 2018–2023 e já está sendo processada), o CAGED é considerado **fonte secundária opcional**.

## Nota Técnica

O Novo CAGED passou a ser divulgado mensalmente a partir de janeiro de 2020, com três arquivos por competência:
- `CAGEDMOV`: movimentações dentro do prazo
- `CAGEDFOR`: movimentações fora do prazo  
- `CAGEDEXC`: movimentações excluídas

Para análises futuras que não dependam de nacionalidade, o CAGED oferece vantagens:
- Frequência mensal (vs. anual da RAIS)
- Dados mais atualizados
- Saldo de movimentações (admisões − demissões)
