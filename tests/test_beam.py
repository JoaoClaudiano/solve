from engine.elements.beam import Beam
from engine.loads.point import PointLoad
from engine.loads.distributed import DistributedLoad
from engine.solver.statics import solve_reactions

def test_uniform_distributed_load():
    b = Beam(5.0)
    b.add_load(DistributedLoad(10.0, 0.0, 5.0))  # q = 10 kN/m over whole beam
    RA, RB = solve_reactions(b)
    assert abs(RA - 25.0) < 1e-6
    assert abs(RB - 25.0) < 1e-6

def test_point_load_midspan():
    b = Beam(4.0)
    b.add_load(PointLoad(20.0, 2.0))  # P at midspan
    RA, RB = solve_reactions(b)
    assert abs(RA - 10.0) < 1e-6
    assert abs(RB - 10.0) < 1e-6
