from pathlib import Path
from pipeline.parsers.ofac_parser import OFACParser
from pipeline.normalization.canonical_factory import CanonicalFactory


def test_canonical_factory():

    xml_path = (
        Path("data")
        / "raw"
        / "ofac"
        / "SDN_ENHANCED.XML"
    )

    parser = OFACParser(str(xml_path))
    records = parser.parse()
    sanction = CanonicalFactory.build(
        records[0],
        fuente="OFAC"
    )

    print("\nRegistro normalizado:")
    print(
        sanction.model_dump()
    )

    assert sanction.fuente == "OFAC"
    assert sanction.activo is True
    assert sanction.hash_contenido is not None