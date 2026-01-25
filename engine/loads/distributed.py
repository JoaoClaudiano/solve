class DistributedLoad:
    def __init__(self, q: float, x_start: float = 0.0, x_end: float = None):
        # q: intensidade (kN/m), positivo para baixo.
        self.q = float(q)
        self.x_start = float(x_start)
        self.x_end = x_end  # se None, define-se como o comprimento da viga quando necessário

    def total_load(self, beam_length):
        x_e = self.x_end if self.x_end is not None else beam_length
        return self.q * max(0.0, x_e - self.x_start)

    def centroid(self, beam_length):
        x_e = self.x_end if self.x_end is not None else beam_length
        L = max(0.0, x_e - self.x_start)
        if L == 0:
            return None
        return self.x_start + L / 2.0

    def __repr__(self):
        return f"DistributedLoad(q={self.q}, x_start={self.x_start}, x_end={self.x_end})"
