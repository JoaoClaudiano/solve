class Beam:
    def __init__(self, length: float):
        self.length = float(length)
        self.loads = []       # cargas: objetos PointLoad ou DistributedLoad
        self.supports = []    # suporte: (tipo, posição) - por enquanto não usado além de convenção

    def add_load(self, load):
        self.loads.append(load)

    def add_support(self, support):
        self.supports.append(support)
