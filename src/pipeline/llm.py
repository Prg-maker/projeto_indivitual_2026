from pipeline.schema import Relatorio
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()


class FinancialExtractor:
    """
    Classe auxiliar que extrai indicadores financeiros e operacionais de um trecho de texto
    usando o modelo Gemini (cliente genai). Encapsula construção do prompt, chamada ao modelo,
    validação básica da resposta e conversão para Relatorio.
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)

    def extract(self, chunk: str) -> Relatorio:
        prompt = f"""
            Você é um especialista em análise de relatórios financeiros de incorporadoras.

            Sua função é extrair apenas indicadores financeiros e operacionais explicitamente presentes no texto.
            Retorne a empresa utilizando apenas um dos nomes abaixo:

            - MRV
            - Direcional
            - Tenda
            - Cury
            - Plano&Plano

            Nunca utilize razão social completa.

            Para cada indicador, preencha obrigatoriamente o campo "trecho_origem".

            O campo deve conter a frase exata do documento de onde o valor foi extraído.

            Exemplo literal de indicador (apenas ilustrativo, mantenha o formato JSON):

            {{
                "nome": "ativos_vendidos",
                "descricao": "ativos já vendidos",
                "valor": 149,
                "unidade": "usd_milhoes",
                "pagina": 12,
                "trecho_origem": "Assets already sold totaled US$149 million."
            }}

            Nunca retorne null para trecho_origem.

            Indicadores permitidos:

            - receita
            - lucro_liquido
            - ebitda
            - geracao_caixa
            - vendas
            - lancamentos
            - vgv
            - divida
            Extraia "ativos_vendidos" somente quando o texto indicar explicitamente
            que a venda já ocorreu.

            Ignore:

            - potencial de venda;
            - pipeline de ativos;
            - ativos disponíveis para venda;
            - expectativa de venda;
            - ativos em negociação.

            - participacao_societaria
            - unidades_produzidas
            - unidades_vendidas
            - unidades_locadas

            Não extraia nenhum outro indicador.

            Ignore completamente:

            - gráficos
            - textos institucionais
            - nomes de executivos
            - cargos
            - e-mails
            - websites
            - frases de marketing
            - comparações entre períodos
            - crescimento YoY
            - crescimento QoQ
            - variações percentuais
            - rankings
            - quantidade de cidades
            - quantidade de estados
            - quantidade de regiões

            Regras:

            - Nunca inferir valores.
            - Nunca converter ausência de informação em zero.
            - Extraia somente números explicitamente presentes.
            - Se o indicador não existir, não o inclua.
            - Não invente indicadores.

            As unidades permitidas são:

            - brl_milhoes
            - usd_milhoes
            - percentual
            - unidades

            Para indicadores repetidos, utilize o campo "descricao" para diferenciá-los.
            O campo descrição deve ser curto (máximo 10 palavras) e identificar
            somente o contexto do indicador.

            Exemplo:

            {{
                "nome": "geracao_caixa",
                "descricao": "geração de caixa consolidada",
                "valor": 278.4,
                "unidade": "brl_milhoes"
            }}

            Extraia também:

            - empresa
            - ano
            - trimestre

            O trimestre deve ser:

            1, 2, 3 ou 4.

            Caso alguma informação não esteja explicitamente presente, retorne null.

            Retorne APENAS JSON válido no seguinte formato:

            {{
                "empresa": null,
                "ano": null,
                "trimestre": null,
                "indicadores": [
                    {{
                        "nome": "",
                        "descricao": "",
                        "valor": 0,
                        "unidade": "",
                        "pagina": null,
                        "trecho_origem": ""
                    }}
                ]
            }}

            Texto:

            {chunk}
            """

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )

        if not getattr(response, "text", None):
            raise ValueError("Gemini retornou resposta vazia")

        return Relatorio.model_validate_json(response.text)
