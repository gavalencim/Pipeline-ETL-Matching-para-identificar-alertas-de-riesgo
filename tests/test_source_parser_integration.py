from pipeline.ingestion.ofac import OFACSource


def test_source_parser_integration():

    source = OFACSource()

    xml_path = source.extract()

    parser_class = source.get_parser()

    parser = parser_class(xml_path)

    records = parser.parse()

    assert len(records) > 0

    print("\nPrimer registro:")
    print(records[0])