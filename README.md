[![License: CC0-1.0](https://img.shields.io/badge/License-CC0%201.0-lightgrey.svg)](http://creativecommons.org/publicdomain/zero/1.0/)

# Listado de productos digitales aragoneses en activo

No me des la chapa… ¡Quiero ver el [catálogo navegable](https://planaspa.github.io/productos-aragoneses/)!

| Recurso | Enlace |
|---------|--------|
| Catálogo web | [planaspa.github.io/productos-aragoneses](https://planaspa.github.io/productos-aragoneses/) |
| Productos digitales (CSV) | [listado.csv](listado.csv) |
| E-commerce (CSV) | [ecommerce.csv](ecommerce.csv) |
| JSON / API | [CONSUMO.md](CONSUMO.md) |
| Contribuir | [CONTRIBUTING.md](CONTRIBUTING.md) |

## Objetivo

¿Cuáles son los productos digitales aragoneses más exitosos? ¿Cómo es posible que no lo sepas?

Este listado nace de mi curiosidad personal por descubrir todos aquellos productos digitales de éxito existentes en Aragón, generando una base de conocimiento abierta de la que todos nos podamos nutrir.

## ¿Qué productos digitales aparecen en la lista?

Por ahora la investigación solo permite recopilar productos digitales que cumplan los siguientes tres requisitos:

1. El producto debe cumplir esta [definición](#productos-digitales) de producto digital.
2. El producto debe ser [aragonés](#aragonés).
3. El producto debe seguir estando en activo, lo que implica que posee usuarios utilizándolo de manera activa a día de hoy o pagando por él.

### Productos digitales

¿A qué denominamos producto digital?

* Definimos producto digital como una colección de capacidades software que aporten valor para un segmento de clientes definido.
* Un producto digital puede ser una combinación de capacidades software y datos o puede comprender cualquier combinación de software, hardware, instalaciones y servicios, según sea necesario para brindar la experiencia completa del producto.
* Podemos estar hablando de capacidades software que permitan la realización de una acción repetible o de plataformas digitales.

¿Pueden incluirse en este listado productos con una componente hardware?

* Sí, siempre y cuando el software sea una componente importante de cara al usuario final sin la cual el producto no tiene sentido.

### Aragonés

Buscamos empresas aragonesas con al menos un producto digital de referencia.
Su sede oficial (*headquarters* en inglés si te mola más) debe estar situada actualmente en algún municipio de Aragón.

## Datos abiertos

Este listado se crea de manera abierta con una licencia [CC0 1.0](LICENSE) a toda la comunidad con doble objetivo:

1. Cualquier persona interesada en conocer el ecosistema de productos digitales de Aragón puede acceder libremente a este listado.
2. Cualquier persona que conozca un producto digital puede libremente **ampliar la lista** o editarla para el beneficio de la comunidad.

### Estándares y metadatos

El catálogo sigue el estándar [Frictionless Data Package](https://frictionlessdata.io/):

* [`datapackage.json`](datapackage.json) — descriptor del paquete de datos
* [`schemas/`](schemas/) — esquemas Table Schema (tipos, restricciones, enums)
* Fechas en **ISO 8601** (`YYYY-MM-DD`)
* Identificador estable `id` y campos de proveniencia en cada registro

Consulta [CONSUMO.md](CONSUMO.md) para URLs de descarga directa, ejemplos en Python/JavaScript y formato JSON.

### GitHub Pages

El catálogo web se publica en **https://planaspa.github.io/productos-aragoneses/** mediante GitHub Actions (workflow [`pages.yml`](.github/workflows/pages.yml)).

Si el enlace devuelve 404, actívalo una sola vez:

1. **Settings → Pages**
2. En **Build and deployment → Source**, elige **GitHub Actions**
3. Vuelve a **Actions → Publicar catálogo (GitHub Pages) → Run workflow**

El workflow intenta activar Pages automáticamente (`enablement: true`); si falla, el paso 2 es obligatorio.

## Contribuir

Lee [CONTRIBUTING.md](CONTRIBUTING.md). Resumen:

* Edita el CSV correspondiente y abre un Pull Request, **o**
* Usa el issue template **«Sugerir producto»** si no usas Git

Tras modificar CSVs, ejecuta:

```bash
python3 scripts/validate.py
python3 scripts/export_json.py
```

## Registro de cambios

Ver [CHANGELOG.md](CHANGELOG.md).
