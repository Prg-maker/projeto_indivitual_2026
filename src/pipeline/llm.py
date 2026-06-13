from pipeline.schema import Relatorio
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
UNIDADES = {
    "R$ milhões": "brl_milhoes",
    "milhões de USD": "usd_milhoes",
    "%": "percentual",
    "unidades": "unidades"
}

class FinancialExtractor:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
    def extract(self, chunk: str)->Relatorio:
        api_key = os.getenv("GEMINI_API_KEY")
        prompt = f"""
      Você é um extrator de indicadores financeiros.

Extraia SOMENTE indicadores financeiros e operacionais relevantes para análise empresarial.

Inclua apenas:
- geração de caixa
- receita
- lucro
- EBITDA
- vendas
- lançamentos
- VGV
- dívida
- ativos vendidos
- participação societária
- unidades produzidas
- unidades vendidas
- unidades locadas
- valores monetários
- percentuais operacionais

Ignore completamente:
- datas
- anos
- trimestres
- idade da empresa
- quantidade de estados
- quantidade de cidades
- quantidade de regiões
- quantidade de macrorregiões
- nomes de pessoas
- cargos
- e-mails
- websites
- textos institucionais
- informações de relações com investidores

Nunca inferir valores.

Nunca converter ausência de informação em zero.

Extraia apenas números explicitamente presentes no texto.

Retorne APENAS JSON válido.

Formato obrigatório:

{{
    "indicadores": [
        {{
            "nome": "nome_do_indicador",
            "valor": 0,
            "unidade": "unidade"
        }}
    ]
}}

Regras:
- Não utilize markdown.
- Não utilize ```json.
- Não escreva explicações.
- Não crie objetos aninhados.
- Não agrupe indicadores por empresa.
- Cada indicador deve ser um item da lista.
- O campo "valor" deve conter apenas números.
- O campo "unidade" deve conter apenas a unidade associada ao valor.

Texto para análise:

{chunk}
        """

        client = genai.Client(api_key=self.api_key)
        response = client.models.generate_content(
                
                model="gemini-3.5-flash",
                contents=prompt
        )

        if not response.text :
            raise ValueError(
                 "Gemini retornou resposta vazia"
            ) 
        json_text = (
            response.text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return Relatorio.model_validate_json(
            json_text
        )
    