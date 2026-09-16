import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, posicao, velocidade, altura_tela):
        super().__init__()
        self.image = pygame.Surface((4,15))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center = posicao)
        self.velocidade = velocidade
        self.altura_tela = altura_tela

    def update(self):
        self.rect.y -= self.velocidade
        if self.rect.y > self.altura_tela + 15 or self.rect.y < 0:
            self.kill()