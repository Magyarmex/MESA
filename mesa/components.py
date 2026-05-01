from __future__ import annotations

from dataclasses import dataclass, field
import itertools

from .models import (
    Brief,
    ComplexityLevel,
    FitnessVector,
    Genotype,
    Organ,
    Phenotype,
    Solor,
    SolorState,
    SuccessContract,
    UserTask,
)


class Interviewer:
    def enrich(self, task: UserTask) -> Brief:
        inferred = len(task.constraints) == 0
        constraints = task.constraints or ["Mantener claridad", "Evitar relleno"]
        context = "Tarea recibida y normalizada para ejecución evolutiva"
        return Brief(
            objective=task.prompt,
            context=context,
            constraints=constraints,
            preferences=task.preferences,
            anti_preferences=task.anti_preferences,
            inferred=inferred,
        )


class Judge:
    def build_contract(self, brief: Brief) -> SuccessContract:
        criteria = {
            "utility": 0.2,
            "precision": 0.1,
            "feasibility": 0.15,
            "originality": 0.05,
            "evidence": 0.1,
            "robustness": 0.15,
            "clarity": 0.1,
            "efficiency": 0.05,
            "alignment": 0.1,
        }
        return SuccessContract(
            objective=brief.objective,
            constraints=brief.constraints,
            criteria=criteria,
            risks=["Supuestos incompletos", "Sobreajuste a forma vs valor"],
            assumptions=["Contexto parcial", "Sin verificación externa automática"],
            bad_outcome="Salida convincente pero no accionable",
        )

    def evaluate(self, solor: Solor, contract: SuccessContract) -> FitnessVector:
        text = solor.phenotype.proposal.lower()
        utility = min(1.0, 0.4 + 0.1 * len(solor.phenotype.execution_plan))
        precision = 0.7 if "supuesto" in text else 0.62
        feasibility = 0.75 if len(solor.phenotype.execution_plan) >= 3 else 0.6
        originality = 0.65 if "alternativa" in text else 0.5
        evidence = min(1.0, 0.55 + 0.1 * len([o for o in solor.organs if o.evidence]))
        robustness = 0.72 if solor.phenotype.mitigations else 0.55
        clarity = 0.8 if len(solor.phenotype.proposal) < 1400 else 0.6
        efficiency = max(0.45, 0.9 - solor.budget_used)
        alignment = 0.78 if all(c for c in contract.constraints) else 0.65
        fitness = FitnessVector(
            utility, precision, feasibility, originality, evidence, robustness, clarity, efficiency, alignment
        )
        solor.fitness = fitness
        solor.judge_feedback = (
            f"Fortalezas: utilidad={utility:.2f}, claridad={clarity:.2f}. "
            f"Mejorar evidencia y robustez con pruebas concretas."
        )
        return fitness


@dataclass
class OrganBank:
    organs: list[Organ] = field(default_factory=list)

    def donate(self, organ: Organ) -> None:
        self.organs.append(organ)

    def best_match(self, role: str) -> list[Organ]:
        return [o for o in self.organs if role in o.compatibilities or not o.compatibilities][:2]


class Governor:
    def choose_complexity(self, task: UserTask) -> ComplexityLevel:
        prompt_len = len(task.prompt)
        if prompt_len < 80 and not task.constraints:
            return ComplexityLevel.AGENT
        if prompt_len < 220:
            return ComplexityLevel.SIMPLE_SOLOR
        if prompt_len < 380:
            return ComplexityLevel.LIGHT_COMPETITION
        return ComplexityLevel.REDUCED_EVOLUTION

    def founder_count(self, level: ComplexityLevel) -> int:
        return {0: 1, 1: 1, 2: 3, 3: 3, 4: 4}[int(level)]

    def should_reproduce(self, solor: Solor) -> bool:
        return bool(solor.fitness and solor.fitness.score() > 0.68 and solor.state == SolorState.ACTIVE)


class SolorFactory:
    _counter = itertools.count(1)

    def create_founder(self, brief: Brief, generation: int, role: str) -> Solor:
        solor_id = f"S{next(self._counter)}"
        genotype = Genotype(
            central_approach=role,
            assumptions=["Usuario busca valor accionable"],
            priorities=["utilidad", "claridad", "riesgo"],
            strategy=f"Explorar enfoque {role} con validación explícita",
            style="structured",
        )
        phenotype = Phenotype(
            proposal=f"Propuesta inicial basada en {role} con alternativa y supuestos declarados.",
            thesis=f"El enfoque {role} maximiza valor por recurso.",
            execution_plan=[
                "Definir objetivo operativo",
                "Diseñar alternativa principal",
                "Comparar tradeoffs",
                "Emitir recomendación",
            ],
            risks=["Ambigüedad en requerimientos"],
            mitigations=["Feedback iterativo del juez"],
        )
        organs = [
            Organ(
                name="tesis",
                function="alinear decisión",
                content=phenotype.thesis,
                confidence=0.72,
                evidence="Basado en contrato de éxito",
                compatibilities=[role],
            )
        ]
        return Solor(solor_id, generation, role, brief.objective, genotype, phenotype, organs)

    def spawn_child(self, parent: Solor, kind: str) -> Solor:
        child = self.create_founder(
            Brief(parent.task, "", [], [], [], True), parent.generation + 1, role=f"{parent.role}-{kind}"
        )
        child.genotype.lineage = [parent.solor_id]
        child.genotype.mutations.append(kind)
        child.history.append(f"Hijo {kind} de {parent.solor_id}")
        return child
