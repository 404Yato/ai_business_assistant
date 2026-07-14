from odoo import models, fields
from odoo.exceptions import UserError

import subprocess
import json
import os


priority_map = {
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

        worker = "/mnt/extra-addons/ai_sales_assistant/services/gemini_worker.py"
        python = "/opt/gemini-env/bin/python"

        for record in self:

            process = subprocess.run(
                [
                    python,
                    worker,
                    record.customer or "",
                    record.description or "",
                ],
                capture_output=True,
                text=True,
                env=os.environ,
            )

            if process.returncode != 0:
                raise UserError(process.stderr)

            try:
                result = json.loads(process.stdout)

            except Exception:
                raise UserError(
                    f"No se pudo interpretar la respuesta de Gemini:\n\n{process.stdout}"
                )

            priority = priority_map.get(
                result.get("priority", "").lower(),
                "medium",
            )

            record.write(
                {
                    "ai_summary": result.get("summary"),
                    "ai_priority": priority,
                    "next_action": result.get("next_action"),
                    "state": "analyzed",
                }
            )