from lxml import etree
from pipeline.normalization.common_record import CommonSanctionRecord


class UNParser:
    """
    Parser de la lista consolidada de Naciones Unidas.

    Convierte el XML oficial de la ONU en una lista de
    CommonSanctionRecord.

    Actualmente procesa:

    - INDIVIDUALS
    - ENTITIES
    """

    def __init__(self, xml_path: str):
        self.xml_path = xml_path

    # Parser principal
    def parse(self) -> list[CommonSanctionRecord]:

        tree = etree.parse(self.xml_path)
        root = tree.getroot()
        records: list[CommonSanctionRecord] = []

        # Personas
        individuals = root.find("INDIVIDUALS")

        if individuals is not None:

            for individual in individuals.findall("INDIVIDUAL"):
                records.append(self._parse_individual(individual))

        # Organizaciones
        entities = root.find("ENTITIES")

        if entities is not None:

            for entity in entities.findall("ENTITY"):
                records.append(self._parse_entity(entity))

        return records

    # Individual
    def _parse_individual(self, individual) -> CommonSanctionRecord:

        first_name = self._text(individual, "FIRST_NAME")
        second_name = self._text(individual, "SECOND_NAME")

        full_name = " ".join(
            part
            for part in [first_name, second_name]
            if part
        )

        return {

            "id_registro": self._text(individual, "DATAID"),
            "tipo_sujeto": "Individual",
            "nombres": full_name,
            "apellidos": None,
            "aliases": self._extract_aliases(individual),
            "fecha_nacimiento": self._extract_birth_date(individual),
            "nacionalidad": self._extract_nationalities(individual),
            "numero_documento": self._extract_document(individual),
            "tipo_sancion": self._text(individual, "UN_LIST_TYPE"),
            "programa_sancion": self._text(individual, "LIST_TYPE/VALUE"),
            "fecha_sancion": self._text(individual, "LISTED_ON"),
            "fecha_vencimiento": None,
            "codigo_referencia": self._text(individual, "REFERENCE_NUMBER"),
            "url_referencia": self._text(individual, "INTERPOL_LINK"),
            "comentarios": self._text(individual, "COMMENTS1"),
        }

    # Entity
    def _parse_entity(self, entity) -> CommonSanctionRecord:

        return {
            "id_registro": self._text(entity, "DATAID"),
            "tipo_sujeto": "Entity",
            "nombres": self._text(entity, "FIRST_NAME"),
            "apellidos": None,
            "aliases": self._extract_aliases(entity),
            "fecha_nacimiento": None,
            "nacionalidad": [],
            "numero_documento": self._extract_document(entity),
            "tipo_sancion": self._text(entity, "UN_LIST_TYPE"),
            "programa_sancion": self._text(entity, "LIST_TYPE/VALUE"),
            "fecha_sancion": self._text(entity, "LISTED_ON"),
            "fecha_vencimiento": None,
            "codigo_referencia": self._text(entity, "REFERENCE_NUMBER"),
            "url_referencia": None,
            "comentarios": self._text(entity, "COMMENTS1"),
            }

    # Métodos auxiliares
    def _text(self, parent, xpath: str) -> str | None:
        value = parent.findtext(xpath)

        if value:
            value = value.strip()

        return value or None

    def _extract_aliases(self, parent) -> list[str]:
        aliases = []

        for alias in parent.findall(".//ALIAS_NAME"):

            if alias.text:
                aliases.append(alias.text.strip())

        return aliases

    def _extract_nationalities(self, parent) -> list[str]:
        countries = []

        for country in parent.findall(".//NATIONALITY/VALUE"):

            if country.text:
                countries.append(country.text.strip())

        return countries

    def _extract_birth_date(self, parent) -> str | None:
        node = parent.find("INDIVIDUAL_DATE_OF_BIRTH")

        if node is None:
            return None

        year = self._text(node, "YEAR")
        month = self._text(node, "MONTH")
        day = self._text(node, "DAY")

        if year and month and day:
            return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

        if year and month:
            return f"{year}-{month.zfill(2)}"

        return year

    def _extract_document(self, parent) -> str | None:
        document = parent.find(".//INDIVIDUAL_DOCUMENT")

        if document is None:
            document = parent.find(".//ENTITY_DOCUMENT")

        if document is None:
            return None

        number = document.findtext("NUMBER")

        if number:
            return number.strip()

        return None