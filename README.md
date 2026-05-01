# MESA

Implementación funcional de **MESA (Multifacet Evolutionary Solution Architect)** con backend evolutivo y frontend HTML.

## Incluye
- Entrevistador (brief enriquecido)
- Juez (contrato de éxito + fitness vectorial)
- Gobernador (termostato + reproducción)
- Solores (fundadores/descendientes)
- Banco de órganos
- Trazabilidad por snapshots
- Interfaz web HTML/JS para interactuar con el sistema

## Ejecutar interfaz web
```bash
python -m mesa.webapp
```
Luego abre: `http://127.0.0.1:8000`

## Ejecutar por CLI
```bash
python -m mesa.cli "Diseña estrategia de lanzamiento para SaaS B2B" --constraint "Presupuesto limitado" --max-generations 2
```

## Tests
```bash
python -m pytest -q
```
