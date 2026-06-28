# Decisiones de Arquitectura

Este documento describe las principales decisiones de diseño adoptadas durante el desarrollo del proyecto y las razones detrás de ellas.

---

# Objetivo arquitectónico

Desde el inicio el objetivo fue construir un pipeline que pudiera crecer fácilmente conforme se incorporaran nuevas fuentes de información.

Se priorizó una arquitectura desacoplada, donde cada componente tuviera una única responsabilidad.

---

# Separación entre extracción y parsing

Cada fuente implementa únicamente tres responsabilidades:

- descargar los datos
- indicar qué parser utilizar
- identificar el nombre de la fuente

Toda la lógica de interpretación del formato original vive exclusivamente dentro del parser.

Esto evita mezclar responsabilidades y facilita el mantenimiento.

---

# Modelo Canónico

Cada organismo publica información diferente.

En lugar de crear tablas específicas para cada uno, todos los registros se transforman hacia un único modelo común.

Esto permite:

- consultas homogéneas
- matching entre fuentes
- agregar nuevas listas sin modificar la base de datos

---

# Uso de Pydantic

Los registros normalizados se representan mediante modelos Pydantic.

Esto proporciona:

- validación automática
- tipado fuerte
- serialización sencilla
- menor cantidad de errores durante la normalización

---

# DuckDB como motor de almacenamiento

Se eligió DuckDB debido a que:

- funciona como un archivo local
- no requiere servidor
- ofrece excelente rendimiento analítico
- facilita la distribución del proyecto

Para una prueba técnica resulta una excelente alternativa frente a PostgreSQL.

---

# Registro centralizado de fuentes

Se implementó un SourceRegistry encargado de registrar todas las fuentes disponibles.

El PipelineRunner nunca conoce qué organismos existen.

Simplemente solicita:

```python
SourceRegistry.get_sources()
```

Esto permite agregar nuevas fuentes modificando únicamente el registro.

---

# PipelineRunner como orquestador

Toda la coordinación del flujo ETL se concentra en PipelineRunner.

Su responsabilidad consiste únicamente en orquestar:

Extracción

↓

Parsing

↓

Normalización

↓

CDC

↓

Persistencia

Cada etapa permanece completamente desacoplada.

---

# Change Data Capture

El proyecto implementa CDC mediante hashes SHA256.

Cada registro genera un hash calculado sobre todos los atributos relevantes.

Durante nuevas ejecuciones:

- hash nuevo → INSERT
- hash diferente → UPDATE
- hash igual → se omite
- registro ausente → activo = FALSE

Este enfoque resulta sencillo, rápido y suficientemente robusto para listas internacionales que no ofrecen mecanismos propios de versionamiento.

---

# Soft Delete

Los registros nunca se eliminan físicamente.

Cuando desaparecen de la fuente se actualiza:

```text
activo = FALSE
```

Esto conserva el histórico y permite auditoría.

---

# Índice en memoria

Antes de iniciar la comparación de cambios se carga únicamente:

- fuente
- id_registro
- hash

Esto reduce significativamente la cantidad de consultas durante el procesamiento masivo.

---

# Parsers independientes

Cada formato posee su propio parser.

Actualmente:

- OFACParser
- UNParser

Esto evita grandes bloques de código con múltiples condiciones según la fuente.

---

# Organización del proyecto

La estructura sigue una separación por responsabilidades:

- ingestion
- parsers
- normalization
- storage
- registry
- runner
- utils

Esta distribución facilita localizar rápidamente cualquier componente del pipeline.

---

# Principios aplicados

Durante el desarrollo se procuró seguir varios principios de ingeniería de software:

- Responsabilidad única (SRP)
- Abierto/Cerrado (OCP)
- Separación de responsabilidades
- Bajo acoplamiento
- Alta cohesión
- Reutilización de componentes
- Escalabilidad

Aunque el proyecto corresponde a una prueba técnica, la arquitectura fue diseñada pensando en un sistema que pueda evolucionar incorporando nuevas fuentes internacionales con modificaciones mínimas.
* Faster processing
