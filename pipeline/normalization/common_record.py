# DEFINIR FORMATO QUE LOS PARSERS DEBEN DEVOLVER
from typing import TypedDict


class CommonSanctionRecord(TypedDict):

    id_registro: str
    tipo_sujeto: str
    nombres: str
    apellidos: str | None
    aliases: list[str]
    fecha_nacimiento: str | None
    nacionalidad: list[str]
    numero_documento: str | None
    tipo_sancion: str | None
    programa_sancion: str | None
    fecha_sancion: str | None
    fecha_vencimiento: str | None
    codigo_referencia: str | None
    url_referencia: str | None
    comentarios: str | None