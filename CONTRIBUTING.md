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

El CI ejecuta `scripts/check.py` y comprueba que `docs/datos/` coincida con lo generado a partir de los CSV.

### Flujo obligatorio al editar datos

1. Modifica solo los CSV de origen (`listado.csv` o `ecommerce.csv`).
2. Ejecuta **una vez** `python3 scripts/check.py`.
3. Incluye en el commit **tanto el CSV como** los artefactos regenerados en `docs/datos/` (`*.csv` y `*.json`).

```bash
python3 scripts/check.py
git add listado.csv ecommerce.csv docs/datos/
```

4. Comprueba localmente que el JSON está sincronizado (debe no mostrar diferencias):

```bash
python3 scripts/check.py && git diff --exit-code docs/datos/
```

### Por qué falla el CI con «Ejecuta: python3 scripts/check.py»

| Causa | Qué hacer |
|-------|-----------|
| No ejecutaste `check.py` tras editar el CSV | Ejecuta el script y commitea `docs/datos/`. |
| Solo commiteaste el CSV, no el JSON | Añade `docs/datos/listado.json`, `listado.csv`, etc. |
| Editaste a mano `docs/datos/*.json` | No edites esos ficheros; regenera con el script. |
| Cambiaste datos pero no `ultima_verificacion` | Actualiza esa fecha al verificar el producto; el JSON usa la fecha más reciente del CSV como `generado_en`. |

Los JSON en `docs/datos/` **no son fuente de verdad**: se generan automáticamente. El campo `generado_en` se calcula de forma estable a partir de la `ultima_verificacion` más reciente de cada dataset, no del reloj del sistema, para que CI y desarrollo local produzcan el mismo resultado.

### Qué valida el CI

1. Esquema Frictionless de los CSV (`schemas/*.schema.json`).
2. Regeneración de `docs/datos/` con `scripts/check.py`.
3. Que no queden diferencias respecto al repositorio (`git diff --exit-code docs/datos/`).

## Más información

- [Consumo programático](CONSUMO.md)
- [Catálogo web](https://planaspa.github.io/productos-aragoneses/)
