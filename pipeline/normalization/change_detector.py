from pipeline.normalization.schemas import CanonicalSanction


def detect_changes(incoming: list[CanonicalSanction], existing_index: dict) -> dict:
    """
    Detecta cambios entre los registros recién procesados
    y los almacenados actualmente en la base de datos.

    Clasifica los registros en cuatro grupos:

    - to_insert:
        No existen en la base de datos.

    - to_update:
        Existen pero cambió su contenido.

    - unchanged:
        Existen y su hash es idéntico.

    - ids_present:
        Conjunto de ids encontrados durante la
        ejecución. Se utiliza posteriormente para
        detectar registros eliminados de la fuente.
    """
    to_insert = []
    to_update = []
    unchanged = []

    ids_present = set()

    for record in incoming:
        key = (record.fuente, record.id_registro)
        ids_present.add(record.id_registro)
        existing = existing_index.get(key)

        # Registro nuevo
        if existing is None:
            to_insert.append(record)
            continue

        # Registro sin cambios
        if existing["hash"] == record.hash_contenido:
            unchanged.append(record)
            continue

        # Registro actualizado
        to_update.append(record)

    return {

        "to_insert": to_insert,
        "to_update": to_update,
        "unchanged": unchanged,
        "ids_present": ids_present
    }