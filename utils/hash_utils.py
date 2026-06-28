# GENERAR HASHES PARA CAPTURAR EL CAMBIO DE LOS DATOS (CDC)
import hashlib
import json

def generate_hash(record: dict) -> str:
    
    # Generar hash SHA256 del registro normalizado para detección de cambios
    payload = json.dumps(
        record,
        sort_keys=True,
        default=str
    )

    return hashlib.sha256(payload.encode("utf-8")).hexdigest()