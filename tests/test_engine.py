from mesa.engine import MesaEngine
from mesa.models import ComplexityLevel, UserTask


def test_complexity_thermostat():
    engine = MesaEngine()
    short = UserTask(prompt="Comando RAM")
    long = UserTask(prompt="x" * 500)
    assert engine.governor.choose_complexity(short) == ComplexityLevel.AGENT
    assert engine.governor.choose_complexity(long) == ComplexityLevel.REDUCED_EVOLUTION


def test_run_produces_winner_and_trace():
    engine = MesaEngine()
    trace = engine.run(UserTask(prompt="Diseña estrategia B2B con riesgos y plan"), max_generations=2)
    assert trace.winner_id
    assert trace.generations == 2
    assert "Síntesis" in trace.final_solution
    assert len(trace.snapshots) >= 1
