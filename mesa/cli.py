from __future__ import annotations

import argparse
import json

from .engine import MesaEngine
from .models import UserTask


def main() -> None:
    parser = argparse.ArgumentParser(description="MESA - Multifacet Evolutionary Solution Architect")
    parser.add_argument("prompt", help="Problema o tarea a resolver")
    parser.add_argument("--constraint", action="append", default=[])
    parser.add_argument("--preference", action="append", default=[])
    parser.add_argument("--max-generations", type=int, default=2)
    args = parser.parse_args()

    engine = MesaEngine()
    trace = engine.run(
        UserTask(prompt=args.prompt, constraints=args.constraint, preferences=args.preference),
        max_generations=args.max_generations,
    )
    output = {
        "complexity": int(trace.complexity),
        "generations": trace.generations,
        "winner": trace.winner_id,
        "final_solution": trace.final_solution,
        "snapshots": trace.snapshots,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
