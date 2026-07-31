#!/usr/bin/env python3
"""Valida CSVs contra los esquemas Frictionless del repositorio."""

from __future__ import annotations

import csv
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"
DATASETS = {
    "listado.csv": SCHEMAS / "listado.schema.json",
    "ecommerce.csv": SCHEMAS / "ecommerce.schema.json",
}

ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ESTADOS = {"activo", "inactivo", "en_revision"}


def load_schema(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_type(value: str, field_type: str) -> bool:
    if field_type == "string":
        return True
    if field_type == "date":
        if not ISO_DATE.match(value):
            return False
        try:
            date.fromisoformat(value)
        except ValueError:
            return False
        return True
    if field_type == "anyuri":
        parsed = urlparse(value)
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
    return True


def validate_enum(value: str, options: list[str]) -> bool:
    return value in options


def validate_constraints(value: str, constraints: dict) -> list[str]:
    errors: list[str] = []
    if constraints.get("required") and not value.strip():
        errors.append("campo obligatorio vacío")
    if "maxLength" in constraints and len(value) > constraints["maxLength"]:
        errors.append(f"supera maxLength ({constraints['maxLength']})")
    if "pattern" in constraints and not re.match(constraints["pattern"], value):
        errors.append(f"no cumple el patrón {constraints['pattern']}")
    if "enum" in constraints and not validate_enum(value, constraints["enum"]):
        errors.append(f"valor no permitido; use uno de {constraints['enum']}")
    return errors


def validate_csv(csv_path: Path, schema_path: Path) -> list[str]:
    schema = load_schema(schema_path)
    fields = {field["name"]: field for field in schema["fields"]}
    errors: list[str] = []
    seen_ids: set[str] = set()

    with csv_path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != list(fields.keys()):
            errors.append(
                f"cabeceras incorrectas: {reader.fieldnames}; "
                f"esperado: {list(fields.keys())}"
            )
            return errors

        for line_no, row in enumerate(reader, start=2):
            row_id = row.get("id", "")
            if row_id in seen_ids:
                errors.append(f"línea {line_no}: id duplicado '{row_id}'")
            seen_ids.add(row_id)

            for name, spec in fields.items():
                value = row.get(name, "")
                field_errors = validate_constraints(value, spec.get("constraints", {}))
                if value and not validate_type(value, spec["type"]):
                    field_errors.append(f"tipo inválido ({spec['type']})")
                for err in field_errors:
                    errors.append(f"línea {line_no}, campo '{name}': {err}")

    return errors


def main() -> int:
    all_errors: list[str] = []
    for csv_name, schema_path in DATASETS.items():
        csv_path = ROOT / csv_name
        if not csv_path.exists():
            all_errors.append(f"no existe {csv_name}")
            continue
        all_errors.extend(
            f"[{csv_name}] {err}" for err in validate_csv(csv_path, schema_path)
        )

    if all_errors:
        print("Errores de validación:")
        for err in all_errors:
            print(f"  - {err}")
        return 1

    print("Validación correcta: todos los datasets cumplen el esquema.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
