import requests
import hashlib
import json
import os

URL = (
    "https://apicatalog.mziq.com/filemanager/company/"
    "4b56353d-d5d9-435f-bf63-dcbf0a6c25d5/"
    "filter/categories/year/meta"
)


CATEGORIAS = [
    "Earnings Release",
    "Prévia Operacional",
    "ITR/DFP",
    "Transcrição"
]



    # internal_name: 'central_de_resultados_release',
    #internal_name: 'central_de_resultados_previa',
    #internal_name: 'central_de_resultados_itr',
    #internal_name: 'central_de_resultados_planilha_interativa',
    #internal_name: 'central_de_resultados_audio',
    #internal_name: 'central_de_resultados_transcricao',
PAYLOAD = {
    "year": 2025,
    "categories": [
        "central_de_resultados_release"
    ],
    "language": "pt_BR",
    "published": True
}

ARQUIVO_HASHES = "documentos_processados.json"
PASTA_PDFS = "pdfs"


def carregar_hashes():
    try:
        with open(ARQUIVO_HASHES, "r") as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()


def salvar_hashes(hashes):
    with open(ARQUIVO_HASHES, "w") as f:
        json.dump(list(hashes), f, indent=2)


os.makedirs(PASTA_PDFS, exist_ok=True)

response = requests.post(URL, json=PAYLOAD)
response.raise_for_status()

dados = response.json()

documentos = dados["data"]["document_metas"]

hashes_processados = carregar_hashes()

for doc in documentos:

    pdf_url = doc["file_url"]

    print(f"Verificando: {doc['file_title']}")

    pdf_response = requests.get(pdf_url)
    pdf_response.raise_for_status()

    hash_doc = hashlib.sha256(pdf_response.content).hexdigest()

    if hash_doc in hashes_processados:
        print(f"Já processado: {doc['file_title']}")
        continue

    print(f"Novo documento encontrado: {doc['file_title']}")

    nome_arquivo = (
        f"{doc['file_year']}_T{doc['file_quarter']}_{hash_doc[:8]}.pdf"
    )

    caminho_arquivo = os.path.join(PASTA_PDFS, nome_arquivo)

    with open(caminho_arquivo, "wb") as f:
        f.write(pdf_response.content)

    print(f"PDF salvo em: {caminho_arquivo}")
    print(f"Hash: {hash_doc}")

    hashes_processados.add(hash_doc)

salvar_hashes(hashes_processados)

print("Monitoramento concluído.")