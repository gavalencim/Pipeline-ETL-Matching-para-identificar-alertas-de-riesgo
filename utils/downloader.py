# DESCARGAR ARCHIVOS DE INTERNET
import logging
from pathlib import Path
import requests

logger = logging.getLogger(__name__)

class Downloader:
    
    # Descargar un archivo desde una URL.
    @staticmethod
    def download(url: str, destination: Path, timeout: int = 60) -> Path: 
        
        logger.info(f"Descargando archivo desde {url}")

        response = requests.get(url, timeout=timeout)

        response.raise_for_status()

        with open(destination, "wb") as file: file.write(response.content)

        logger.info(f"Archivo guardado en {destination}")

        return destination
