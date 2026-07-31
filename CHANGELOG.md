# Changelog

Todos los cambios relevantes del catálogo se documentan aquí.

El formato se inspira en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

## [2.0.0] - 2026-07-31

### Añadido

- Esquema estándar Frictionless Data Package (`datapackage.json`, `schemas/`)
- Campos de proveniencia: `id`, `fecha_alta`, `ultima_verificacion`, `fuente`, `estado`
- Exportación JSON en `datos/` para consumo programático
- Guía de contribución (`CONTRIBUTING.md`) y documentación de consumo (`CONSUMO.md`)
- Validación automática en CI y scripts locales (`scripts/validate.py`, `scripts/export_json.py`)
- Catálogo navegable en GitHub Pages (`docs/`)
- Plantillas de issue y pull request

### Cambiado

- Cabeceras CSV normalizadas a snake_case en español
- Formato de ubicación unificado: `Municipio, Provincia`
- Migración de registros existentes con `fecha_alta` y `ultima_verificacion` según la fecha del primer commit en Git (`scripts/backfill_dates.py`)

### Corregido

- Typo `Husesca` → `Huesca, Huesca` (IriusRisk)
- Nombre `Data Driven Factory?` → `Data Driven Factory`
- Espacio erróneo antes de URL en e-commerce (Aceros de Hispania)
- Ubicaciones incompletas (`Huesca` → `Huesca, Huesca`) en Frogtek, Seycob, Tiendatek y videoo.tv

## [1.x] - histórico

Versiones anteriores con cabeceras en español natural y sin campos de proveniencia. Consultar el historial de Git para detalle.

[2.0.0]: https://github.com/planaspa/productos-aragoneses/compare/v1...v2.0.0
