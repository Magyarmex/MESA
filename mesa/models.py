from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ComplexityLevel(int, Enum):
    AGENT = 0
    SIMPLE_SOLOR = 1
    LIGHT_COMPETITION = 2
    REDUCED_EVOLUTION = 3
    FULL_MESA = 4


class SolorState(str, Enum):
    ACTIVE = "active"
    REVIEWING = "reviewing"
    FINISHED = "finished"
    DISCARDED = "discarded"
    FROZEN = "frozen"


@dataclass
class UserTask:
    prompt: str
    constraints: list[str] = field(default_factory=list)
    preferences: list[str] = field(default_factory=list)
    anti_preferences: list[str] = field(default_factory=list)
    risk_tolerance: str = "medium"
    desired_format: str = "structured"


@dataclass
class Brief:
    objective: str
    context: str
    constraints: list[str]
    preferences: list[str]
    anti_preferences: list[str]
    inferred: bool


@dataclass
class SuccessContract:
    objective: str
    constraints: list[str]
    criteria: dict[str, float]
    risks: list[str]
    assumptions: list[str]
    bad_outcome: str


@dataclass
class Organ:
    name: str
    function: str
    content: str
    confidence: float
    evidence: str
    dependencies: list[str] = field(default_factory=list)
    compatibilities: list[str] = field(default_factory=list)
    incompatibilities: list[str] = field(default_factory=list)
    integration_cost: float = 0.1
    state: str = "active"


@dataclass
class Genotype:
    central_approach: str
    assumptions: list[str]
    priorities: list[str]
    strategy: str
    style: str
    lineage: list[str] = field(default_factory=list)
    mutations: list[str] = field(default_factory=list)


@dataclass
class Phenotype:
    proposal: str
    thesis: str
    execution_plan: list[str]
    risks: list[str]
    mitigations: list[str]


@dataclass
class FitnessVector:
    utility: float
    precision: float
    feasibility: float
    originality: float
    evidence: float
    robustness: float
    clarity: float
    efficiency: float
    alignment: float

    def score(self) -> float:
        fields = [
            self.utility,
            self.precision,
            self.feasibility,
            self.originality,
            self.evidence,
            self.robustness,
            self.clarity,
            self.efficiency,
            self.alignment,
        ]
        return sum(fields) / len(fields)


@dataclass
class Solor:
    solor_id: str
    generation: int
    role: str
    task: str
    genotype: Genotype
    phenotype: Phenotype
    organs: list[Organ]
    state: SolorState = SolorState.ACTIVE
    fitness: FitnessVector | None = None
    pheromones: dict[str, float] = field(default_factory=dict)
    budget_used: float = 0.0
    judge_feedback: str = ""
    history: list[str] = field(default_factory=list)

    def snapshot(self) -> dict[str, Any]:
        return {
            "id": self.solor_id,
            "generation": self.generation,
            "state": self.state.value,
            "fitness": self.fitness.score() if self.fitness else None,
            "pheromones": self.pheromones,
            "budget_used": self.budget_used,
        }
