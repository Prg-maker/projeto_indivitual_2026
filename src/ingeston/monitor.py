import requests
import hashlib
import json
import os


class MRVMonitor:

    URL = (
        "https://apicatalog.mziq.com/filemanager/company/"
        "4b56353d-d5d9-435f-bf63-dcbf0a6c25d5/"
        "filter/categories/year/meta"
    )

    ARQUIVO_HASHES = "documentos_processados.json"
    PASTA_PDFS = "pdfs"
    CATEGORIAS = [
        "central_de_resultados_release",
        "central_de_resultados_previa",
        "central_de_resultados_itr",
        "central_de_resultados_planilha_interativa",
        "central_de_resultados_transcricao"
    ]
    def __init__(self, ano:int = 2026, categoria: str ="central_de_resultados_previa"):
        self.ano = ano
        if categoria not in self.CATEGORIAS:
            raise ValueError(
                f"Categoria inválida: {categoria}\n"
                f"Categorias disponíveis: {self.CATEGORIAS}"
            )
        if ano < 2015 :
            raise ValueError(
                f"Ano inválida"
            ) 

        self.payload = {
            "year": ano,
            "categories": [
                categoria
            ],
            "language": "pt_BR",
            "published": True
        }

        os.makedirs(self.PASTA_PDFS, exist_ok=True)

    def carregar_hashes(self):
        try:
            with open(self.ARQUIVO_HASHES, "r") as f:
                return set(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            return set()

    def salvar_hashes(self, hashes):
        with open(self.ARQUIVO_HASHES, "w") as f:
            json.dump(list(hashes), f, indent=2)

    def buscar_documentos(self):
        response = requests.post(
            self.URL,
            json=self.payload
        )

        response.raise_for_status()

        dados = response.json()

        return dados["data"]["document_metas"]

    def baixar_documento(self, doc):

        pdf_url = doc["file_url"]

        pdf_response = requests.get(pdf_url)
        pdf_response.raise_for_status()

        return pdf_response.content

    def gerar_hash(self, conteudo_pdf):
        return hashlib.sha256(conteudo_pdf).hexdigest()

    def salvar_pdf(self, doc, conteudo_pdf, hash_doc):

        nome_arquivo = (
            f"{doc['file_year']}_"
            f"T{doc['file_quarter']}_"
            f"{hash_doc[:8]}.pdf"
        )

        caminho = os.path.join(
            self.PASTA_PDFS,
            nome_arquivo
        )

        with open(caminho, "wb") as f:
            f.write(conteudo_pdf)

        return caminho

    def executar(self):

        hashes_processados = self.carregar_hashes()

        documentos = self.buscar_documentos()

        print(f"Encontrados {len(documentos)} documentos")

        for doc in documentos:

            print(
                f"Verificando: "
                f"{doc['file_title']}"
            )

            conteudo_pdf = self.baixar_documento(doc)

            hash_doc = self.gerar_hash(
                conteudo_pdf
            )

            if hash_doc in hashes_processados:
                print(
                    f"Já processado: "
                    f"{doc['file_title']}"
                )
                continue

            print(
                f"Novo documento encontrado: "
                f"{doc['file_title']}"
            )

            caminho = self.salvar_pdf(
                doc,
                conteudo_pdf,
                hash_doc
            )

            print(f"PDF salvo em: {caminho}")

            hashes_processados.add(hash_doc)

        self.salvar_hashes(
            hashes_processados
        )

        print("Monitoramento concluído.")


if __name__ == "__main__":

    monitor = MRVMonitor(
        ano=2026,
        categoria="central_de_resultados_previa"
    )

    monitor.executar()