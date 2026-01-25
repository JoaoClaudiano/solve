from numpy import linspace
from engine.loads.point import PointLoad
from engine.loads.distributed import DistributedLoad

def shear_diagram(beam, npoints=200):
    L = beam.length
    xs = linspace(0, L, npoints)
    V = []
    RA = beam._reactions['A']
    for x in xs:
        v = RA
        # subtrai cargas pontuais à esquerda de x
        for pl in [l for l in beam.loads if isinstance(l, PointLoad)]:
            if pl.x <= x:
                v -= pl.P
        # subtrai parte das cargas distribuídas à esquerda de x
        for dl in [l for l in beam.loads if isinstance(l, DistributedLoad)]:
            x_e = dl.x_end if dl.x_end is not None else L
            if x > dl.x_start:
                left = min(x, x_e) - dl.x_start
                left = max(0.0, left)
                v -= dl.q * left
        V.append(v)
    return xs, V
