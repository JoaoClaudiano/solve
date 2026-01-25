class PointLoad:
    def __init__(self, P: float, x: float):
        # P: magnitude (kN). Convenção: positivo para baixo.
        self.P = float(P)
        self.x = float(x)

    def __repr__(self):
        return f"PointLoad(P={self.P}, x={self.x})"
