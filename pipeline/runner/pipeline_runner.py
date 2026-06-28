import logging
from datetime import datetime
from pipeline.ingestion.base_source import BaseSource
from pipeline.normalization.canonical_factory import CanonicalFactory
from pipeline.storage.duckdb_repository import DuckDBRepository
from pipeline.normalization.change_detector import detect_changes

logger = logging.getLogger(__name__)

class PipelineRunner:
    """
    Orquestador principal del proceso ETL.

    Su responsabilidad es coordinar el flujo completo
    desde la extracción hasta el almacenamiento,
    sin conocer detalles específicos de cada fuente.
    """

    def run(self, source: BaseSource):

        logger.info("=" * 60)
        logger.info(f"Iniciando pipeline para {source.source_name}")
        logger.info("=" * 60)
        start = datetime.now()

        # Extracción
        logger.info("Extrayendo información...")
        extracted_file = source.extract()

        # Parser
        logger.info("Parseando registros...")
        parser_class = source.get_parser()
        parser = parser_class(extracted_file)
        parsed_records = parser.parse()
        logger.info(f"Registros parseados: {len(parsed_records)}")

        # Normalización
        logger.info("Normalizando registros...")
        canonical_records = [

            CanonicalFactory.build(parsed_record=record, fuente=source.source_name)
            for record in parsed_records
        ]

        # Persistencia
        logger.info("Almacenando en DuckDB...")
        repository = DuckDBRepository()

        try: 

            # Cargar índice existente
            existing_index = repository.load_index()

            # Detectar cambios
            changes = detect_changes(canonical_records, existing_index)

            # Insertar nuevos
            repository.insert_many(changes["to_insert"])

            # Actualizar modificados
            repository.update_many(changes["to_update"])

            # Desactivar eliminados
            deactivated = repository.deactivate_missing(fuente=source.source_name, ids_presentes=changes["ids_present"])

            total = repository.count_records()
        
        finally: 
            repository.close()

        # Resumen: 
        elapsed = datetime.now() - start

        logger.info("=" * 60)
        logger.info("PIPELINE FINALIZADO")
        logger.info("=" * 60)
        logger.info(f"Fuente        : {source.source_name}")
        logger.info(f"Leídos        : {len(parsed_records)}")
        logger.info(f"Nuevos        : {len(changes['to_insert'])}")
        logger.info(f"Actualizados  : {len(changes['to_update'])}")
        logger.info(f"Sin cambios   : {len(changes['unchanged'])}")
        logger.info(f"Desactivados  : {deactivated}")
        logger.info(f"Total BD      : {total}")
        logger.info(f"Tiempo        : {elapsed}")
        logger.info("=" * 60)