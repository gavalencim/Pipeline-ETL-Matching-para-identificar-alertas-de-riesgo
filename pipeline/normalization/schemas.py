from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class CanonicalSanction(BaseModel):
    # Esquema canónico:
    id_registro: str
    fuente: str
    tipo_sujeto: str
    nombres: str
    apellidos: Optional[str] = None
    aliases: List[str] = []
    fecha_nacimiento: Optional[str] = None
    nacionalidad: List[str] = Field(default_factory=list)
    numero_documento: Optional[str] = None
    tipo_sancion: Optional[str] = None
    programa_sancion: Optional[str] = None
    fecha_sancion: Optional[str] = None
    fecha_vencimiento: Optional[str] = None
    codigo_referencia: Optional[str] = None
    url_referencia: Optional[str] = None
    comentarios: Optional[str] = None
    activo: bool
    fecha_ingesta: datetime
    hash_contenido: str