[![License: CC0-1.0](https://img.shields.io/badge/License-CC0%201.0-lightgrey.svg)](http://creativecommons.org/publicdomain/zero/1.0/)

# Productos digitales aragoneses

Catálogo abierto de software y e-commerce con sede en Aragón.

| | |
|---|---|
| **Catálogo web** | [planaspa.github.io/productos-aragoneses](https://planaspa.github.io/productos-aragoneses/) |
| **Datos** | [listado.csv](listado.csv) · [ecommerce.csv](ecommerce.csv) |
| **Contribuir** | [CONTRIBUTING.md](CONTRIBUTING.md) |
| **API / JSON** | [CONSUMO.md](CONSUMO.md) |

## Estructura del repositorio

```
listado.csv, ecommerce.csv   ← fuente de verdad (editar aquí)
schemas/                     ← esquema de columnas (Frictionless)
scripts/check.py             ← validar CSV y regenerar JSON
docs/                        ← catálogo web (GitHub Pages)
  index.html, assets/
  datos/*.{csv,json}         ← generado; descarga desde el catálogo web
datapackage.json             ← metadatos del paquete de datos
```

## Criterios de inclusión

1. **Producto digital** (o tienda en `ecommerce.csv`): software con valor para un segmento de clientes.
2. **Aragonés**: sede oficial en un municipio de Aragón.
3. **Activo**: usuarios o clientes de pago a día de hoy.

Definiciones ampliadas en [CONTRIBUTING.md](CONTRIBUTING.md).

## Datos abiertos

Licencia [CC0 1.0](LICENSE). Metadatos en [`datapackage.json`](datapackage.json), esquemas en [`schemas/`](schemas/).

## GitHub Pages

Publicar el catálogo desde **`main`** / carpeta **`/docs`**: [Settings → Pages](https://github.com/planaspa/productos-aragoneses/settings/pages).

## Cambios

Ver [CHANGELOG.md](CHANGELOG.md).
