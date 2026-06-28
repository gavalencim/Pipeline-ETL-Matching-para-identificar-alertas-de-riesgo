from datetime import datetime, UTC

from pipeline.normalization.change_detector import detect_changes
from pipeline.normalization.schemas import CanonicalSanction


def build_record(id_registro: str, hash_contenido: str):

    return CanonicalSanction(

        id_registro=id_registro,
        fuente="OFAC",

        tipo_sujeto="Entity",

        nombres="Empresa X",
        apellidos=None,

        aliases=[],

        fecha_nacimiento=None,
        nacionalidad=[],

        numero_documento=None,

        tipo_sancion=None,
        fecha_sancion=None,
        fecha_vencimiento=None,

        programa_sancion=None,
        codigo_referencia=None,
        url_referencia=None,
        comentarios=None,

        activo=True,

        fecha_ingesta=datetime.now(UTC),

        hash_contenido=hash_contenido
    )


def test_change_detector():

    incoming = [

        build_record("1", "AAA"),
        build_record("2", "BBB"),
        build_record("3", "CCC")
    ]

    existing = {

        ("OFAC", "2"): {
            "hash": "BBB",
            "activo": True
        },

        ("OFAC", "3"): {
            "hash": "XXX",
            "activo": True
        }
    }

    result = detect_changes(
        incoming=incoming,
        existing_index=existing
    )

    print()

    print("Insertar:")
    print([r.id_registro for r in result["to_insert"]])

    print()

    print("Actualizar:")
    print([r.id_registro for r in result["to_update"]])

    print()

    print("Sin cambios:")
    print([r.id_registro for r in result["unchanged"]])

    print()

    print("IDs presentes:")
    print(result["ids_present"])

    assert len(result["to_insert"]) == 1
    assert len(result["to_update"]) == 1
    assert len(result["unchanged"]) == 1

    assert result["to_insert"][0].id_registro == "1"
    assert result["to_update"][0].id_registro == "3"
    assert result["unchanged"][0].id_registro == "2"