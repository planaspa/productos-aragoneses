# Guía de contribución

## Formas de contribuir

| Vía | Cuándo |
|-----|--------|
| **Pull Request** editando el CSV | Añadir o corregir datos con Git |
| **Issue «Sugerir producto»** | Sin Git; un mantenedor lo incorpora |

## Criterios

Un registro debe cumplir los [criterios del README](README.md): producto digital, sede en Aragón, activo.

Incluye en el PR o issue:

- URL del producto (`web`)
- URL de evidencia (`fuente`)
- `ultima_verificacion` con la fecha en que comprobaste que sigue activo

## Campos del CSV

| Campo | Descripción |
|-------|-------------|
| `id` | Slug único e **inmutable** (`cuentica`) |
| `nombre` | Nombre comercial |
| `nombre_compania` | Empresa propietaria |
| `ubicacion_sede` | `Municipio, Provincia` |
| `descripcion` | Qué hace el producto o qué vende la tienda |
| `web` | URL pública |
| `fecha_alta` | Fecha de alta en el listado (`YYYY-MM-DD`) |
| `ultima_verificacion` | Última comprobación de actividad |
| `fuente` | URL que acredita la información |
| `estado` | `activo` · `inactivo` · `en_revision` |

Esquemas completos: [`schemas/`](schemas/).

## Añadir un registro

1. Edita [`listado.csv`](listado.csv) o [`ecommerce.csv`](ecommerce.csv).
2. Añade una fila al final. Ejemplo:

```csv
mi-producto,Mi Producto,Mi Empresa SL,"Calatayud, Zaragoza",Descripción breve.,https://ejemplo.com,2026-01-15,2026-01-15,https://ejemplo.com,activo
```

3. Ejecuta `python3 scripts/check.py` y abre un PR.

## Baja lógica

No borres filas. Cambia `estado` a `inactivo` y actualiza `ultima_verificacion`.

## Validación

El CI ejecuta `scripts/check.py`: valida el esquema y comprueba que el JSON esté sincronizado.

## Más información

- [Consumo programático](CONSUMO.md)
- [Catálogo web](https://planaspa.github.io/productos-aragoneses/)
