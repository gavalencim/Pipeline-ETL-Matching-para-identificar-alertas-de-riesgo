# ETL Pipeline for International Sanctions Lists

## Overview

This project implements an incremental ETL pipeline capable of ingesting international sanctions lists from multiple public sources, transforming heterogeneous data into a unified canonical model and storing the results in DuckDB.

The pipeline was designed following software engineering principles such as separation of responsibilities, modularity and extensibility, making it easy to incorporate new sanction sources in the future.

Currently implemented sources:

* OFAC SDN List (United States Treasury)
* United Nations Consolidated Sanctions List

---

## Main Features

* Modular ETL architecture
* Incremental loading (Change Data Capture)
* Hash-based change detection
* Canonical data model
* Multiple data source support
* Automatic download of source files
* XML parsing using streaming (`iterparse`)
* DuckDB persistence
* Unit tests
* Structured logging

---

## Project Structure

```text
pipeline/
│
├── ingestion/
├── parsers/
├── normalization/
├── runner/
├── registry/
└── storage/

utils/

tests/

data/
```

---

## ETL Workflow

```text
Source Registry
        │
        ▼
Pipeline Runner
        │
        ▼
Download Source
        │
        ▼
Parser
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
DuckDB Repository
```

---

## Incremental Processing

Instead of loading every record on every execution, the pipeline performs Change Data Capture (CDC).

Each canonical record generates a deterministic SHA256 hash based on its content.

During execution the pipeline classifies records into four categories:

* New records
* Updated records
* Unchanged records
* Removed records (logical deletion)

This dramatically reduces unnecessary database writes.

---

## Technologies

* Python 3.12
* DuckDB
* Pydantic
* lxml
* Requests
* Pytest

---

## Running

```bash
python -m pipeline.run_pipeline
```

---

## Example Output

```text
Source        : OFAC

Read          : 19122
New           : 0
Updated       : 0
Unchanged     : 19122
Deactivated   : 0

----------------------------------------

Source        : UN

Read          : 1002
New           : 0
Updated       : 0
Unchanged     : 1002
Deactivated   : 0
```

---

## Future Improvements

* SEC FCPA source
* EU Sanctions List
* Fuzzy name matching
* REST API
* Dashboard
* Docker deployment
* Airflow scheduling
