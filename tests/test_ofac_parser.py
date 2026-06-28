from pathlib import Path
from pipeline.parsers.ofac_parser import OFACParser


def test_ofac_parser():

    xml_path = (
        Path("data")
        / "raw"
        / "ofac"
        / "SDN_ENHANCED.XML"
    )

    parser = OFACParser(str(xml_path))
    records = parser.parse()
    assert len(records) > 0
    first_record = records[0]

    assert "id_registro" in first_record
    assert "nombres" in first_record
    assert "aliases" in first_record

    print("\nPrimer registro:")
    print(first_record)