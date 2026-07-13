from odoo import models, fields
from odoo.exceptions import UserError

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

        for record in self:

            if not record.description:
                raise UserError(
                    "Debe ingresar una descripción antes de analizar."
                )

            # Temporalmente simularemos la IA
            result = {
                "summary": "Análisis generado por IA",
                "priority": "high",
                "next_action": "Contactar al cliente"
            }

            record.write({
                "ai_summary": result["summary"],
                "ai_priority": result["priority"],
                "next_action": result["next_action"],
                "state": "analyzed"
            })