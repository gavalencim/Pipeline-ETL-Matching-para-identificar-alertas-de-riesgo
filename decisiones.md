# Design Decisions

## Why a Canonical Model?

Each sanctions source publishes information using different field names, formats and structures.

Instead of adapting the storage layer for every source, the project defines a single canonical representation (`CanonicalSanction`).

Every parser transforms its native format into this shared model.

Benefits:

* Simplifies persistence.
* Makes the system extensible.
* Reduces duplicated logic.

---

## Why CommonSanctionRecord?

Parsers should not instantiate database models directly.

Instead, every parser returns a lightweight intermediate structure called `CommonSanctionRecord`.

Responsibilities:

Parser

↓

Extract source-specific fields

↓

Return standardized dictionary

↓

CanonicalFactory

↓

CanonicalSanction

This separation keeps parsers focused only on extraction.

---

## Why a CanonicalFactory?

The factory centralizes all normalization logic.

Responsibilities:

* Create CanonicalSanction objects.
* Generate ingestion timestamp.
* Generate content hash.
* Apply default values.

This avoids duplicating normalization logic across multiple parsers.

---

## Why Change Data Capture?

Reloading every record on every execution is inefficient.

Instead, the pipeline computes a SHA256 hash for every canonical record.

By comparing hashes with existing database values, records are classified as:

* Insert
* Update
* Unchanged

Benefits:

* Faster executions
* Less database I/O
* Easier auditing

---

## Why DuckDB?

DuckDB was selected because it provides:

* Zero configuration
* Embedded database
* Excellent analytical performance
* SQL compatibility
* Portable single-file database

It is ideal for local ETL pipelines.

---

## Why a Repository Layer?

All SQL is isolated inside `DuckDBRepository`.

The rest of the project never interacts directly with SQL.

Advantages:

* Easier maintenance
* Better testing
* Clear separation of responsibilities

---

## Why a Source Registry?

Instead of hardcoding sources inside the pipeline, a registry keeps track of all available sources.

Adding a new source only requires:

1. Create the ingestion class.
2. Create its parser.
3. Register it.

No changes are required in the pipeline execution logic.

---

## Why Streaming XML Parsing?

Large XML files can contain tens of thousands of records.

Instead of loading the entire document into memory, parsers use `lxml.iterparse()`.

Benefits:

* Constant memory usage
* Better scalability
* Faster processing
