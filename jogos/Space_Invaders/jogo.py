import pygame, random
from nave import Nave
from defesa import Defesa, grid
from alien import Alien
from alien import NaveMisterio
from laser import Laser

class Jogo:
    def __init__(self, largura_tela, altura_tela, offset):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.offset = offset
        self.nave_grupo = pygame.sprite.GroupSingle()
        self.nave_grupo.add(Nave(self.largura_tela, self.altura_tela, self.offset))
        self.defesas = self.criar_defesas()
        self.aliens_grupo = pygame.sprite.Group()
        self.criar_aliens()
        self.aliens_direcao = 1
        self.aliens_lasers_grupo = pygame.sprite.Group()
        self.nave_misterio_grupo = pygame.sprite.GroupSingle()
        self.vidas = 3
        self.run = True
        self.score = 0
        self.highscore = 0
        self.carregar_highscore()
        self.level = 1
        self.explosao = pygame.mixer.Sound("sons/explosao.ogg")
        self.explosao.set_volume(0.3)
        self.hit = pygame.mixer.Sound("sons/Hit.ogg")
        self.hit.set_volume(0.3)

    def criar_defesas(self):
        largura_defesa = len(grid[0]) * 3
        espaco = (self.largura_tela + self.offset - (4*largura_defesa))/5
        defesas = []
        for i in range(4):
            self.offset_x = (i + 1) * espaco + i * largura_defesa
            defesa = Defesa(self.offset_x, self.altura_tela - 100)
            defesas.append(defesa)
        return defesas

    def criar_aliens(self):
        ordem = random.randint(1, 3)
        for linha in range(5):
            for coluna in range(11):
                x = 75 + coluna * 55
                y = 110 + linha * 55

                if ordem == 1:
                    if linha == 0:
                        alien_tipo = 3
                    elif linha in (1,2):
                        alien_tipo = 2
                    else:
                        alien_tipo = 1
                elif ordem == 2:
                    if linha in (0,1):
                        alien_tipo = 2
                    elif linha == 2:
                        alien_tipo = 3
                    else:
                        alien_tipo = 1
                elif ordem == 3:
                    if linha in (0,1):
                        alien_tipo = 1
                    elif linha in (2,3):
                        alien_tipo = 2
                    else:
                        alien_tipo = 3

                alien = Alien(alien_tipo, x + self.offset/2, y)
                self.aliens_grupo.add(alien)

    def mover_aliens(self):
        self.aliens_grupo.update(self.aliens_direcao)

        aliens_sprite = self.aliens_grupo.sprites()
        for alien in aliens_sprite:
            if alien.rect.right >= self.largura_tela + self.offset/2:
                self.aliens_direcao = -1
                self.aliens_mover_baixo(2)
            elif alien.rect.left <= self.offset/2:
                self.aliens_direcao = 1
                self.aliens_mover_baixo(2)

    def aliens_mover_baixo(self, distancia):
        if self.aliens_grupo:
            for alien in self.aliens_grupo.sprites():
                alien.rect.y += distancia

    def alien_atirar_laser(self):
        if self.aliens_grupo.sprites():
            random_alien = random.choice(self.aliens_grupo.sprites())
            laser_sprite = Laser(random_alien.rect.center, -6, self.altura_tela)
            self.aliens_lasers_grupo.add(laser_sprite)

    def criar_nave_misterio(self):
        self.nave_misterio_grupo.add(NaveMisterio(self.largura_tela, self.offset))

    def verificar_colisoes(self):
        #Nave
        if self.nave_grupo.sprite.grupo_lasers:
            for laser_sprite in self.nave_grupo.sprite.grupo_lasers:

                alien_hit = pygame.sprite.spritecollide(laser_sprite, self.aliens_grupo, True)
                if alien_hit:
                    for alien in alien_hit:
                        self.score += alien.tipo * 10
                        self.verificar_highscore()
                        laser_sprite.kill()
                        self.explosao.play()
                        

                if pygame.sprite.spritecollide(laser_sprite, self.nave_misterio_grupo, True):
                    self.score += 50
                    self.verificar_highscore()
                    laser_sprite.kill()
                    self.explosao.play()

                for defesa in self.defesas:
                    if pygame.sprite.spritecollide(laser_sprite, defesa.grupo_blocos, True):
                        laser_sprite.kill()
                        self.explosao.play()

        #Aliens lasers
        if self.aliens_lasers_grupo:
            for laser_sprite in self.aliens_lasers_grupo:
                if pygame.sprite.spritecollide(laser_sprite, self.nave_grupo, False):
                    laser_sprite.kill()
                    self.hit.play()
                    self.vidas -= 1
                    if self.vidas == 0:
                        self.fim_de_jogo()

                for defesa in self.defesas:
                    if pygame.sprite.spritecollide(laser_sprite, defesa.grupo_blocos, True):
                        laser_sprite.kill()
                        self.explosao.play()

        if self.aliens_grupo:
            for alien in self.aliens_grupo:
                for defesa in self.defesas:
                    pygame.sprite.spritecollide(alien, defesa.grupo_blocos, True)

                if pygame.sprite.spritecollide(alien, self.nave_grupo, False):
                    self.vidas -= 1
                    if self.vidas == 0:
                        self.fim_de_jogo()

    def fim_de_jogo(self):
        self.run = False

    def reset(self):
        self.run = True
        self.vidas = 3
        self.nave_grupo.sprite.reset()
        self.aliens_grupo.empty()
        self.aliens_lasers_grupo.empty()
        self.criar_aliens()
        self.nave_misterio_grupo.empty()
        self.defesas = self.criar_defesas()
        self.score = 0
        self.level = 1


    def verificar_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score

            with open("highscore.txt", "w") as file:
                file.write(str(self.highscore))

    def carregar_highscore(self):
        try:
            with open("highscore.txt", "r") as file:
                self.highscore = int(file.read())
        except (FileNotFoundError, ValueError):
            self.highscore = 0

    def proximo_nivel(self):
        if not self.aliens_grupo:
            self.criar_aliens()
            self.aliens_lasers_grupo.empty()
            if self.vidas <=9:
                self.vidas += 1
            self.level += 1
            if self.level %5 == 0:
                self.defesas = self.criar_defesas()