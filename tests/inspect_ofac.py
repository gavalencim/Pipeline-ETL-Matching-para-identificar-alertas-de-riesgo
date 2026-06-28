from lxml import etree

from config.settings import DATA_DIR


def show_structure(element, level=0):

    indent = "    " * level

    tag = element.tag.split("}")[-1]

    print(f"{indent}{tag}")

    for child in element:
        show_structure(child, level + 1)


xml_path = (
    DATA_DIR
    / "raw"
    / "ofac"
    / "SDN_ENHANCED.XML"
)

namespace = (
    "https://sanctionslistservice.ofac.treas.gov/"
    "api/PublicationPreview/exports/ENHANCED_XML"
)

entity_tag = f"{{{namespace}}}entity"

context = etree.iterparse(
    str(xml_path),
    events=("end",),
    tag=entity_tag
)

_, entity = next(context)

for section in entity:

    section_name = section.tag.split("}")[-1]

    print("\n" + "=" * 60)
    print(section_name.upper())
    print("=" * 60)

    show_structure(section)