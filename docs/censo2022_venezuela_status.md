# Status: Extração de Venezuelanos do Censo 2022

## Problema
A tabela SIDRA 9606 baixada não contém dados de nacionalidade. A classificação D4N representa **Sexo** (Total/Homens/Mulheres), e não nacionalidade. A classificação C6794 (Nacionalidade) é incompatível com esta tabela.

## Tabela 9606 real
**Título:** População residente, por cor ou raça, segundo o sexo e a idade  
**Fonte:** Censo Demográfico 2022

## Tabelas candidatas para nacionalidade
Ainda não identificada via API SIDRA. Possíveis fontes:
1. **SIDRA — outra tabela do Censo 2022** com classificação de país de nascimento/nacionalidade
2. **FTP do IBGE** — microdados do Censo 2022 (AMOSTRA), variável `V0619` (Nacionalidade) ou `V0620` (País de nascimento)
3. **Base dos Dados** — tabelas tratadas do Censo 2022
4. **Panorama do Censo 2022** — interface interativa do IBGE

## Próximo passo
Consultar o portal SIDRA manualmente em https://sidra.ibge.gov.br/pesquisa/censo-demografico/demografico-2022 e localizar a tabela que contenha a classificação **"País de nascimento"** ou **"Nacionalidade"**.

## Script preparado
`scripts/download_censo2022_nacionalidade.py` foi criado para automatizar o download assim que a tabela correta for identificada.

## Referência
O IBGE divulgou que o Censo 2022 registrou **272 mil pessoas nascidas na Venezuela** no Brasil (Agência IBGE, 27/06/2025). A distribuição municipal está disponível nos microdados da amostra.
