import os
import time
import json
from google import genai
from google.genai.errors import ServerError, ClientError


class GeminiService:

    def __init__(self):

        self.client = genai.Client(
            api_key=os.getenv(
                "GEMINI_API_KEY"
            )
        )

        self.model = "gemini-3.1-flash-lite"

    def analyze(self, customer, description):

        prompt = f"""
Analiza esta oportunidad comercial.

Cliente:
{customer}

Descripción:
{description}


Devuelve solamente JSON válido.

Formato obligatorio:

{{
    "summary": "Resumen del análisis",
    "priority": "low|medium|high",
    "next_action": "Próximo paso recomendado"
}}

IMPORTANTE:
El campo priority debe contener únicamente:
low
medium
high

No uses:
Alta
Media
Baja
"""
   
        for attempt in range(3):

            try:

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )

                data = json.loads(response.text)

                return data

            except ServerError:

                time.sleep(5)

            except ClientError as e:

                raise Exception(
                    f"Gemini error: {e}"
                )

        raise Exception(
            "Gemini no disponible después de varios intentos"
        )