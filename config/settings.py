'''
Centralizar las configuraciones del proyecto
'''
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

DUCKDB_PATH = DATA_DIR / "sanctions.duckdb"

OFAC_URL = (
    "https://sanctionslistservice.ofac.treas.gov/"
    "api/PublicationPreview/exports/"
    "SDN_ENHANCED.ZIP"
)

UN_URL = (
    "https://scsanctions.un.org/resources/xml/en/consolidated.xml"
)

EU_URL = (
    "https://webgate.ec.europa.eu/fsd/fsf/public/files/"
    "xmlFullSanctionsList_1_1/content"
)

FCPA_URL = (
    'https://efts.sec.gov/LATEST/search-index?q=%22%22'
)

PACO_DISC_URL = (
    "https://paco7public7info7prod.blob.core.windows.net/"
    "paco-pulic-info/antecedentes_SIRI_sanciones_Cleaned.zip"
)

PACO_PENAL_URL = (
    "https://paco7public7info7prod.blob.core.windows.net/"
    "paco-pulic-info/sanciones_penales_FGN.csv"
)

WORLD_BANK_URL = (
    "https://projects.worldbank.org/en/projects-operations/"
    "procurement/debarred-firms"
)