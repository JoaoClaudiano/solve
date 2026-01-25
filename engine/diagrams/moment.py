from numpy import linspace
from engine.loads.point import PointLoad
from engine.loads.distributed import DistributedLoad

def moment_diagram(beam, npoints=200):
    xs = linspace(0, beam.length, npoints)
    M = []
    RA = beam._reactions['A']
    for x in xs:
        m = RA * x
        # momentos de cargas pontuais à esquerda
        for pl in [l for l in beam.loads if isinstance(l, PointLoad)]:
            if pl.x <= x:
                m -= pl.P * (x - pl.x)
        # momentos de cargas distribuídas parcialmente
        for dl in [l for l in beam.loads if isinstance(l, DistributedLoad)]:
            x_e = dl.x_end if dl.x_end is not None else beam.length
            if x > dl.x_start:
                left = min(x, x_e) - dl.x_start
                left = max(0.0, left)
                # carga total left = q * left, centroid = dl.x_start + left/2
                m -= dl.q * left * (x - (dl.x_start + left/2))
        M.append(m)
    return xs, M
