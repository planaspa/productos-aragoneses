#!/usr/bin/env python3
"""Valida los CSV y regenera el JSON del catálogo web."""

from __future__ import annotations

import csv
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"
JSON_DIR = ROOT / "docs" / "datos"
DATASETS = ["listado", "ecommerce"]
CSV_SCHEMAS = {
    "listado.csv": SCHEMAS / "listado.schema.json",
    "ecommerce.csv": SCHEMAS / "ecommerce.schema.json",
}
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


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


def validate_constraints(value: str, constraints: dict) -> list[str]:
    errors: list[str] = []
    if constraints.get("required") and not value.strip():
        errors.append("campo obligatorio vacío")
    if "maxLength" in constraints and len(value) > constraints["maxLength"]:
        errors.append(f"supera maxLength ({constraints['maxLength']})")
    if "pattern" in constraints and not re.match(constraints["pattern"], value):
        errors.append(f"no cumple el patrón {constraints['pattern']}")
    if "enum" in constraints and value not in constraints["enum"]:
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
            return [
                f"cabeceras incorrectas: {reader.fieldnames}; "
                f"esperado: {list(fields.keys())}"
            ]

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


def validate_all() -> list[str]:
    errors: list[str] = []
    for csv_name, schema_path in CSV_SCHEMAS.items():
        csv_path = ROOT / csv_name
        if not csv_path.exists():
            errors.append(f"no existe {csv_name}")
            continue
        errors.extend(f"[{csv_name}] {err}" for err in validate_csv(csv_path, schema_path))
    return errors


def generated_timestamp(records: list[dict[str, str]]) -> str:
    """Marca de tiempo estable derivada de los datos, no del reloj del sistema."""
    dates = [row["ultima_verificacion"] for row in records if row.get("ultima_verificacion")]
    if not dates:
        return "1970-01-01T00:00:00Z"
    return f"{max(dates)}T00:00:00Z"


def export_artifacts() -> None:
    JSON_DIR.mkdir(parents=True, exist_ok=True)

    for name in DATASETS:
        csv_src = ROOT / f"{name}.csv"
        shutil.copy2(csv_src, JSON_DIR / f"{name}.csv")

        with csv_src.open(encoding="utf-8", newline="") as handle:
            records = list(csv.DictReader(handle))

        payload = {
            "nombre": name,
            "generado_en": generated_timestamp(records),
            "licencia": "CC0-1.0",
            "total": len(records),
            "registros": records,
        }
        path = JSON_DIR / f"{name}.json"
        with path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")


def main() -> int:
    errors = validate_all()
    if errors:
        print("Errores de validación:")
        for err in errors:
            print(f"  - {err}")
        return 1

    export_artifacts()
    print("OK: CSV válidos y artefactos actualizados en docs/datos/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
