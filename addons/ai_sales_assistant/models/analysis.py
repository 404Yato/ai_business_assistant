from odoo import models, fields
from odoo.exceptions import UserError
from ..services.gemini_service import GeminiService

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
            ('low', 'Baja'),
            ('medium', 'Media'),
            ('high', 'Alta'),
        ],
        string="Prioridad IA",
        readonly=True
    )

    next_action = fields.Text(
        string="Próxima acción sugerida",
        readonly=True
    )   

    state = fields.Selection(
        [
            ('draft', 'Borrador'),
            ('analyzed', 'Analizado'),
        ],
        string="Estado",
        default="draft"
    )

    def action_analyze_with_ai(self):

        service = GeminiService()

        for record in self:

            result = service.analyze(
                record.customer,
                record.description
            )

            priority = result.get("priority", "").lower()

            priority = priority_map.get(
                priority,
                "medium"
            )

            record.write({

                "ai_summary": result.get("summary"),

                "ai_priority": priority,

                "next_action": result.get("next_action"),

                "state": "analyzed"

            })