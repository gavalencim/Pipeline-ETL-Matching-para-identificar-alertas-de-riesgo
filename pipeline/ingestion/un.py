import logging
from pathlib import Path
from config.settings import UN_URL
from pipeline.ingestion.base_source import BaseSource
from pipeline.parsers.un_parser import UNParser
from utils.downloader import Downloader


logger = logging.getLogger(__name__)


class UNSource(BaseSource):
    """
    Fuente correspondiente a la lista consolidada
    del Consejo de Seguridad de Naciones Unidas.

    Responsabilidades:
    - Descargar el XML.
    - Devolver la ruta del archivo.
    - Indicar qué parser debe utilizarse.
    """
    FILE_NAME = "consolidated.xml"

    def __init__(self):
        super().__init__("UN")
        self.url =  UN_URL

    def extract(self) -> Path:
        logger.info("Iniciando descarga UN")
        destination = self.raw_dir / self.FILE_NAME
        Downloader.download(self.url, destination)
        logger.info(f"Archivo XML localizado: {destination.name}")

        return destination

    def get_parser(self):

        return UNParser