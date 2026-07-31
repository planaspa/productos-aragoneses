# Guía de contribución

¡Gracias por ayudar a mantener el catálogo de productos digitales y e-commerce aragoneses! Esta guía explica cómo aportar datos de forma correcta.

## Formas de contribuir

Puedes elegir la vía que te resulte más cómoda:

| Vía | Cuándo usarla |
|-----|---------------|
| **Pull Request** editando el CSV | Si conoces Git y quieres añadir o corregir datos directamente |
| **Issue «Sugerir producto»** | Si no usas Git pero quieres proponer un alta o corrección |
| **Correcciones menores** | Typo en descripción, URL rota, sede mal escrita → PR o issue |

## Criterios de inclusión

Un registro debe cumplir **los tres** requisitos del [README](README.md):

1. **Producto digital** (o tienda online en `ecommerce.csv`): software que aporta valor a un segmento de clientes. Se admite hardware si el software es esencial para el usuario final.
2. **Aragonés**: la sede oficial (*headquarters*) está en un municipio de Aragón.
3. **Activo**: tiene usuarios activos o clientes de pago a día de hoy.

### Evidencia mínima

Al proponer un alta, incluye al menos:

- URL del producto o tienda (campo `web`)
- URL que acredite la sede o la actividad (campo `fuente`; puede ser la misma `web`, la web corporativa o un registro público)
- Fecha en que comprobaste que sigue activo (campo `ultima_verificacion`, formato `YYYY-MM-DD`)

## Esquema de datos

Los datasets siguen el estándar [Frictionless Data Package](https://frictionlessdata.io/) con fechas en **ISO 8601** (`YYYY-MM-DD`).

| Campo | Obligatorio | Descripción |
|-------|-------------|-------------|
| `id` | Sí | Identificador estable en minúsculas y guiones (p. ej. `cuentica`). **No cambiar** una vez publicado. |
| `nombre` | Sí | Nombre comercial del producto o tienda. |
| `nombre_compania` | Sí | Empresa propietaria. |
| `ubicacion_sede` | Sí | Formato **`Municipio, Provincia`** (p. ej. `Zaragoza, Zaragoza`, `Jaca, Huesca`). |
| `descripcion` | Sí | Resumen del valor que aporta (español preferido). |
| `web` | Sí | URL pública del producto (`https://` preferido). |
| `fecha_alta` | Sí | Fecha de incorporación al listado (`YYYY-MM-DD`). |
| `ultima_verificacion` | Sí | Última comprobación de que sigue activo. |
| `fuente` | Sí | URL que acredita la información. |
| `estado` | Sí | `activo`, `inactivo` o `en_revision`. |

Esquemas completos: [`schemas/listado.schema.json`](schemas/listado.schema.json) y [`schemas/ecommerce.schema.json`](schemas/ecommerce.schema.json).

## Añadir un producto digital

1. Haz fork del repositorio y crea una rama.
2. Abre [`listado.csv`](listado.csv) y añade **una fila al final** con este ejemplo:

```csv
mi-producto,Mi Producto,Mi Empresa SL,"Calatayud, Zaragoza",Descripción breve del producto.,https://ejemplo.com/producto,2026-07-31,2026-07-31,https://ejemplo.com/producto,activo
```

3. Genera un `id` único:
   - Solo minúsculas, números y guiones
   - Sin acentos ni espacios (`Mi Producto` → `mi-producto`)
   - Comprueba que no exista ya en el CSV
4. Ejecuta la validación local (opcional pero recomendado):

```bash
python3 scripts/validate.py
python3 scripts/export_json.py
```

5. Abre un Pull Request usando la plantilla incluida.

## Añadir un e-commerce

Mismo proceso en [`ecommerce.csv`](ecommerce.csv). El campo `descripcion` describe los productos comercializados.

## Modificar o dar de baja un registro

- **Corrección de datos**: edita la fila correspondiente y actualiza `ultima_verificacion`.
- **Producto inactivo**: cambia `estado` a `inactivo` y actualiza `ultima_verificacion`. **No borres la fila**; así conservamos el historial.
- **Duda sobre criterios**: cambia `estado` a `en_revision` y explica el caso en el PR o issue.

## Reglas del identificador (`id`)

- Se asigna **una sola vez** al crear el registro.
- **Nunca renombrar** un `id` existente aunque cambie el nombre comercial.
- Si un producto desaparece y otro ocupa su URL, son registros distintos con `id` distintos.

## Validación automática

Cada Pull Request ejecuta una comprobación que verifica:

- Cabeceras y tipos según el esquema
- Formato de fechas ISO 8601
- URLs válidas (`http`/`https`)
- `id` únicos
- Formato de `ubicacion_sede` (`Municipio, Provincia`)

## Convenciones de estilo

- Codificación **UTF-8**
- Separador **coma**; campos con comas entre comillas dobles
- Descripciones en **español** cuando sea posible
- URLs sin espacios al inicio o final
- Una fila = un producto o tienda

## Dudas abiertas / decisiones del mantenedor

Si no estás seguro de si un producto cumple los criterios, abre un issue antes del PR. Casos habituales:

- Empresa con sede en Aragón pero producto desarrollado fuera
- Producto con varias marcas comerciales (un registro por producto)
- Filial vs. sede matriz

## Más información

- [Consumo programático de los datos](CONSUMO.md)
- [Registro de cambios](CHANGELOG.md)
- [Catálogo navegable (GitHub Pages)](https://planaspa.github.io/productos-aragoneses/)
