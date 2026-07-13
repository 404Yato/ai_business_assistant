import os
import json

from openai import OpenAI


class AIService:

    def __init__(self):

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise Exception(
                "OPENAI_API_KEY no configurada"
            )

        self.client = OpenAI(
            api_key=api_key
        )


    def analyze(self, customer, description):

        prompt = f"""
Analiza esta oportunidad comercial.

Cliente:
{customer}

Descripción:
{description}

Responde únicamente con JSON válido.

Formato obligatorio:

{{
    "summary": "Resumen del análisis",
    "priority": "low|medium|high",
    "next_action": "Próxima acción recomendada"
}}
"""

        response = self.client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        content = response.output_text

        return json.loads(content)