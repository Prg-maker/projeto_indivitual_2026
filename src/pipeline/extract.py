from PyPDF2 import PdfReader

class PDFExtractor:

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def extract(self):

        pdf = PdfReader(self.pdf_path)

        paginas = []

        for pagina in pdf.pages:
            paginas.append(
                pagina.extract_text()
            )

        return paginas