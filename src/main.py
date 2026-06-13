from ingeston.monitor import MRVMonitor
from pipeline.extract import PDFExtractor
from pipeline.chunk import Chunker
from pipeline.llm import FinancialExtractor

result = PDFExtractor(
    pdf_path= "pdfs/2025_T4_2f9106c8.pdf"
)

texto = result.extract()

chunk = Chunker(max_chars=3000)
chunks = chunk.chunk(paginas=texto )


extractor = FinancialExtractor()

for c in chunks:
    relatorio = extractor.extract(c)
    print(relatorio)
