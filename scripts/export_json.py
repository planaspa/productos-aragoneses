#!/usr/bin/env python3
"""Exporta CSVs a JSON y copia artefactos para GitHub Pages."""

from __future__ import annotations

import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATASETS = ["listado", "ecommerce"]
DATOS_DIR = ROOT / "datos"
DOCS_DATOS_DIR = ROOT / "docs" / "datos"


def csv_to_records(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def export_dataset(name: str) -> dict:
    records = csv_to_records(ROOT / f"{name}.csv")
    payload = {
        "nombre": name,
        "generado_en": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "licencia": "CC0-1.0",
        "total": len(records),
        "registros": records,
    }
    return payload


def main() -> None:
    DATOS_DIR.mkdir(exist_ok=True)
    DOCS_DATOS_DIR.mkdir(parents=True, exist_ok=True)

    catalog = {
        "nombre": "productos-aragoneses",
        "generado_en": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "licencia": "CC0-1.0",
        "datasets": {},
    }

    for name in DATASETS:
        payload = export_dataset(name)
        json_path = DATOS_DIR / f"{name}.json"
        with json_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        shutil.copy2(json_path, DOCS_DATOS_DIR / f"{name}.json")
        catalog["datasets"][name] = {
            "total": payload["total"],
            "csv": f"{name}.csv",
            "json": f"datos/{name}.json",
        }

    catalog_path = DATOS_DIR / "catalogo.json"
    with catalog_path.open("w", encoding="utf-8") as handle:
        json.dump(catalog, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    shutil.copy2(catalog_path, DOCS_DATOS_DIR / "catalogo.json")

    print(f"Exportados {len(DATASETS)} datasets a {DATOS_DIR}/ y {DOCS_DATOS_DIR}/")


if __name__ == "__main__":
    main()
