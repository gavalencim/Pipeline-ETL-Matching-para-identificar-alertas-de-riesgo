from lxml import etree

from config.settings import DATA_DIR


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

for _, entity in context:

    features = entity.find(
        f"{{{namespace}}}features"
    )

    if features is not None:

        print("\nFEATURES ENCONTRADOS\n")

        for feature in features[:10]:

            print("-" * 50)

            for child in feature:

                tag = child.tag.split("}")[-1]

                print(
                    f"{tag}: {child.text}"
                )

        break