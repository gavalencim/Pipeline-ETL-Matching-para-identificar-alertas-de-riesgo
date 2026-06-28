# ETL Pipeline para Listas Internacionales de Sanciones

Proyecto desarrollado como prueba técnica y como ejercicio de diseño de una arquitectura ETL escalable para la integración de listas internacionales de sanciones.

Actualmente el pipeline consume información desde diferentes organismos internacionales, normaliza los registros hacia un modelo canónico único y los almacena en DuckDB aplicando estrategias de Change Data Capture (CDC).

---

# Objetivos del proyecto

El propósito principal del proyecto es construir una arquitectura que permita incorporar nuevas fuentes de sanciones sin modificar el núcleo del pipeline.

Se busca que cada nueva fuente únicamente implemente la lógica necesaria para:

- descargar la información
- interpretar el formato original
- transformarla al modelo común

Todo el resto del proceso permanece exactamente igual.

---

# Características

Actualmente el proyecto incluye:

- Arquitectura ETL desacoplada
- Modelo canónico independiente de la fuente
- Descarga automática de archivos
- Soporte para XML y JSON
- Parsers especializados por organismo
- Persistencia en DuckDB
- Detección de cambios mediante hashes
- Actualización incremental (CDC)
- Desactivación lógica de registros eliminados
- Registro automático de fuentes
- Logging detallado
- Pruebas unitarias

---

# Fuentes implementadas

Actualmente el pipeline soporta las siguientes listas internacionales.

| Fuente | Formato | Estado |
|---------|----------|---------|
| OFAC SDN | XML (ZIP) | ✅ |
| United Nations Consolidated List | XML | ✅ |

Fuentes planeadas:

- SEC FCPA Enforcement Actions
- Unión Europea
- UK Sanctions List
- Interpol Red Notices

---

# Arquitectura

```
Fuente
    │
    ▼
Downloader
    │
    ▼
Parser específico
    │
    ▼
CommonSanctionRecord
    │
    ▼
CanonicalFactory
    │
    ▼
CanonicalSanction
    │
    ▼
Change Detector (CDC)
    │
    ▼
DuckDBRepository
```

Cada etapa tiene una única responsabilidad y puede evolucionar de manera independiente.

---

# Estructura del proyecto

```text
pipeline/

    ingestion/
        base_source.py
        ofac.py
        un.py

    parsers/
        ofac_parser.py
        un_parser.py

    normalization/
        common_record.py
        canonical_factory.py
        schemas.py
        change_detector.py

    storage/
        duckdb_repository.py

    registry/
        source_registry.py

    runner/
        pipeline_runner.py

run_pipeline.py

utils/

config/

tests/

docs/
```

---

# Flujo de ejecución

Para cada fuente registrada:

1. Descarga el archivo original.
2. Ejecuta el parser correspondiente.
3. Genera registros Python.
4. Convierte todos los registros al modelo canónico.
5. Calcula un hash SHA256 del contenido.
6. Compara los hashes contra DuckDB.
7. Inserta registros nuevos.
8. Actualiza registros modificados.
9. Desactiva registros que desaparecieron de la fuente.

---

# Change Data Capture

El proyecto implementa un mecanismo sencillo de CDC basado en hashes.

Cada registro canónico genera un SHA256 calculado sobre todos sus campos relevantes.

Durante una nueva ejecución:

- Si el registro no existe → INSERT
- Si existe y el hash cambió → UPDATE
- Si existe y el hash es igual → No se realiza ninguna operación
- Si un registro desaparece de la fuente → activo = FALSE

Este mecanismo evita reprocesar registros sin cambios y reduce considerablemente el costo de actualización.

---

# Modelo Canónico

Todas las fuentes se transforman al mismo esquema.

Campos principales:

- id_registro
- fuente
- tipo_sujeto
- nombres
- apellidos
- aliases
- nacionalidad
- numero_documento
- tipo_sancion
- programa_sancion
- codigo_referencia
- url_referencia
- comentarios
- activo
- fecha_ingesta
- hash_contenido

Esto permite incorporar nuevas fuentes sin modificar la capa de almacenamiento.

---

# Tecnologías

- Python 3.12
- DuckDB
- Pydantic
- Requests
- lxml
- Pytest

---

# Ejecución

Crear ambiente virtual

```bash
python -m venv .venv
```

Activar

Windows

```bash
.venv\Scripts\activate
```

Linux

```bash
source .venv/bin/activate
```

Instalar dependencias

```bash
pip install -r requirements.txt
```

Ejecutar

```bash
python -m pipeline.run_pipeline
```

---

# Ejemplo de salida

```text
============================================================

Fuente        : OFAC

Leídos        : 19122

Nuevos        : 5

Actualizados  : 3

Sin cambios   : 19110

Desactivados  : 4

Tiempo        : 00:01:04

============================================================
```

---

# Próximos pasos

- Incorporar nuevas listas internacionales
- Matching entre listas
- Exposición mediante API REST
- Dashboard de monitoreo
- Versionamiento histórico
- Métricas de calidad de datos

---

# Autor

Proyecto desarrollado por **Ginna Valencia** como ejercicio de arquitectura ETL y prueba técnica para integración de listas internacionales de sanciones.
