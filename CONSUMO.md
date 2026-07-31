# Consumo programático

Este documento describe cómo descargar y usar los datos del catálogo de forma automatizada.

## Estándares

| Aspecto | Estándar |
|---------|----------|
| Paquete de datos | [Frictionless Data Package](https://specs.frictionlessdata.io/data-package/) (`datapackage.json`) |
| Esquema tabular | [Table Schema](https://specs.frictionlessdata.io/table-schema/) en `schemas/` |
| Fechas | [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) (`YYYY-MM-DD`) |
| Codificación | UTF-8 |
| Licencia | [CC0 1.0](LICENSE) — uso libre sin atribución obligatoria |

## Recursos disponibles

Sustituye `{owner}` y `{branch}` por el repositorio y rama deseados (p. ej. `planaspa` y `main`).

### CSV (fuente de verdad)

| Dataset | URL |
|---------|-----|
| Productos digitales | `https://raw.githubusercontent.com/{owner}/productos-aragoneses/{branch}/listado.csv` |
| E-commerce | `https://raw.githubusercontent.com/{owner}/productos-aragoneses/{branch}/ecommerce.csv` |

### JSON (generado, cómodo para APIs y frontends)

| Dataset | URL |
|---------|-----|
| Productos digitales | `https://raw.githubusercontent.com/{owner}/productos-aragoneses/{branch}/datos/listado.json` |
| E-commerce | `https://raw.githubusercontent.com/{owner}/productos-aragoneses/{branch}/datos/ecommerce.json` |
| Índice de datasets | `https://raw.githubusercontent.com/{owner}/productos-aragoneses/{branch}/datos/catalogo.json` |

### Metadatos

| Recurso | URL |
|---------|-----|
| Data Package | `https://raw.githubusercontent.com/{owner}/productos-aragoneses/{branch}/datapackage.json` |
| Esquema listado | `https://raw.githubusercontent.com/{owner}/productos-aragoneses/{branch}/schemas/listado.schema.json` |
| Esquema e-commerce | `https://raw.githubusercontent.com/{owner}/productos-aragoneses/{branch}/schemas/ecommerce.schema.json` |

## Formato JSON

Cada archivo `datos/*.json` tiene esta estructura:

```json
{
  "nombre": "listado",
  "generado_en": "2026-07-31T12:00:00Z",
  "licencia": "CC0-1.0",
  "total": 50,
  "registros": [
    {
      "id": "cuentica",
      "nombre": "Cuentica",
      "nombre_compania": "Cuentica",
      "ubicacion_sede": "Zaragoza, Zaragoza",
      "descripcion": "...",
      "web": "https://cuentica.com/",
      "fecha_alta": "2026-07-31",
      "ultima_verificacion": "2026-07-31",
      "fuente": "https://cuentica.com/",
      "estado": "activo"
    }
  ]
}
```

Filtra por `estado == "activo"` para obtener solo registros vigentes.

## Ejemplos

### curl

```bash
curl -sL "https://raw.githubusercontent.com/planaspa/productos-aragoneses/main/datos/listado.json" \
  | jq '.registros[] | select(.estado == "activo") | {id, nombre, web}'
```

### Python

```python
import json
from urllib.request import urlopen

URL = "https://raw.githubusercontent.com/planaspa/productos-aragoneses/main/datos/listado.json"

with urlopen(URL) as response:
    data = json.load(response)

activos = [r for r in data["registros"] if r["estado"] == "activo"]
print(f"{len(activos)} productos activos")
```

### JavaScript (fetch)

```javascript
const res = await fetch(
  "https://raw.githubusercontent.com/planaspa/productos-aragoneses/main/datos/listado.json"
);
const { registros } = await res.json();
const activos = registros.filter((r) => r.estado === "activo");
```

### Pandas

```python
import pandas as pd

df = pd.read_csv(
    "https://raw.githubusercontent.com/planaspa/productos-aragoneses/main/listado.csv"
)
activos = df[df["estado"] == "activo"]
por_provincia = activos["ubicacion_sede"].str.split(", ").str[-1].value_counts()
```

### Frictionless (Python)

Con [frictionless](https://framework.frictionlessdata.io/) instalado:

```python
from frictionless import Package

package = Package("datapackage.json")
for resource in package.resources:
    print(resource.name, resource.row_count)
```

## Identificadores estables

Usa el campo `id` como clave primaria. No cambia aunque se renombre el producto. Ejemplo de URL propia:

```
https://planaspa.github.io/productos-aragoneses/#producto/cuentica
```

## Regenerar JSON localmente

Tras editar un CSV:

```bash
python3 scripts/validate.py
python3 scripts/export_json.py
```

El CI del repositorio ejecuta estos pasos en cada PR.

## Versionado

- **CSV**: historial completo en Git; cada commit es una versión.
- **JSON**: regenerado en cada cambio; consulta `generado_en` para saber cuándo se exportó.
- **Cambios relevantes**: ver [CHANGELOG.md](CHANGELOG.md).

## Catálogo web

Exploración humana del dataset: [https://planaspa.github.io/productos-aragoneses/](https://planaspa.github.io/productos-aragoneses/)
