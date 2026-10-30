
import json
import os
import sys
import time

from google import genai
from google.genai.errors import ServerError, ClientError


def validate_response(data):
    """
    Comprueba que Gemini haya devuelto
    los campos necesarios para el análisis.
    """

    if not isinstance(data, dict):
        raise ValueError("La respuesta no es un objeto JSON.")

    required_fields = [
        "summary",
        "priority",
        "next_action",
    ]

    for field in required_fields:
        value = data.get(field)

        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"Campo inválido o ausente: {field}"
            )

    valid_priorities = {
        "high",
        "medium",
        "low",
        "alta",
        "media",
        "baja",
    }

    priority = data["priority"].strip().lower()

    if priority not in valid_priorities:
        raise ValueError("Prioridad no reconocida.")

    data["priority"] = priority

    return data


def main():

    if len(sys.argv) < 3:
        raise ValueError(
            "Faltan argumentos para ejecutar el análisis."
        )

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "No se encontró GEMINI_API_KEY."
        )

    customer = sys.argv[1]
    description = sys.argv[2]

    client = genai.Client(api_key=api_key)

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

La prioridad debe ser exclusivamente:
- high
- medium
- low

No escribas texto adicional.
No utilices markdown.
No uses bloques de código.
"""

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt,
            )

            response_text = response.text

            if not response_text:
                raise ValueError(
                    "Gemini devolvió una respuesta vacía."
                )

            # Compatibilidad con respuestas que incluyan
            # accidentalmente bloques Markdown.
            response_text = response_text.strip()

            if response_text.startswith("```"):
                response_text = (
                    response_text
                    .removeprefix("```json")
                    .removeprefix("```")
                    .removesuffix("```")
                    .strip()
                )

            result = json.loads(response_text)

            result = validate_response(result)

            # stdout se reserva exclusivamente
            # para respuestas JSON exitosas.
            print(
                json.dumps(
                    result,
                    ensure_ascii=False
                )
            )

            return 0

        except ServerError:

            if attempt < 2:
                time.sleep(5)
                continue

            raise RuntimeError(
                "Gemini no respondió después de varios intentos."
            )

        except ClientError:
            raise RuntimeError(
                "La API de Gemini rechazó la solicitud. "
                "Revisa la API Key y la cuota disponible."
            )

    return 1


if __name__ == "__main__":

    try:
        exit_code = main()
        sys.exit(exit_code)

    except Exception as error:

        # Los errores se escriben en stderr,
        # nunca como respuestas JSON exitosas.
        print(
            f"Error en Gemini Worker: {error}",
            file=sys.stderr
        )

        sys.exit(1)
