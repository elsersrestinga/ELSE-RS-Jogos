import pygame, random

class Alien(pygame.sprite.Sprite):
    def __init__(self, tipo, x, y):
        super().__init__()
        self.tipo = tipo
        path = f"Imagens/alien_{tipo}.png"
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(topleft = (x, y))

    def update(self, direction):
        self.rect.x += direction

class NaveMisterio(pygame.sprite.Sprite):
    def __init__(self, largura_tela, offset):
        super().__init__()
        self.largura_tela = largura_tela
        self.offset = offset
        self.image = pygame.image.load("Imagens/misterio.png")
        x = random.choice([self.offset/2, self.largura_tela + self.offset - self.image.get_width()])
        if x == self.offset/2:
            self.velocidade = 3
        else:
            self.velocidade = -3
        self.rect = self.image.get_rect(topleft = (x, 90))

    def update(self):
        self.rect.x += self.velocidade
        if self.rect.right > self.largura_tela + self.offset/2:
            self.kill()
        elif self.rect.left < self.offset/2:
            self.kill()