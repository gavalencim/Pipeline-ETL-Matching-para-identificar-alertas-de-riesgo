from pathlib import Path
import sys
from collections import Counter

from lxml import etree


# ==========================================================
# UTILIDADES
# ==========================================================

def clean_tag(tag: str) -> str:
    """
    Elimina el namespace de una etiqueta XML.
    """

    if "}" in tag:
        return tag.split("}", 1)[1]

    return tag


def print_tree(element, level=0, max_depth=5):
    """
    Imprime la estructura jerárquica de un nodo.
    """

    indent = "    " * level

    print(f"{indent}{clean_tag(element.tag)}")

    if level >= max_depth:
        return

    for child in element:
        print_tree(child, level + 1, max_depth)


def print_values(element, level=0):
    """
    Imprime todos los valores encontrados
    dentro de un nodo.
    """

    indent = "    " * level

    text = (element.text or "").strip()

    if text:
        print(f"{indent}{clean_tag(element.tag)} = {text}")

    for attribute, value in element.attrib.items():
        print(f"{indent}@{attribute} = {value}")

    for child in element:
        print_values(child, level + 1)


# ==========================================================
# VALIDACIÓN
# ==========================================================

if len(sys.argv) != 2:

    print("\nUso:")

    print("python tests/inspect_xml.py ruta/del/archivo.xml")

    exit()


xml_path = Path(sys.argv[1])

if not xml_path.exists():

    raise FileNotFoundError(xml_path)


# ==========================================================
# PARSEO
# ==========================================================

tree = etree.parse(xml_path)

root = tree.getroot()


# ==========================================================
# ROOT
# ==========================================================

print("=" * 70)
print("ROOT")
print("=" * 70)

print(clean_tag(root.tag))

print()


# ==========================================================
# HIJOS DEL ROOT
# ==========================================================

print("=" * 70)
print("HIJOS DEL ROOT")
print("=" * 70)

children = Counter()

for child in root:

    children[clean_tag(child.tag)] += 1

for tag, amount in children.items():

    print(f"{tag} ({amount})")

print()


# ==========================================================
# BUSCAR PRIMER REGISTRO
# ==========================================================

candidate = None

for child in root:

    if len(child):

        candidate = child[0]

        break

if candidate is None:

    raise Exception("No fue posible encontrar un registro.")


# ==========================================================
# ESTRUCTURA
# ==========================================================

print("=" * 70)
print("ESTRUCTURA DEL PRIMER REGISTRO")
print("=" * 70)

print_tree(candidate)

print()


# ==========================================================
# VALORES
# ==========================================================

print("=" * 70)
print("VALORES DEL PRIMER REGISTRO")
print("=" * 70)

print_values(candidate)

print()


# ==========================================================
# CONTAR REGISTROS
# ==========================================================

print("=" * 70)
print("CANTIDAD DE REGISTROS")
print("=" * 70)

parent = candidate.getparent()

print(len(parent))

print()


# ==========================================================
# INFORMACIÓN EXTRA
# ==========================================================

print("=" * 70)
print("NAMESPACE")
print("=" * 70)

if root.tag.startswith("{"):

    namespace = root.tag.split("}")[0][1:]

    print(namespace)

else:

    print("No encontrado")