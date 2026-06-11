from bloco import Bloco
from posicao import Posicao

class LBloco(Bloco):
    def __init__(self):
        super().__init__(id = 1)
        self.celulas = {
            0: [Posicao(0,2), Posicao(1,0), Posicao(1,1), Posicao(1,2)],
            1: [Posicao(0,1), Posicao(1,1), Posicao(2,1), Posicao(2,2)],
            2: [Posicao(1,0), Posicao(1,1), Posicao(1,2), Posicao(2,0)],
            3: [Posicao(0,0), Posicao(0,1), Posicao(1,1), Posicao(2,1)]
        }
        self.mover(0,3)

class JBloco(Bloco):
    def __init__(self):
        super().__init__(id = 2)
        self.celulas = {
            0: [Posicao(0,0), Posicao(1,0), Posicao(1,1), Posicao(1,2)],
            1: [Posicao(0,1), Posicao(0,2), Posicao(1,1), Posicao(2,1)],
            2: [Posicao(1,0), Posicao(1,1), Posicao(1,2), Posicao(2,2)],
            3: [Posicao(0,1), Posicao(1,1), Posicao(2,0), Posicao(2,1)]
        }
        self.mover(0,3)

class IBloco(Bloco):
    def __init__(self):
        super().__init__(id = 3)
        self.celulas = {
            0: [Posicao(1,0), Posicao(1,1), Posicao(1,2), Posicao(1,3)],
            1: [Posicao(0,2), Posicao(1,2), Posicao(2,2), Posicao(3,2)],
            2: [Posicao(2,0), Posicao(2,1), Posicao(2,2), Posicao(2,3)],
            3: [Posicao(0,1), Posicao(1,1), Posicao(2,1), Posicao(3,1)]
        }
        self.mover(-1,3)

class OBloco(Bloco):
    def __init__(self):
        super().__init__(id = 4)
        self.celulas = {
            0: [Posicao(0,0), Posicao(0,1), Posicao(1,0), Posicao(1,1)]
        }
        self.mover(0,4)

class SBloco(Bloco):
    def __init__(self):
        super().__init__(id = 5)
        self.celulas = {
            0: [Posicao(0,1), Posicao(0,2), Posicao(1,0), Posicao(1,1)],
            1: [Posicao(0,1), Posicao(1,1), Posicao(1,2), Posicao(2,2)],
            2: [Posicao(1,1), Posicao(1,2), Posicao(2,0), Posicao(2,1)],
            3: [Posicao(0,0), Posicao(1,0), Posicao(1,1), Posicao(2,1)]
        }
        self.mover(0,3)

class TBloco(Bloco):
    def __init__(self):
        super().__init__(id = 6)
        self.celulas = {
            0: [Posicao(0,1), Posicao(1,0), Posicao(1,1), Posicao(1,2)],
            1: [Posicao(0,1), Posicao(1,1), Posicao(1,2), Posicao(2,1)],
            2: [Posicao(1,0), Posicao(1,1), Posicao(1,2), Posicao(2,1)],
            3: [Posicao(0,1), Posicao(1,0), Posicao(1,1), Posicao(2,1)]
        }
        self.mover(0,3)

class ZBloco(Bloco):
    def __init__(self):
        super().__init__(id = 7)
        self.celulas = {
            0: [Posicao(0,0), Posicao(0,1), Posicao(1,1), Posicao(1,2)],
            1: [Posicao(0,2), Posicao(1,1), Posicao(1,2), Posicao(2,1)],
            2: [Posicao(1,0), Posicao(1,1), Posicao(2,1), Posicao(2,2)],
            3: [Posicao(0,1), Posicao(1,0), Posicao(1,1), Posicao(2,0)]
        }
        self.mover(0,3)