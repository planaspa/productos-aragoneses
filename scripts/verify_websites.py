#!/usr/bin/env python3
"""Comprueba la disponibilidad de las URLs y marca registros inactivos."""

from __future__ import annotations

import csv
import ssl
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATASETS = ["listado.csv", "ecommerce.csv"]
TODAY = date.today().isoformat()
TIMEOUT = 10
WORKERS = 8

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; ProductosAragonesesBot/1.0; "
        "+https://github.com/planaspa/productos-aragoneses)"
    )
}


def check_url(url: str) -> tuple[bool, str]:
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=SSL_CTX) as resp:
            code = resp.getcode()
            if 200 <= code < 400:
                return True, f"HTTP {code}"
            return False, f"HTTP {code}"
    except urllib.error.HTTPError as exc:
        code = exc.code
        if code in (401, 403, 405, 429):
            return True, f"HTTP {code} (acceso restringido)"
        return False, f"HTTP {code}"
    except urllib.error.URLError as exc:
        reason = exc.reason if hasattr(exc, "reason") else exc
        return False, f"URL error: {reason}"
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def load_active_records() -> list[tuple[str, dict[str, str]]]:
    records: list[tuple[str, dict[str, str]]] = []
    for csv_name in DATASETS:
        csv_path = ROOT / csv_name
        with csv_path.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                if row["estado"] == "activo":
                    records.append((csv_name, row))
    return records


def update_csv(csv_name: str, inactive_ids: set[str]) -> int:
    if not inactive_ids:
        return 0

    csv_path = ROOT / csv_name
    with csv_path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        rows = list(reader)

    updated = 0
    for row in rows:
        if row["id"] in inactive_ids:
            row["estado"] = "inactivo"
            row["ultima_verificacion"] = TODAY
            updated += 1

    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return updated


def main() -> int:
    records = load_active_records()
    inactive_by_csv: dict[str, set[str]] = {name: set() for name in DATASETS}
    active_count = 0

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        future_map = {
            pool.submit(check_url, row["web"]): (csv_name, row)
            for csv_name, row in records
        }
        for future in as_completed(future_map):
            csv_name, row = future_map[future]
            active, reason = future.result()
            status = "OK" if active else "INACTIVE"
            print(f"[{status}] {row['id']}: {reason} - {row['web']}", flush=True)
            if active:
                active_count += 1
            else:
                inactive_by_csv[csv_name].add(row["id"])

    inactive_total = sum(len(ids) for ids in inactive_by_csv.values())
    print(f"\n--- Summary ---", flush=True)
    print(f"Total checked: {len(records)}", flush=True)
    print(f"Active: {active_count}", flush=True)
    print(f"Inactive: {inactive_total}", flush=True)

    if inactive_total == 0:
        print("No CSV changes needed.", flush=True)
        return 0

    print("\nUpdating CSV files...", flush=True)
    for csv_name, ids in inactive_by_csv.items():
        if ids:
            count = update_csv(csv_name, ids)
            print(f"  {csv_name}: marked {count} record(s) as inactivo", flush=True)
            for row_id in sorted(ids):
                print(f"    - {row_id}", flush=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
