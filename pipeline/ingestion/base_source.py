from abc import ABC
from abc import abstractmethod
from config.settings import DATA_DIR
from utils.file_manager import FileManager


class BaseSource(ABC):
    # Clase de procesamiento común de las fuentes de datos

    def __init__(self, source_name: str):
        self.source_name = source_name

        self.raw_dir = (
            DATA_DIR /
            "raw" /
            source_name
        )

        FileManager.create_directory(self.raw_dir)

    @abstractmethod
    def extract(self):
        # Obtener datos
        pass

    @abstractmethod
    def get_parser(self):
        # Convertir datos a estructura de python
        pass