from pydantic import BaseModel

class Indicador(BaseModel):
    nome: str
    valor: float
    unidade: str


class Relatorio(BaseModel):
    indicadores: list[Indicador]