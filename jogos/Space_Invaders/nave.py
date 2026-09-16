import pygame
from laser import Laser

class Nave(pygame.sprite.Sprite):
    def __init__(self, largura_tela, altura_tela, offset):
        super().__init__()
        self.offset = offset
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.image = pygame.image.load("Imagens/nave.png")
        self.rect = self.image.get_rect(midbottom = ((self.largura_tela + self.offset)/2, self.altura_tela))
        self.velocidade = 6
        self.grupo_lasers = pygame.sprite.Group()
        self.laser_pronto = True
        self.tempo_laser = 0
        self.espera_laser = 300

    def get_input_usuario(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.velocidade
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.velocidade
        if keys[pygame.K_SPACE] or keys[pygame.K_z]:
            if self.laser_pronto:
                self.laser_pronto = False
                laser = Laser(self.rect.center, 5, self.altura_tela)
                self.grupo_lasers.add(laser)
                self.tempo_laser = pygame.time.get_ticks()

    def update(self):
        self.get_input_usuario()
        self.limitar_movimento()
        self.grupo_lasers.update()
        self.recarregar_laser()

    def limitar_movimento(self):
        if self.rect.right > self.largura_tela:
            self.rect.right = self.largura_tela
        if self.rect.left < self.offset:
            self.rect.left = self.offset

    def recarregar_laser(self):
        if not self.laser_pronto:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_laser >= self.espera_laser:
                self.laser_pronto = True

    def reset(self):
        self.rect = self.image.get_rect(midbottom = ((self.largura_tela + self.offset)/2, self.altura_tela))
        self.grupo_lasers.empty()