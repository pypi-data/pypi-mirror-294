# AiManagerToolkit 🤖

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![AzureOpenAI](https://img.shields.io/badge/Azure%20OpenAI-✔️-blue)
![OpenAI](https://img.shields.io/badge/OpenAI-✔️-brightgreen)

`AiManagerToolkit` es una librería Python diseñada para simplificar la interacción con las APIs de OpenAI y Azure OpenAI. Esta herramienta proporciona una forma flexible y eficiente de gestionar conversaciones con modelos de lenguaje, integrar herramientas personalizadas y generar respuestas estructuradas, ideal para desarrolladores que buscan aprovechar la potencia de la inteligencia artificial en sus aplicaciones.

## Características ✨

- **Soporte para OpenAI y Azure OpenAI:** Fácil integración con ambas plataformas.
- **Herramientas Personalizadas:** Define y registra herramientas para mejorar las interacciones con el modelo.
- **Salidas Estructuradas:** Genera respuestas en formato JSON basadas en esquemas definidos.
- **Chat Sincrónico y Asíncrono:** Manejo de conversaciones tanto en modo sincrónico como en streaming.
- **Logging Configurable:** Sistema de logging integrado para monitorear y depurar las interacciones.

## Instalación 🚀

Puedes instalar `AiManagerToolkit` desde PyPI utilizando pip:

```bash
pip install AiManagerToolkit
```

## Uso Básico 💻

### 1. Configuración Inicial 🛠️

Puedes configurar la conexión a las APIs de OpenAI o Azure OpenAI utilizando variables de entorno o parámetros en el código.

#### Configuración utilizando `.env` 🌐

Crea un archivo `.env` en el directorio raíz de tu proyecto con las credenciales necesarias:

```env
AZURE_OPENAI_MODEL=gpt-4o
AZURE_OPENAI_ENDPOINT=https://tu-endpoint.azure.com/
AZURE_OPENAI_API_KEY=tu-clave-api
AZURE_OPENAI_API_VERSION=2023-05-15
```

#### Configuración en el Código 🔧

Puedes pasar la configuración directamente en tu código:

```python
from AiManagerToolkit import AzureAiToolkit

# Inicializa la herramienta con configuración personalizada
azure_ai = AzureAiToolkit(
    model="gpt-4o",
    azure_endpoint="https://tu-endpoint.azure.com/",
    api_key="tu-clave-api",
    temperature=0.7
)
```

### 2. Ejemplo de Uso Sincrónico 🔄

```python
from AiManagerToolkit import AzureAiToolkit, user

# Inicializa la herramienta con la configuración predeterminada o personalizada
azure_ai = AzureAiToolkit()

# Crear un mensaje de usuario y obtener la respuesta
messages = [user("¿Cuál es el estado de mi pedido?")]
response = azure_ai.chat(messages)
print(response)
```

### 3. Ejemplo de Uso con Herramientas 🔧

```python
from AiManagerToolkit import Tool, Toolbox, AzureAiToolkit, user

# Definir una nueva herramienta
tool = Tool(
    name="get_weather",
    description="Obtén el clima para una ubicación dada",
    parameters={
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "Ubicación para el clima"},
            "unit": {"type": "string", "enum": ["C", "F"], "description": "Unidad de temperatura"}
        },
        "required": ["location", "unit"]
    },
    strict=True
)

# Registrar la herramienta
Toolbox.register_tool(tool)

# Usar la herramienta en una conversación
messages = [user("¿Cómo está el clima en Santiago?")]
azure_ai = AzureAiToolkit()
response = azure_ai.chat(messages, tools=Toolbox.get_tools())
print(response)
```

### 4. Logging Personalizado 📜

El sistema de logging integrado te permite personalizar el nivel de log y elegir si quieres guardar los logs en un archivo o solo en consola.

```python
from AiManagerToolkit import log

# Cambia el nivel de logging
log.setLevel("INFO")

# Loggea un mensaje
log.info("Este es un mensaje de información.")
```

## Contribuciones 👥

¡Las contribuciones son bienvenidas! Si deseas contribuir al proyecto, sigue estos pasos:

1. Realiza un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/mi-nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -am 'Añadir nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature/mi-nueva-funcionalidad`).
5. Crea un nuevo Pull Request.

## Roadmap 🛤️

- [ ] Integración con otras plataformas de IA.
- [ ] Mejoras en la documentación con ejemplos avanzados.
- [ ] Añadir más tests unitarios y de integración.
- [ ] Soporte para operaciones avanzadas con Azure OpenAI.

## Licencia 📄

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.

---

¡Gracias por usar `AiManagerToolkit`! Si tienes alguna pregunta o sugerencia, no dudes en abrir un issue en el repositorio. 😊
