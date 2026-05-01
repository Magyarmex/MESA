# MESA

Implementación funcional inicial de **MESA (Multifacet Evolutionary Solution Architect)**.

## Qué incluye
- Entrevistador (brief enriquecido)
- Juez (contrato de éxito + evaluación por vector de fitness)
- Gobernador (termostato de complejidad + control de reproducción)
- Solores (fundadores y descendientes)
- Reproducción padre congelado + hijos lógico/reparador
- Banco de órganos por donación
- Trazabilidad de snapshots por generación

## Ejecutar
```bash
python -m mesa.cli "Diseña estrategia de lanzamiento para SaaS B2B" --constraint "Presupuesto limitado" --max-generations 2
```

## Tests
```bash
python -m pytest -q
```
