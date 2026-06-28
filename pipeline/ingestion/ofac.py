import logging
from pathlib import Path
from config.settings import OFAC_URL
from pipeline.ingestion.base_source import BaseSource
from utils.downloader import Downloader
from utils.file_manager import FileManager
from pipeline.parsers.ofac_parser import OFACParser


logger = logging.getLogger(__name__)


class OFACSource(BaseSource):
    # Implementar la fuente OFAC
    
    def __init__(self):
        super().__init__("OFAC")
        self.url = OFAC_URL

    def extract(self) -> Path:
        # Descargar y descomprimir
        logger.info("Iniciando descarga OFAC")
        zip_path = (
            self.raw_dir /
            "ofac.zip")

        Downloader.download( self.url, zip_path) # Descarga archivo
        FileManager.extract_zip(zip_path, self.raw_dir) # Descomprime archivo
        xml_files = FileManager.find_files(self.raw_dir, "XML") # Busca archivo por extensión

        if not xml_files:
            raise FileNotFoundError("No se encontró XML OFAC")
        
        xml_path = xml_files[0]
        logger.info("Archivo XML localizado: %s",xml_path.name)

        return xml_path
    
    def get_parser(self):
        return OFACParser