# Scripts de Integração com Plataformas Abertas

Este diretório contém utilitários para publicação, arquivamento e
diagnóstico de credenciais junto às plataformas **OSF**, **Zenodo** e **Zotero**.

---

## Pré-requisitos

1. Copie `.env.example` para `.env` e preencha as credenciais:
   ```bash
   cp .env.example .env
   ```
2. Instale as dependências (se ainda não tiver):
   ```bash
   pip install requests python-dotenv
   ```
3. **NUNCA** versione o arquivo `.env` — ele já está no `.gitignore`.

### Escopos necessários

| Serviço | Variável | Escopo / Permissão |
|---------|----------|-------------------|
| OSF | `OSF_TOKEN` | `osf.full_write` (leitura + escrita) |
| Zenodo | `ZENODO_TOKEN` | Acesso à API de depósitos |
| Zotero | `ZOTERO_API_KEY` + `ZOTERO_USER_ID` | Acesso de leitura ao library do usuário |

---

## `upload_osf.py`

Upload de arquivos e criação de pastas no **Open Science Framework (OSF)**.

### Funções principais

```python
from scripts.upload_osf import (
    get_osf_headers,
    get_node_info,
    upload_file_to_osf,
    list_osf_files,
    create_osf_folder,
)
```

### Uso via CLI

```bash
# Upload simples para a raiz do nó
python scripts/upload_osf.py --file outputs/figura.png

# Upload para uma subpasta
python scripts/upload_osf.py --file data/processados/tabela.csv --target-path dados/v2

# Criar pasta vazia
python scripts/upload_osf.py --create-folder nova_pasta --target-path dados

# Listar arquivos existentes no nó
python scripts/upload_osf.py --list

# Especificar outro nó (sobrescreve OSF_NODE_ID)
python scripts/upload_osf.py --file relatorio.pdf --node-id abc12
```

### Argumentos

| Flag | Descrição | Obrigatório |
|------|-----------|-------------|
| `--file` | Caminho local do arquivo | Sim (exceto com `--list`) |
| `--node-id` | ID do nó OSF | Não (padrão: `OSF_NODE_ID` do `.env`) |
| `--target-path` | Caminho relativo dentro do `osfstorage` | Não |
| `--create-folder` | Nome de uma pasta a ser criada | Não |
| `--list` | Lista arquivos do nó e sai | Flag |
| `-v, --verbose` | Ativa logging DEBUG | Flag |

---

## `upload_zenodo.py`

Criação de depósitos, upload de arquivos e publicação no **Zenodo** (com suporte a *sandbox*).

### Funções principais

```python
from scripts.upload_zenodo import (
    get_zenodo_api_url,
    create_deposition,
    upload_file_to_zenodo,
    publish_deposition,
    get_deposition,
)
```

### Uso via CLI

```bash
# Criar rascunho e fazer upload (não publica)
python scripts/upload_zenodo.py \
    --title "Dados da migração venezuelana no Oeste de SC" \
    --description "Conjunto de dados processados provenientes de RAIS, CAGED e DATASUS." \
    --file outputs/dados_finais.parquet

# Publicar imediatamente (gera DOI permanente)
python scripts/upload_zenodo.py \
    --title "Relatório técnico" \
    --description "Relatório de análise espacial e demográfica." \
    --file docs/relatorio.pdf \
    --publish

# Testar no sandbox
python scripts/upload_zenodo.py \
    --title "Teste sandbox" \
    --description "Descrição de teste." \
    --file data/amostra.csv \
    --sandbox \
    --publish

# Especificar creators via JSON
python scripts/upload_zenodo.py \
    --title "Artigo de dados" \
    --description "Descrição." \
    --file artigo.zip \
    --creators '[{"name": "Maria Silva", "affiliation": "UFSC", "orcid": "0000-0001-2345-6789"}]'
```

### Argumentos

| Flag | Descrição | Obrigatório |
|------|-----------|-------------|
| `--title` | Título do depósito | Sim |
| `--description` | Resumo / descrição | Sim |
| `--file` | Caminho local do arquivo | Sim |
| `--creators` | JSON com lista de autores | Não (padrão: projeto genérico) |
| `--publish` | Publica o depósito imediatamente | Flag |
| `--sandbox` | Usa `sandbox.zenodo.org` | Flag |
| `-v, --verbose` | Ativa logging DEBUG | Flag |

Ao publicar, o script imprime automaticamente o **DOI** e o **link de acesso**.

---

## `check_credentials.py`

Diagnóstico rápido que verifica se as credenciais de OSF, Zenodo e Zotero estão válidas.

### Uso

```bash
python scripts/check_credentials.py
```

### Saída esperada

```text
=== Verificação de Credenciais ===

  ✓ OSF — nó 'fna8v' — Raio X da Migração Venezuelana no Oeste de SC
  ✓ Zenodo — 3 depósito(s) visível(eis)
  ✓ Zotero — usuário OK (user_id=12345678)

Resumo: 3/3 serviços OK
✓Todas as credenciais estão funcionando corretamente.
```

Se alguma falhar, aparece `✗` com o código HTTP e uma sugestão para revisar o `.env`.

---

## Tratamento de erros

Todos os scripts:

- Usam `requests` com timeout configurado.
- Levantam `requests.HTTPError` para erros da API.
- Logam falhas de forma informativa.
- Retornam código de saída `1` em caso de erro e `0` em caso de sucesso.

---

## Notas de segurança

- **NUNCA** escreva tokens diretamente no código.
- **NUNCA** faça `git add .env`.
- Se um token vazar, revogue-o imediatamente no painel do serviço e gere um novo.
