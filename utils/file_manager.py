# MANIPULAR ARCHIVOS
import logging
import zipfile
from pathlib import Path

logger = logging.getLogger(__name__)

class FileManager:

    @staticmethod
    def extract_zip(zip_path: Path, destination: Path) -> None:
        
        # Descomprimir un ZIP:
        logger.info(f"Extrayendo ZIP: {zip_path}")

        with zipfile.ZipFile(zip_path, "r") as zip_file: zip_file.extractall(destination)

        logger.info("Extracción completada")

    @staticmethod
    def find_files(directory: Path, extension: str) -> list[Path]:
        # Buscar archivos por extensión ignorando minusculas y mayusculas:

        extension = extension.lower()
        return [
            file
            for file in directory.iterdir()
            if file.is_file()
            and file.suffix.lower()
            == f".{extension}"]
    
    @staticmethod
    def create_directory(directory: Path) -> None:
        
        # Crear directorio si no existe: 
        directory.mkdir(parents=True, exist_ok=True)