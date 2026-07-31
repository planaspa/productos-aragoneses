# Changelog

Todos los cambios relevantes del catálogo se documentan aquí.

El formato se inspira en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

## [2.1.0] - 2026-07-31

### Añadido

- Rediseño del catálogo web (tema software + identidad aragonesa)

### Cambiado

- Un solo script de mantenimiento: `scripts/check.py` (validar + exportar JSON)
- JSON único en `docs/datos/` (eliminada copia en `datos/`)
- README, CONTRIBUTING y CONSUMO más breves, con mapa del repositorio

### Eliminado

- Scripts de migración y backfill ya innecesarios
- `catalogo.json` (redundante con `datapackage.json`)
- Workflow de GitHub Actions para Pages (publicación desde `/docs`)

## [2.0.0] - 2026-07-31

### Añadido

- Esquema estándar Frictionless Data Package (`datapackage.json`, `schemas/`)
- Campos de proveniencia: `id`, `fecha_alta`, `ultima_verificacion`, `fuente`, `estado`
- Exportación JSON en `datos/` para consumo programático
- Guía de contribución (`CONTRIBUTING.md`) y documentación de consumo (`CONSUMO.md`)
- Validación automática en CI (`scripts/check.py`)
- Catálogo navegable en GitHub Pages (`docs/`)
- Plantillas de issue y pull request

### Cambiado

- Cabeceras CSV normalizadas a snake_case en español
- Formato de ubicación unificado: `Municipio, Provincia`
- Migración de registros con fechas según historial de Git

### Corregido

- Typo `Husesca` → `Huesca, Huesca` (IriusRisk)
- Nombre `Data Driven Factory?` → `Data Driven Factory`
- Espacio erróneo antes de URL en e-commerce (Aceros de Hispania)
- Ubicaciones incompletas (`Huesca` → `Huesca, Huesca`) en Frogtek, Seycob, Tiendatek y videoo.tv

## [1.x] - histórico

Versiones anteriores con cabeceras en español natural y sin campos de proveniencia. Consultar el historial de Git para detalle.

[2.0.0]: https://github.com/planaspa/productos-aragoneses/compare/v1...v2.0.0
