from __future__ import annotations

from dataclasses import dataclass, field

from .components import Governor, Interviewer, Judge, OrganBank, SolorFactory
from .models import ComplexityLevel, Solor, SolorState, UserTask


@dataclass
class RunTrace:
    complexity: ComplexityLevel
    generations: int
    snapshots: list[dict] = field(default_factory=list)
    winner_id: str = ""
    final_solution: str = ""


class MesaEngine:
    def __init__(self) -> None:
        self.interviewer = Interviewer()
        self.judge = Judge()
        self.governor = Governor()
        self.factory = SolorFactory()
        self.organ_bank = OrganBank()

    def run(self, task: UserTask, max_generations: int = 2) -> RunTrace:
        brief = self.interviewer.enrich(task)
        contract = self.judge.build_contract(brief)
        level = self.governor.choose_complexity(task)
        founders = [
            self.factory.create_founder(brief, 0, role)
            for role in ["analítico", "creativo", "riesgo"][: self.governor.founder_count(level)]
        ]

        population: list[Solor] = founders
        trace = RunTrace(complexity=level, generations=0)

        for generation in range(max_generations):
            trace.generations = generation + 1
            next_population: list[Solor] = []
            for solor in population:
                fitness = self.judge.evaluate(solor, contract)
                solor.pheromones = {
                    "quality": fitness.score(),
                    "improvement": 0.2 + generation * 0.1,
                    "diversity": 0.6 if "creativo" in solor.role else 0.4,
                }
                solor.budget_used += 0.12
                trace.snapshots.append(solor.snapshot())
                if self.governor.should_reproduce(solor) and generation + 1 < max_generations:
                    solor.state = SolorState.FROZEN
                    logical = self.factory.spawn_child(solor, "logico")
                    repair = self.factory.spawn_child(solor, "reparador")
                    next_population.extend([solor, logical, repair])
                else:
                    next_population.append(solor)

                if solor.fitness and solor.fitness.score() < 0.63:
                    solor.state = SolorState.DISCARDED
                    for organ in solor.organs:
                        organ.state = "donable"
                        self.organ_bank.donate(organ)

            population = [p for p in next_population if p.state != SolorState.DISCARDED]

        winner = max(population, key=lambda s: s.fitness.score() if s.fitness else 0.0)
        winner.state = SolorState.FINISHED
        trace.winner_id = winner.solor_id
        trace.final_solution = self._synthesize_final(population)
        return trace

    def _synthesize_final(self, population: list[Solor]) -> str:
        ranked = sorted(population, key=lambda s: s.fitness.score() if s.fitness else 0.0, reverse=True)
        top = ranked[:2]
        parts = [f"[{s.solor_id}/{s.role}] {s.phenotype.proposal}" for s in top]
        return "\n".join(parts) + "\nSíntesis: recomendación robusta con tradeoffs explícitos."
