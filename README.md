## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

# AI Business Assistant

AI Business Assistant es un módulo personalizado para **Odoo 18** que integra **Google Gemini** para analizar oportunidades de negocio y generar recomendaciones comerciales mediante Inteligencia Artificial.

Este proyecto fue desarrollado como demostración técnica para mostrar conocimientos en desarrollo sobre Odoo, integración con APIs de IA y arquitectura modular en Python.

---

## Características

- Desarrollo de un módulo personalizado para Odoo 18.
- Modelo de negocio personalizado (`ai.analysis`).
- Vistas de lista y formulario.
- Acción personalizada mediante botón.
- Integración con Google Gemini API.
- Análisis automático de oportunidades comerciales.
- Generación de:
  - Resumen ejecutivo.
  - Nivel de prioridad.
  - Próxima acción recomendada.
- Arquitectura desacoplada mediante una capa de servicios.
- Variables de entorno para proteger credenciales.

---

## Tecnologías

- Odoo 18
- Python 3
- PostgreSQL
- Docker & Docker Compose
- Google Gemini API
- XML (vistas Odoo)

---

## Arquitectura

```text
Usuario
      │
      ▼
Formulario Odoo
      │
      ▼
Botón "Analizar con IA"
      │
      ▼
AIAnalysis (Modelo Odoo)
      │
      ▼
GeminiService
      │
      ▼
Google Gemini API
      │
      ▼
Respuesta JSON
      │
      ▼
Persistencia mediante ORM de Odoo
      │
      ▼
Visualización del resultado
```

---

## Capturas

### Formulario

> *(Agregar captura aquí)*

### Resultado del análisis

> *(Agregar captura aquí)*

---

## Instalación

### Clonar repositorio

```bash
git clone https://github.com/404Yato/ai_business_assistant.git
cd ai_business_assistant
```

### Levantar Docker

```bash
docker compose up -d
```

### Configurar la API Key

Crear un archivo `.env`:

```env
GEMINI_API_KEY=tu_api_key
```

### Instalar el módulo

1. Activar modo desarrollador.
2. Ir a **Apps**.
3. Actualizar lista de aplicaciones.
4. Instalar **AI Business Assistant**.

---

## Ejemplo de uso

Crear un nuevo análisis indicando:

- Cliente
- Descripción de la oportunidad

Luego presionar:

**Analizar con IA**

La IA generará automáticamente:

- Resumen ejecutivo
- Prioridad
- Próxima acción sugerida

---

## Estructura del proyecto

```text
ai_sales_assistant/

├── models/
│   └── analysis.py
│
├── services/
│   └── gemini_service.py
│
├── views/
│   └── views.xml
│
├── __manifest__.py
└── __init__.py
```

---

## Posibles mejoras

Este proyecto representa un MVP funcional. Algunas mejoras futuras podrían ser:

- [ ] Integración con el módulo CRM de Odoo.
- [ ] Soporte para múltiples proveedores de IA (OpenAI, Claude, Gemini).
- [ ] Configuración de API Keys desde Odoo.
- [ ] Historial de análisis realizados.
- [ ] Sistema de puntuación comercial.
- [ ] Registro de logs y monitoreo.
- [ ] Pruebas unitarias.

---

## Objetivo del proyecto

Este proyecto fue desarrollado como parte de mi portfolio para demostrar experiencia en:

- Desarrollo de módulos personalizados para Odoo.
- Integración con APIs externas.
- Arquitectura basada en servicios.
- Consumo de modelos de IA generativa.
- Desarrollo backend con Python.