from pydantic import BaseModel
from typing import Literal


class Indicador(BaseModel):

    nome: Literal[
        "receita",
        "lucro_liquido",
        "ebitda",
        "geracao_caixa",
        "vendas",
        "lancamentos",
        "vgv",
        "divida",
        "ativos_vendidos",
        "participacao_societaria",
        "unidades_produzidas",
        "unidades_vendidas",
        "unidades_locadas"
    ]

    descricao: str | None = None
    valor: float

    unidade: Literal[
        "brl_milhoes",
        "usd_milhoes",
        "percentual",
        "unidades"
    ]

    pagina: int | None = None
    trecho_origem: str 

class Relatorio(BaseModel):

    empresa: str | None = None

    ano: int | None = None

    trimestre: int | None = None

    indicadores: list[Indicador]