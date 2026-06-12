import fitz

class PDFExtractor():
    def __init__(self , pdf_path:str ): ## ainda vou arrumar para pegar um arquivo pdf ao contrario de um diretorio

        self.pdf_path= pdf_path
        self.text  = ""
    

    def extract(self )-> str:

        pdf = fitz.open(self.pdf_path )

      

        for pagina in pdf:
            self.texto += pagina.get_text()
        
        pdf.close()
        return  self.texto,
    def total_caracteres(self)->int:
        return len(self.texto)

if __name__ == "__main__":
    pass
    
        