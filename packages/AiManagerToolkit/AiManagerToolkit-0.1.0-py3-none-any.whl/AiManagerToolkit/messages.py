class Message:
    """
    Clase para representar un mensaje con un rol específico (user, assistant, system)
    y contenido asociado. El contenido puede ser texto o una URL de imagen.

    Args:
        role (str): El rol del mensaje, puede ser "user", "assistant" o "system".
        *args: Cualquier número de cadenas de texto que se añadirán al contenido.
        **kwargs: Argumentos adicionales como 'image_url' para añadir una imagen al contenido.

    Attributes:
        role (str): El rol del mensaje.
        content (list): Lista de diccionarios que contienen el contenido del mensaje.
    """
    
    def __init__(self, role, *args, **kwargs):
        self.role = role
        self.content = []

        # Añade el contenido de texto
        if args:
            for text in args:
                self.content.append({
                    "type": "text",
                    "text": text
                })

        # Añade una URL de imagen si se proporciona
        if "image_url" in kwargs:
            self.content.append({
                "type": "image_url",
                "image_url": {
                    "url": kwargs["image_url"]
                }
            })

    def to_dict(self):
        """
        Convierte la instancia del mensaje a un diccionario.

        Returns:
            dict: Un diccionario con el rol y el contenido del mensaje.
        """
        return {
            "role": self.role,
            "content": self.content
        }

def user(*args, **kwargs):
    """
    Crea un mensaje con el rol 'user'.

    Returns:
        dict: Un diccionario que representa el mensaje.
    """
    return Message("user", *args, **kwargs).to_dict()

def assistant(*args, **kwargs):
    """
    Crea un mensaje con el rol 'assistant'.

    Returns:
        dict: Un diccionario que representa el mensaje.
    """
    return Message("assistant", *args, **kwargs).to_dict()

def system(*args, **kwargs):
    """
    Crea un mensaje con el rol 'system'.

    Returns:
        dict: Un diccionario que representa el mensaje.
    """
    return Message("system", *args, **kwargs).to_dict()