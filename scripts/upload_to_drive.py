#!/usr/bin/env python3
"""Upload de arquivos para Google Drive via OAuth 2.0.

ATENÇÃO: A API do Google Drive NÃO suporta API Keys para upload.
É necessário um OAuth 2.0 access token. Siga as instruções abaixo:

1. Acesse https://console.cloud.google.com/
2. Crie um projeto (ou use um existente)
3. Ative a API Google Drive: https://console.cloud.google.com/apis/library/drive.googleapis.com
4. Crie credenciais OAuth 2.0 (tipo "Desktop app"): https://console.cloud.google.com/apis/credentials
5. Baixe o arquivo JSON de credenciais (client_secrets.json)
6. Execute este script uma vez para autorizar — ele abrirá o navegador para login Google
7. O token será salvo em token.json para uso futuro

Uso:
    python scripts/upload_to_drive.py --file data/processed/painel_oeste_sc_2018_2023.parquet --folder "migracao-venezuelana-sc"
"""

import argparse
import os
import pickle
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Escopos necessários para upload
SCOPES = ["https://www.googleapis.com/auth/drive"]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TOKEN_PATH = PROJECT_ROOT / "token.json"
CREDENTIALS_PATH = PROJECT_ROOT / "client_secrets.json"


def authenticate():
    """Autentica via OAuth 2.0 e retorna serviço do Drive."""
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_PATH.exists():
                raise FileNotFoundError(
                    f"Credenciais não encontradas: {CREDENTIALS_PATH}\n"
                    "Siga as instruções no topo deste script para criar client_secrets.json"
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    
    return build("drive", "v3", credentials=creds)


def find_or_create_folder(service, folder_name):
    """Encontra ou cria uma pasta no Drive."""
    query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and trashed=false"
    results = service.files().list(q=query, spaces="drive", fields="files(id, name)").execute()
    items = results.get("files", [])
    
    if items:
        return items[0]["id"]
    
    metadata = {"name": folder_name, "mimeType": "application/vnd.google-apps.folder"}
    folder = service.files().create(body=metadata, fields="id").execute()
    return folder["id"]


def upload_file(service, file_path, folder_id=None):
    """Faz upload de um arquivo para o Drive."""
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    
    metadata = {"name": file_path.name}
    if folder_id:
        metadata["parents"] = [folder_id]
    
    media = MediaFileUpload(str(file_path), resumable=True)
    file = service.files().create(body=metadata, media_body=media, fields="id, name, webViewLink").execute()
    
    print(f"✓ Upload concluído: {file['name']}")
    print(f"  ID: {file['id']}")
    print(f"  Link: {file.get('webViewLink', 'N/A')}")
    return file


def main():
    parser = argparse.ArgumentParser(description="Upload para Google Drive via OAuth 2.0")
    parser.add_argument("--file", type=Path, required=True, help="Arquivo local para upload")
    parser.add_argument("--folder", type=str, default="migracao-venezuelana-sc", help="Nome da pasta no Drive")
    args = parser.parse_args()
    
    print("Autenticando com Google Drive...")
    service = authenticate()
    
    print(f"Verificando pasta '{args.folder}'...")
    folder_id = find_or_create_folder(service, args.folder)
    
    print(f"Enviando {args.file.name}...")
    upload_file(service, args.file, folder_id)


if __name__ == "__main__":
    main()
