## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

# CMTS AI Business Assistant 🤖

Sistema de análisis empresarial asistido por inteligencia artificial desarrollado sobre **Odoo 18**, integrando un módulo personalizado capaz de analizar solicitudes de clientes mediante **Google Gemini AI** y generar recomendaciones automáticas de prioridad, resumen y próximas acciones.

El objetivo del proyecto es demostrar la integración entre un ERP empresarial, desarrollo de módulos personalizados, inteligencia artificial generativa y despliegue cloud.

La arquitectura fue diseñada para ser extensible, permitiendo incorporar diferentes proveedores de inteligencia artificial mediante servicios adicionales sin modificar la lógica principal del sistema.

---

# 🚀 Demo

Aplicación desplegada:

🔗 **Demo:** https://cmts-ai-business-assistant.up.railway.app/

## Usuario Demo

Para explorar la aplicación:

```
Usuario:
demo

Contraseña:
demo123
```

> El usuario demo está creado únicamente para pruebas y visualización de funcionalidades.

---

# 📸 Capturas de la aplicación

## Pantalla principal

<img width="1861" height="510" alt="image" src="https://github.com/user-attachments/assets/b67481a2-71b5-476b-9cbe-e3500a9b901e" />

---

## Creación de análisis empresarial

La aplicación permite registrar nuevos casos ingresando:

- Título del análisis.
- Cliente asociado.
- Descripción del problema o necesidad.

Ejemplo:

> Cliente necesita reemplazar su sistema actual de inventario porque presenta errores frecuentes.

<img width="1863" height="326" alt="image" src="https://github.com/user-attachments/assets/53d151f0-ddd4-44c3-b654-da117c2855bd" />

---

## Resultado generado por Inteligencia Artificial

Luego del análisis, Gemini genera automáticamente:

- Resumen del caso.
- Nivel de prioridad.
- Próxima acción recomendada.

<img width="1867" height="578" alt="image" src="https://github.com/user-attachments/assets/a580ae8c-4ad1-4fda-872c-f12a6066c48c" />

---

# 🧠 Funcionamiento

El flujo general de la aplicación es:

```
Usuario
   |
   v
Formulario Odoo
   |
   v
Módulo personalizado AI Analysis
   |
   v
Capa de servicios de Inteligencia Artificial
   |
   v
Proveedor IA configurado
(Gemini, OpenAI, Claude, modelos propios, etc.)
   |
   v
Respuesta estructurada JSON
   |
   v
Actualización automática del registro
```

La aplicación separa la lógica del negocio de la integración con inteligencia artificial.

Esto permite cambiar o agregar proveedores de IA sin modificar los modelos, vistas o procesos internos del módulo Odoo.

---

# 🏗️ Arquitectura

## Tecnologías utilizadas

### ERP / Backend

- Odoo 18
- Python
- ORM de Odoo
- Módulos personalizados

### Inteligencia Artificial

- Google Gemini API.
- Google GenAI SDK.
- Procesamiento de lenguaje natural.
- Arquitectura extensible para múltiples proveedores IA.

### Base de datos

- PostgreSQL 17

### Infraestructura

- Docker
- Railway
- PostgreSQL administrado
- Variables de entorno

---

# 🤖 Arquitectura extensible de Inteligencia Artificial

La integración fue diseñada utilizando una capa de servicios independiente.

Actualmente el sistema utiliza **Google Gemini AI**, pero la arquitectura permite incorporar nuevos modelos de inteligencia artificial mediante servicios adicionales.

Por ejemplo, podría integrarse:

- Google Gemini.
- OpenAI GPT.
- Anthropic Claude.
- Modelos locales mediante API propia.
- Cualquier proveedor compatible con respuestas estructuradas.

Para agregar una nueva inteligencia artificial solamente sería necesario crear un nuevo servicio encargado de comunicarse con dicho proveedor manteniendo la misma estructura esperada.

Esto permite mantener independiente:

- La lógica empresarial.
- Los modelos de datos de Odoo.
- Las vistas del módulo.
- Los procesos internos.

De esta forma, el sistema no queda acoplado a un único proveedor de IA y puede evolucionar fácilmente según las necesidades del negocio.

---

# 📂 Estructura del proyecto

```
.
├── addons/
│   └── ai_analysis/
│       ├── models/
│       │   └── analysis.py
│       ├── services/
│       │   └── gemini_worker.py
│       ├── views/
│       └── __manifest__.py
│
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── requirements.txt
└── README.md
```

---

# 🔎 Módulo AI Analysis

El módulo agrega un nuevo modelo dentro de Odoo:

```
ai.analysis
```

Este modelo permite almacenar análisis empresariales generados por usuarios y enriquecidos mediante inteligencia artificial.

## Campos principales

| Campo | Descripción |
|---|---|
| Nombre | Título del análisis |
| Cliente | Cliente asociado al caso |
| Descripción | Contexto del problema |
| Resumen IA | Resumen generado por inteligencia artificial |
| Prioridad IA | Nivel de prioridad detectado |
| Próxima acción | Recomendación generada |
| Estado | Estado actual del análisis |

---

# 🤖 Integración con Gemini

El módulo utiliza una capa de servicios para comunicarse con modelos de inteligencia artificial.

Actualmente la implementación utiliza **Google Gemini API**.

El módulo envía la información del caso:

```json
{
  "customer": "Cliente ejemplo",
  "description": "Descripción del problema"
}
```

Gemini procesa la información y responde con una estructura definida:

```json
{
  "summary": "Resumen generado por IA",
  "priority": "high",
  "next_action": "Contactar cliente y evaluar solución"
}
```

La respuesta es procesada automáticamente y almacenada dentro del registro de Odoo.

---

# 🐳 Ejecución local

## Requisitos

- Docker
- Docker Compose
- API Key de Gemini

---

## Variables de entorno

Crear archivo:

```
.env
```

Ejemplo:

```env
PGHOST=localhost
PGPORT=5432
PGUSER=odoo
PGPASSWORD=password
PGDATABASE=odoo

GEMINI_API_KEY=tu_api_key
```

---

## Levantar aplicación

Ejecutar:

```bash
docker compose up --build
```

La aplicación estará disponible en:

```
http://localhost:8069
```

---

# ☁️ Deploy

La aplicación está preparada para despliegue mediante contenedores Docker.

Configuración utilizada:

- Contenedor Odoo personalizado.
- PostgreSQL externo administrado.
- Variables de entorno para credenciales.
- Script de inicialización automático.
- Integración con servicios cloud.

Actualmente desplegada utilizando:

- Railway como plataforma de hosting.
- Railway PostgreSQL como base de datos.

---

# 🔐 Seguridad

Buenas prácticas aplicadas:

- Credenciales almacenadas mediante variables de entorno.
- API Key de Gemini protegida.
- Separación entre aplicación y base de datos.
- Separación de usuarios y permisos.
- Configuración preparada para ambientes productivos.

---

# 📚 Aprendizajes del proyecto

Durante el desarrollo se trabajaron conceptos como:

- Creación de módulos personalizados en Odoo.
- Desarrollo utilizando ORM de Odoo.
- Integración con APIs de inteligencia artificial.
- Diseño de servicios desacoplados.
- Arquitectura preparada para múltiples proveedores IA.
- Dockerización de aplicaciones empresariales.
- Configuración de PostgreSQL en entornos cloud.
- Deploy utilizando infraestructura administrada.
- Manejo de variables de entorno.
- Automatización del primer arranque de la aplicación.

---

# 👨‍💻 Autor

## Cristian Tapia Suárez

Desarrollador Full Stack enfocado en:

- Python
- Django
- SQL
- Desarrollo Backend
- Integración de Inteligencia Artificial

---

⭐ Proyecto desarrollado como demostración de integración entre ERP, inteligencia artificial y despliegue cloud.
