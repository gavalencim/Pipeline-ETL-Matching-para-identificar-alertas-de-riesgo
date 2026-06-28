from datetime import datetime, UTC

from pipeline.storage.duckdb_repository import DuckDBRepository
from pipeline.normalization.schemas import CanonicalSanction


def build_record():

    return CanonicalSanction(

        id_registro="TEST-001",
        fuente="TEST",

        tipo_sujeto="Entity",

        nombres="Empresa Test",
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

        hash_contenido="ABC123"
    )


def test_duckdb_repository():

    repo = DuckDBRepository()

    repo.delete_record(fuente="TEST", id_registro="TEST-001")

    record = build_record()

    repo.insert(record)

    total = repo.count_records()

    print()
    print("Total registros:", total)

    index = repo.load_index()

    print()
    print("Registro encontrado:")

    print(index[("TEST", "TEST-001")])

    assert ("TEST", "TEST-001") in index

    repo.close()