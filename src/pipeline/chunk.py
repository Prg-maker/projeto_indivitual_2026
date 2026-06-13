class Chunker:

    def __init__(self, max_chars: int = 3000):
        self.max_chars = max_chars

    def chunk(self, paginas: list[str]) -> list[str]:
        
        chunks = []
        chunk_atual = ""
        for pagina in paginas:
            if len(chunk_atual) + len(pagina) > self.max_chars:
                chunks.append(
                    chunk_atual
                )
                chunk_atual = pagina
            else:
                chunk_atual += pagina
        chunks.append(chunk_atual)

        return chunks