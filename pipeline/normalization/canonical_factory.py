from datetime import datetime, UTC
from pipeline.normalization.schemas import CanonicalSanction
from utils.hash_utils import generate_hash
from pipeline.normalization.common_record import (CommonSanctionRecord)


class CanonicalFactory:

    @staticmethod
    def build(parsed_record: CommonSanctionRecord, fuente: str) -> CanonicalSanction:

        return CanonicalSanction(

            id_registro=parsed_record["id_registro"],
            fuente=fuente,
            tipo_sujeto=parsed_record["tipo_sujeto"],
            nombres=parsed_record["nombres"],
            apellidos=parsed_record["apellidos"],
            aliases=parsed_record["aliases"],
            fecha_nacimiento=parsed_record["fecha_nacimiento"],
            nacionalidad=parsed_record["nacionalidad"],
            numero_documento=parsed_record["numero_documento"],
            tipo_sancion=parsed_record["tipo_sancion"],
            programa_sancion=parsed_record["programa_sancion"],
            fecha_sancion=parsed_record["fecha_sancion"],
            fecha_vencimiento=parsed_record["fecha_vencimiento"],
            codigo_referencia=parsed_record["codigo_referencia"],
            url_referencia=parsed_record["url_referencia"],
            comentarios=parsed_record["comentarios"],
            activo=True,
            fecha_ingesta=datetime.now(UTC),
            hash_contenido=generate_hash(parsed_record)
        )