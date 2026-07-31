#!/usr/bin/env python3
"""Migra CSVs al esquema estándar con id, proveniencia y fechas ISO 8601."""

from __future__ import annotations

import csv
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIGRATION_DATE = "2026-07-31"

LISTADO_OLD_HEADERS = [
    "Nombre del producto",
    "Nombre de la compañía",
    "Ubicación de la sede",
    "Descripción del producto",
    "Web del producto",
]

ECOMMERCE_OLD_HEADERS = [
    "Nombre del eCommerce",
    "Nombre de la compañía",
    "Ubicación de la sede",
    "Productos comercializados",
    "Web del eCommerce",
]

STANDARD_HEADERS = [
    "id",
    "nombre",
    "nombre_compania",
    "ubicacion_sede",
    "descripcion",
    "web",
    "fecha_alta",
    "ultima_verificacion",
    "fuente",
    "estado",
]

# Correcciones manuales de calidad de datos
LOCATION_FIXES = {
    "Zaragoza": "Zaragoza, Zaragoza",
    "Jaca": "Jaca, Huesca",
    "Huesca": "Huesca, Huesca",
    "Teruel": "Teruel, Teruel",
}

NAME_FIXES = {
    "Data Driven Factory?": "Data Driven Factory",
}

SLUG_OVERRIDES = {
    "E-normative software": "e-normative",
    "Flip&Flip": "flip-and-flip",
    "La Finesse Truffles": "la-finesse-truffles",
    "Central de reservas": "central-de-reservas",
    "Aceros de Hispania": "aceros-de-hispania",
}


def slugify(text: str) -> str:
    if text in SLUG_OVERRIDES:
        return SLUG_OVERRIDES[text]
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_text.lower()).strip("-")
    return slug or "sin-id"


def normalize_location(location: str) -> str:
    location = location.strip()
    if location in LOCATION_FIXES:
        return LOCATION_FIXES[location]
    if "," in location:
        parts = [p.strip() for p in location.split(",", 1)]
        return f"{parts[0]}, {parts[1]}"
    return location


def normalize_url(url: str) -> str:
    return url.strip()


def migrate_row(name: str, company: str, location: str, description: str, web: str) -> dict:
    name = NAME_FIXES.get(name, name)
    web = normalize_url(web)
    return {
        "id": slugify(name),
        "nombre": name,
        "nombre_compania": company.strip(),
        "ubicacion_sede": normalize_location(location),
        "descripcion": description.strip(),
        "web": web,
        "fecha_alta": MIGRATION_DATE,
        "ultima_verificacion": MIGRATION_DATE,
        "fuente": web,
        "estado": "activo",
    }


def read_legacy_csv(path: Path, name_col: str) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                migrate_row(
                    row[name_col],
                    row["Nombre de la compañía"],
                    row["Ubicación de la sede"],
                    row[[k for k in row if "Descripción" in k or "Productos" in k][0]],
                    row[[k for k in row if "Web" in k][0]],
                )
            )
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=STANDARD_HEADERS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    listado = read_legacy_csv(ROOT / "listado.csv", "Nombre del producto")
    ecommerce = read_legacy_csv(ROOT / "ecommerce.csv", "Nombre del eCommerce")

    ids = [row["id"] for row in listado + ecommerce]
    duplicates = {i for i in ids if ids.count(i) > 1}
    if duplicates:
        raise SystemExit(f"IDs duplicados detectados: {sorted(duplicates)}")

    write_csv(ROOT / "listado.csv", listado)
    write_csv(ROOT / "ecommerce.csv", ecommerce)
    print(f"Migrados {len(listado)} productos digitales y {len(ecommerce)} e-commerce.")


if __name__ == "__main__":
    main()
