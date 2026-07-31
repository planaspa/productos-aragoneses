#!/usr/bin/env python3
"""Asigna fecha_alta y ultima_verificacion según el primer commit de Git."""

from __future__ import annotations

import csv
import io
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DATASETS = {
    "listado.csv": [
        "Nombre del producto",
        "nombre",
    ],
    "ecommerce.csv": [
        "Nombre del eCommerce",
        "nombre",
    ],
}


def git_commits(path: str) -> list[tuple[str, str]]:
    output = subprocess.check_output(
        ["git", "log", "--reverse", "--format=%H|%as", "--", path],
        cwd=ROOT,
        text=True,
    ).strip()
    if not output:
        return []
    return [tuple(line.split("|", 1)) for line in output.splitlines()]


def read_csv_at_commit(commit: str, path: str) -> list[dict]:
    try:
        content = subprocess.check_output(
            ["git", "show", f"{commit}:{path}"],
            cwd=ROOT,
            text=True,
        )
    except subprocess.CalledProcessError:
        return []

    reader = csv.DictReader(io.StringIO(content))
    return list(reader)


def record_key(row: dict, name_fields: list[str]) -> str | None:
    web = next(
        (v.strip() for k, v in row.items() if k and k.lower().startswith("web") and v),
        None,
    )
    if web:
        return web.rstrip("/").lower()

    for field in name_fields:
        value = row.get(field)
        if value and value.strip():
            return value.strip().lower()

    for key, value in row.items():
        if key and "nombre" in key.lower() and "compa" not in key.lower() and value and value.strip():
            return value.strip().lower()

    return None


def first_seen_dates(path: str, name_fields: list[str]) -> dict[str, str]:
    seen: dict[str, str] = {}
    for commit, date in git_commits(path):
        for row in read_csv_at_commit(commit, path):
            key = record_key(row, name_fields)
            if key and key not in seen:
                seen[key] = date
    return seen


def update_csv(path: Path, dates: dict[str, str], name_fields: list[str]) -> list[str]:
    missing: list[str] = []
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    for row in rows:
        key = record_key(row, name_fields)
        if key and key in dates:
            row["fecha_alta"] = dates[key]
            row["ultima_verificacion"] = dates[key]
        else:
            missing.append(row.get("id") or row.get("nombre") or key or "?")

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    return missing


def main() -> int:
    all_missing: list[str] = []
    for filename, name_fields in DATASETS.items():
        path = ROOT / filename
        dates = first_seen_dates(filename, name_fields)
        missing = update_csv(path, dates, name_fields)
        all_missing.extend(f"{filename}: {item}" for item in missing)
        print(f"{filename}: {len(dates)} fechas históricas, {len(missing)} sin match")

    if all_missing:
        print("Sin fecha histórica:", file=sys.stderr)
        for item in all_missing:
            print(f"  - {item}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
