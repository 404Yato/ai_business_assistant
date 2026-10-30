
import json
import logging
import os
import subprocess

from odoo import models, fields
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


PRIORITY_MAP = {
    "alta": "high",
    "media": "medium",
    "baja": "low",
    "high": "high",
    "medium": "medium",
    "low": "low",
}


class AIAnalysis(models.Model):
    _name = "ai.analysis"
    _description = "AI Business Analysis"
    _rec_name = "name"

    name = fields.Char(
        string="Título",
        required=True
    )

    customer = fields.Char(
        string="Cliente"
    )

    description = fields.Text(
        string="Descripción"
    )

    ai_summary = fields.Text(
        string="Resumen IA",
        readonly=True
    )

    ai_priority = fields.Selection(
        [
            ("low", "Baja"),
            ("medium", "Media"),
            ("high", "Alta"),
        ],
        string="Prioridad IA",
        readonly=True,
    )

    next_action = fields.Text(
        string="Próxima acción sugerida",
        readonly=True,
    )

    state = fields.Selection(
        [
            ("draft", "Borrador"),
            ("analyzed", "Analizado"),
        ],
        default="draft",
        string="Estado",
    )

    def action_analyze_with_ai(self):

        worker = (
            "/mnt/extra-addons/"
            "ai_analysis/services/gemini_worker.py"
        )

        python = "/opt/gemini-env/bin/python"

        for record in self:

            if not record.description or not record.description.strip():
                raise UserError(
                    "Debes ingresar una descripción antes de analizar."
                )

            try:
                process = subprocess.run(
                    [
                        python,
                        worker,
                        record.customer or "",
                        record.description,
                    ],
                    capture_output=True,
                    text=True,
                    env=os.environ.copy(),
                    timeout=90,
                    check=False,
                )

            except subprocess.TimeoutExpired:
                _logger.warning(
                    "Timeout al analizar el registro %s",
                    record.id,
                )
                raise UserError(
                    "El análisis excedió el tiempo máximo permitido. "
                    "Intenta nuevamente más tarde."
                )

            except OSError:
                _logger.exception(
                    "No se pudo ejecutar el worker de Gemini."
                )
                raise UserError(
                    "No fue posible iniciar el servicio de inteligencia artificial."
                )

            if process.returncode != 0:
                _logger.error(
                    "Worker Gemini falló. Registro: %s. Error: %s",
                    record.id,
                    process.stderr,
                )

                raise UserError(
                    "No fue posible completar el análisis con IA. "
                    "Revisa la configuración del servicio e intenta nuevamente."
                )

            try:
                result = json.loads(process.stdout)

            except (json.JSONDecodeError, TypeError):
                _logger.error(
                    "Respuesta JSON inválida del worker. Registro: %s",
                    record.id,
                )
                raise UserError(
                    "El servicio de IA devolvió una respuesta inválida."
                )

            if not isinstance(result, dict):
                raise UserError(
                    "La respuesta de IA tiene un formato incorrecto."
                )

            summary = result.get("summary")
            priority = result.get("priority")
            next_action = result.get("next_action")

            if not all(
                isinstance(value, str) and value.strip()
                for value in (summary, priority, next_action)
            ):
                raise UserError(
                    "La respuesta de IA está incompleta."
                )

            priority = PRIORITY_MAP.get(priority.strip().lower())

            if priority is None:
                raise UserError(
                    "La IA devolvió una prioridad no reconocida."
                )

            record.write(
                {
                    "ai_summary": summary.strip(),
                    "ai_priority": priority,
                    "next_action": next_action.strip(),
                    "state": "analyzed",
                }
            )
