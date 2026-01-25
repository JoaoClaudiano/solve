from engine.elements.beam import Beam
from engine.loads.point import PointLoad
from engine.loads.distributed import DistributedLoad
from engine.solver.statics import solve_reactions
from engine.diagrams import shear, moment
from engine.memory.report import simple_report

def run_beam_analysis(data):
    """
    data: dict com chaves:
      - length: float
      - loads: list de dicts {type: 'point'|'distributed', value: ..., x: ..., x_start:, x_end:}
      - supports: list (não usado ativamente aqui, apenas convenção)
    Retorna: dict com reações, arrays de V(x) e M(x) e 'report' (texto).
    """
    beam = Beam(length=data.get("length", 5.0))
    for L in data.get("loads", []):
        t = L.get("type")
        if t == "point":
            beam.add_load(PointLoad(L.get("value", 0.0), L.get("x", 0.0)))
        elif t == "distributed":
            x_start = L.get("x_start", 0.0)
            x_end = L.get("x_end", None)
            beam.add_load(DistributedLoad(L.get("value", 0.0), x_start=x_start, x_end=x_end))

    RA, RB = solve_reactions(beam)
    beam._reactions = {"A": RA, "B": RB}

    xs_v, V = shear.shear_diagram(beam)
    xs_m, M = moment.moment_diagram(beam)
    report = simple_report(beam)

    return {
        "length": beam.length,
        "reactions": {"A": RA, "B": RB},
        "xs_shear": xs_v.tolist(),
        "shear": [float(v) for v in V],
        "xs_moment": xs_m.tolist(),
        "moment": [float(m) for m in M],
        "report": report
    }
