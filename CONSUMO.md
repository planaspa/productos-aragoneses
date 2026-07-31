# Consumo programático

URLs con `{owner}` y `{branch}` (p. ej. `planaspa`, `main`).

## Descarga directa

| Formato | Productos digitales | E-commerce |
|---------|---------------------|------------|
| CSV | [`listado.csv`](https://raw.githubusercontent.com/{owner}/productos-aragoneses/{branch}/listado.csv) | [`ecommerce.csv`](https://raw.githubusercontent.com/{owner}/productos-aragoneses/{branch}/ecommerce.csv) |
| JSON | [`docs/datos/listado.json`](https://raw.githubusercontent.com/{owner}/productos-aragoneses/{branch}/docs/datos/listado.json) | [`docs/datos/ecommerce.json`](https://raw.githubusercontent.com/{owner}/productos-aragoneses/{branch}/docs/datos/ecommerce.json) |

Metadatos: [`datapackage.json`](https://raw.githubusercontent.com/{owner}/productos-aragoneses/{branch}/datapackage.json) · esquemas en [`schemas/`](schemas/).

## Formato JSON

```json
{
  "nombre": "listado",
  "generado_en": "2026-07-31T12:00:00Z",
  "licencia": "CC0-1.0",
  "total": 50,
  "registros": [{ "id": "cuentica", "nombre": "Cuentica", "estado": "activo", "...": "..." }]
}
```

Filtra por `estado == "activo"` para registros vigentes.

## Ejemplos

```bash
# curl + jq
curl -sL "https://raw.githubusercontent.com/planaspa/productos-aragoneses/main/docs/datos/listado.json" \
  | jq '.registros[] | select(.estado == "activo") | {id, nombre, web}'
```

```python
import json
from urllib.request import urlopen

url = "https://raw.githubusercontent.com/planaspa/productos-aragoneses/main/docs/datos/listado.json"
data = json.load(urlopen(url))
activos = [r for r in data["registros"] if r["estado"] == "activo"]
```

```python
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/planaspa/productos-aragoneses/main/listado.csv")
activos = df[df["estado"] == "activo"]
```

## Identificadores

Usa el campo `id` como clave estable (p. ej. `cuentica`). No cambia aunque se renombre el producto.

## Regenerar JSON

Tras editar un CSV:

```bash
python3 scripts/check.py
```
