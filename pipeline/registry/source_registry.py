from pipeline.ingestion.ofac import OFACSource
from pipeline.ingestion.un import UNSource
from pipeline.ingestion.base_source import BaseSource


class SourceRegistry:
    """
    Registro centralizado de todas las fuentes de datos.

    Permite que el pipeline descubra automáticamente
    qué fuentes debe ejecutar sin modificar el
    PipelineRunner ni el punto de entrada.
    """

    @staticmethod
    def get_sources() -> list[BaseSource]:

        return [
            OFACSource(), 
            UNSource(),
        ]