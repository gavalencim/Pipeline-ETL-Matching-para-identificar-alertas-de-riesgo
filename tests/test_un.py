from pipeline.ingestion.un import UNSource


def test_un_source():

    source = UNSource()

    xml_path = source.extract()

    print("\nArchivo descargado:")

    print(xml_path)

    assert xml_path.exists()