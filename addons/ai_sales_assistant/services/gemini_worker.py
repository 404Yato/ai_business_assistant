import os
import sys
import json
import time

from google import genai
from google.genai.errors import ServerError, ClientError


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


customer = sys.argv[1]
description = sys.argv[2]


prompt = f"""
Eres un analista comercial experto.

Analiza la siguiente oportunidad de negocio.

Cliente:
{customer}

Descripción:
{description}

Devuelve únicamente un JSON válido con este formato:

{{
    "summary": "Resumen ejecutivo",
    "priority": "high",
    "next_action": "Próximo paso recomendado"
}}

No escribas texto adicional.
No utilices markdown.
No uses ```json.
"""


try:

    for intento in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt,
            )

            text = response.text.strip()

            if text.startswith("```"):
                text = (
                    text.replace("```json", "")
                    .replace("```", "")
                    .strip()
                )

            print(text)
            sys.exit(0)

        except ServerError:

            if intento < 2:
                time.sleep(5)
                continue

            print(
                json.dumps(
                    {
                        "summary": "Gemini no respondió por saturación.",
                        "priority": "medium",
                        "next_action": "Intentar nuevamente más tarde.",
                    }
                )
            )
            sys.exit(1)

        except ClientError as e:

            print(
                json.dumps(
                    {
                        "summary": f"Error de API: {str(e)}",
                        "priority": "medium",
                        "next_action": "Revisar la API Key o la cuota disponible.",
                    }
                )
            )
            sys.exit(1)

except Exception as e:

    print(
        json.dumps(
            {
                "summary": f"Error inesperado: {str(e)}",
                "priority": "medium",
                "next_action": "Revisar logs del worker.",
            }
        )
    )

    sys.exit(1)