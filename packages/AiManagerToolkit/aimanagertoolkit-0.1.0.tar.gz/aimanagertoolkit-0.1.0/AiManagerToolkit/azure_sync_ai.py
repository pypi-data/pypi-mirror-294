####################################################
# Importaciones y configuraciones centralizadas
####################################################

import os
from openai import AzureOpenAI, AsyncAzureOpenAI
from pydantic import BaseModel
from .log import log
from dotenv import load_dotenv

# Carga las variables de entorno desde un archivo .env
load_dotenv(override=True)

####################################################
# Clase Azure AI Toolkit (Versión Síncrona)
####################################################

class AzureAiToolkit:
    def __init__(self, 
                 model=None, 
                 azure_endpoint=None, 
                 azure_deployment=None,
                 api_key=None, 
                 api_version=None, 
                 temperature=None, 
                 max_tokens=None,
                 response_format=None,
                 tools=None,
                 tool_choice=None,
                 ):
        """
        Inicializa una instancia de AzureAiToolkit para manejar interacciones con Azure OpenAI.

        Parámetros:
        - model (str): El modelo de Azure OpenAI a utilizar. Si no se especifica, se obtiene de la variable de entorno 'AZURE_OPENAI_MODEL'.
        - azure_endpoint (str): El endpoint de Azure OpenAI. Si no se especifica, se obtiene de la variable de entorno 'AZURE_OPENAI_ENDPOINT'.
        - api_key (str): La clave API para autenticar las solicitudes a Azure OpenAI. Si no se especifica, se obtiene de la variable de entorno 'AZURE_OPENAI_API_KEY'.
        - api_version (str): La versión de la API de Azure OpenAI. Si no se especifica, se obtiene de la variable de entorno 'AZURE_OPENAI_API_VERSION'.
        - temperature (float): Parámetro que controla la aleatoriedad de las respuestas. Valores más bajos dan respuestas más conservadoras.
        - max_tokens (int): El número máximo de tokens a generar en la respuesta.
        - response_format (str): Formato de la respuesta (puede ser 'json', 'json_schema', 'text', etc.).
        - tools (list): Herramientas adicionales que se pueden usar en el proceso.
        - tool_choice (str): La herramienta seleccionada para esta solicitud específica.
        """
        self.model = model or os.getenv("AZURE_OPENAI_MODEL")
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = AzureOpenAI(
            azure_endpoint=azure_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=api_key or os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=api_version or os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_deployment=azure_deployment or os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        )
        self.async_client = AsyncAzureOpenAI(
            azure_endpoint=azure_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=api_key or os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=api_version or os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_deployment=azure_deployment or os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        )
        self.response_format = response_format
        self.tools = tools
        self.tool_choice = tool_choice


    ####################################################
    # Chat Sincrónico (Respuesta Completa)
    ####################################################
    
    def chat(self,
             messages,
             temperature=None,
             tools=None,
             response_format=None):
        """
        Crea completaciones de chat utilizando la API de Azure OpenAI con parámetros opcionales especificados durante la inicialización.

        Args:
            messages (list of dict): Una lista de diccionarios que representan el historial de conversación.
            temperature (float, opcional): Controla la aleatoriedad de las respuestas. Si no se especifica, se utiliza la temperatura definida en la inicialización.
            tools (list, opcional): Una lista de herramientas a utilizar en la llamada a la API. Si no se especifica, se utilizan las herramientas definidas en la inicialización.
            response_format (dict, opcional): El formato de la respuesta. Si se proporciona, este formato será utilizado. Si no se especifica, se utiliza el formato definido en la inicialización. Puede ser None.

        Returns:
            dict: La respuesta de la API de Azure OpenAI que contiene la completación del chat. Devuelve None en caso de error.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=self.max_tokens,
                response_format=response_format or self.response_format,
                stream=False,
                tools=tools or self.tools,
                tool_choice=self.tool_choice if (tools or self.tools) else None,

            )
            return response
        except Exception as e:
            log.error(f"Ocurrió un error: {e}")
            return None

    ####################################################
    # Chat Sincrónico (Streaming)
    ####################################################

    def stream(self,
                messages,
                temperature=None,
                tools=None,
                response_format=None
                ):
        """
        Crea completaciones de chat utilizando la API de Azure OpenAI con respuesta por streaming.

        Args:
            messages (list of dict): Una lista de diccionarios que representan el historial de conversación.
            temperature (float, opcional): Controla la aleatoriedad de las respuestas. Si no se especifica, se utiliza la temperatura definida en la inicialización.
            tools (list, opcional): Una lista de herramientas a utilizar en la llamada a la API. Si no se especifica, se utilizan las herramientas definidas en la inicialización.
            response_format (dict, opcional): El formato de la respuesta. Si se proporciona, este formato será utilizado. Si no se especifica, se utiliza el formato definido en la inicialización. Puede ser None.

        Returns:
            None: Imprime las respuestas de la API de Azure OpenAI a medida que se reciben.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=self.max_tokens,
                response_format=response_format or self.response_format,
                stream=True,
                tools=tools or self.tools,
                tool_choice=self.tool_choice if (tools or self.tools) else None,
            )

            for chunk in response:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    print(chunk.choices[0].delta.content, end="")

        except Exception as e:
            log.error(f"Ocurrió un error: {e}")
            return None

    ####################################################
    # Chat Sincrónico (Formato Estructurado)
    ####################################################
    
    def str_output(self, messages, schema, temperature=None):
        """
        Crea completaciones de chat utilizando la API de Azure OpenAI con salida estructurada según un JSON Schema.

        Args:
            messages (list of dict): Una lista de diccionarios que representan el historial de conversación.
            schema (BaseModel): Un esquema de Pydantic que define la estructura esperada de la respuesta.
            temperature (float, opcional): Controla la aleatoriedad de las respuestas. Si no se especifica, se utiliza la temperatura definida en la inicialización.

        Returns:
            dict: La respuesta de la API de Azure OpenAI que contiene la completación del chat estructurada según el esquema proporcionado.
        """
        try:
            completion = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                response_format=schema
            )
            return completion
        except Exception as e:
            log.error(f"Ocurrió un error al generar una salida estructurada: {e}")
            return None


####################################################
# Documentación Adicional Basada en la API Oficial
####################################################

# Parámetros adicionales opcionales:
# - frequency_penalty (float, opcional): Penaliza tokens nuevos basados en su frecuencia en el texto hasta el momento. Rango: -2.0 a 2.0.
# - logit_bias (dict, opcional): Modifica la probabilidad de que aparezcan tokens específicos en la respuesta.
# - logprobs (bool, opcional): Si es True, retorna las probabilidades logarítmicas de los tokens generados.
# - presence_penalty (float, opcional): Penaliza tokens nuevos según si ya aparecieron en el texto, aumentando la probabilidad de que el modelo hable sobre nuevos temas.
# - stop (str/list, opcional): Hasta 4 secuencias donde la API dejará de generar tokens adicionales.
# - stream_options (dict, opcional): Opciones adicionales para la transmisión de la respuesta.
# - top_p (float, opcional): Realiza una "nucleus sampling" considerando solo tokens que sumen el `top_p`% de probabilidad total.
# - n (int, opcional): Número de completaciones de chat a generar por cada mensaje de entrada.
# - seed (int, opcional): Especifica una semilla para hacer esfuerzos por reproducir resultados de manera determinista.
# - service_tier