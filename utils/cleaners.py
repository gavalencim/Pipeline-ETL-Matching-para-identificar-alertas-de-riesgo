# LIMPIEZA Y ESTANDARIZACION DE TEXTO
import re
from unidecode import unidecode

def remove_extra_spaces(value: str) -> str:
    #Eliminar espacios 
    if not value:
        return ""

    return re.sub(
        r"\s+",
        " ",
        value
    ).strip()


def normalize_name(value: str) -> str:
    # Normalizar nombres: Mayúsculas sin tildes
    if not value:
        return ""

    normalized = unidecode(value) # Quita tildes
    normalized = normalized.upper() # Pone todo en Mayúsculas
    normalized = remove_extra_spaces(
        normalized
    )

    return normalized