class Cores:
    cinza_escuro = (79, 79, 79)
    verde = (50, 205, 50)
    vermelho = (255, 0, 0)
    amarelo = (255, 255, 0)
    azul = (0, 0, 255)
    roxo = (128, 0, 128)
    laranja = (255, 165, 0)
    ciano = (0, 255, 255)
    midnight_blue = (25, 25, 112)
    light_blue = (135,206,250)
    branco = (255, 255, 255)

    @classmethod
    def cores_celulas(cls):
        return [cls.cinza_escuro, cls.verde, cls.vermelho, cls.laranja, cls.amarelo, cls.roxo, cls.ciano, cls.azul]