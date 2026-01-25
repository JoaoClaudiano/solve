from engine.loads.point import PointLoad
from engine.loads.distributed import DistributedLoad

def _total_vertical_load(beam):
    total = 0.0
    for L in beam.loads:
        if isinstance(L, PointLoad):
            total += L.P
        elif isinstance(L, DistributedLoad):
            total += L.total_load(beam.length)
    return total

def _first_moment_about_A(beam):
    sm = 0.0
    for L in beam.loads:
        if isinstance(L, PointLoad):
            sm += L.P * L.x
        elif isinstance(L, DistributedLoad):
            W = L.total_load(beam.length)
            c = L.centroid(beam.length)
            if c is not None:
                sm += W * c
    return sm

def solve_reactions(beam):
    """
    Resolve reações para viga biapoiada com apoios em x=0 (A) e x=L (B).
    Convenção: cargas para baixo são positivas.
    Retorna (RA, RB), reações verticais (kN).
    """
    L = beam.length
    W = _total_vertical_load(beam)            # carga total para baixo (kN)
    M_about_A = _first_moment_about_A(beam)   # Σ(load * x) em relação a A
    # RB * L = Σ(load * x) -> RB = Σ(load*x)/L
    RB = M_about_A / L if L != 0 else 0.0
    RA = W - RB
    return float(RA), float(RB)
