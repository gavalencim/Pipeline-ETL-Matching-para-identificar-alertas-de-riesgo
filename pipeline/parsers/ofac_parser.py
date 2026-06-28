from lxml import etree
from pipeline.normalization.common_record import (CommonSanctionRecord)


class OFACParser:
    """
    Parser de la lista OFAC SDN Enhanced XML.

    Responsabilidades:
    - Leer el XML.
    - Extraer la información relevante de cada entidad.
    - Devolver registros en formato CommonSanctionRecord.

    No debe:
    - Calcular hashes.
    - Conocer DuckDB.
    - Conocer CanonicalSanction.
    - Realizar persistencia.
    """

    NAMESPACE = (
        "https://sanctionslistservice.ofac.treas.gov/"
        "api/PublicationPreview/exports/ENHANCED_XML"
    )

    def __init__(self, xml_path: str):
        self.xml_path = xml_path

    def parse(self) -> list[CommonSanctionRecord]:
        # Procesar el XML completo y devolver una lista de registros
        # con la estructura común definida por CommonSanctionRecord.
        
        records: list[CommonSanctionRecord] = []
        entity_tag = f"{{{self.NAMESPACE}}}entity"
        context = etree.iterparse(self.xml_path, events=("end",), tag=entity_tag)

        for _, entity in context:
            record = self._parse_entity(entity)
            records.append(record)
            # Liberar memoria
            entity.clear()

        return records

    def _parse_entity(self, entity ) -> CommonSanctionRecord:
        # Convertir una entidad XML OFAC en un CommonSanctionRecord.
        
        return {
            "id_registro": self._extract_identity_id(entity),
            "tipo_sujeto": self._extract_entity_type(entity),
            "nombres": self._extract_primary_name(entity),
            "apellidos": None,
            "aliases": self._extract_aliases(entity),
            "fecha_nacimiento": None,
            "nacionalidad": [],
            "numero_documento": None,
            "tipo_sancion": self._extract_sanction_type(entity),
            "fecha_sancion": None,
            "fecha_vencimiento": None,
            "programa_sancion": None,
            "codigo_referencia": None,
            "url_referencia": None,
            "comentarios": None,
        }

    def _extract_identity_id(self, entity) -> str:
        # Extraer el identificador único OFAC

        return entity.findtext(
            f".//{{{self.NAMESPACE}}}identityId",
            default=""
        )

    def _extract_entity_type(self, entity) -> str:
        # Extraer el tipo de sujeto

        return entity.findtext(f".//{{{self.NAMESPACE}}}entityType", default="")

    def _extract_primary_name(self, entity) -> str:
        # Extraer el nombre principal.

        names = entity.findall(f".//{{{self.NAMESPACE}}}name")

        for name in names:
            is_primary = name.findtext(f"{{{self.NAMESPACE}}}isPrimary")

            if is_primary == "true":
                return name.findtext(f".//{{{self.NAMESPACE}}}formattedFullName", default="")

        return ""

    def _extract_aliases(self, entity) -> list[str]:
        # Extraer aliases o nombres alternativos
    
        aliases = []

        names = entity.findall(f".//{{{self.NAMESPACE}}}name")

        for name in names:
            is_primary = name.findtext(f"{{{self.NAMESPACE}}}isPrimary")

            if is_primary == "false":
                alias = name.findtext(f".//{{{self.NAMESPACE}}}formattedFullName", default="")

                if alias:
                    aliases.append(alias)

        return aliases

    def _extract_sanction_type(self, entity) -> str | None:
        # Extraer el tipo de sanción

        sanctions = entity.findall(
            f".//{{{self.NAMESPACE}}}sanctionsTypes"
            f"/{{{self.NAMESPACE}}}sanctionsType"
        )

        if sanctions:
            return sanctions[0].text

        return None