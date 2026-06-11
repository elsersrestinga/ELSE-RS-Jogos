import pygame, sys, random
from pygame.math import Vector2
import asyncio

pygame.init()

tamanho_celula = 30
total_celula = 20
fora_das_celulas = 75

clock = pygame.time.Clock()
tela = pygame.display.set_mode((2*fora_das_celulas + tamanho_celula*total_celula,2*fora_das_celulas + tamanho_celula*total_celula))
pygame.display.set_caption("Snake")

class Comida:
    def __init__(self, cobra_corpo):
        self.posicao = self.geracao_pos_aleatoria(cobra_corpo)
    
    def mostrar(self):
        comida_rect = pygame.Rect(fora_das_celulas + self.posicao.x*tamanho_celula, fora_das_celulas + self.posicao.y*tamanho_celula, tamanho_celula, tamanho_celula)
        pygame.draw.rect(tela, "red", comida_rect)

    def geracao_celula_aleatoria(self):
        x = random.randint(0, total_celula -1)
        y = random.randint(0, total_celula -1)
        return Vector2(x,y)

    def geracao_pos_aleatoria(self, cobra_corpo):
        posicao = self.geracao_celula_aleatoria()
        while posicao in cobra_corpo:
            posicao = self.geracao_celula_aleatoria()
        return posicao
    
class Cobra:
    def __init__(self):
        self.corpo = [Vector2(6,9), Vector2(5,9)]
        self.direcao = Vector2(1, 0)
        self.adicionar_parte = False

    def mostrar(self):
        for pedaco in self.corpo:
            pedaco_rect = (fora_das_celulas + pedaco.x*tamanho_celula, fora_das_celulas + pedaco.y*tamanho_celula, tamanho_celula, tamanho_celula)
            pygame.draw.rect(tela, "green", pedaco_rect, 0 , 7)

    def mover(self):
        self.corpo.insert(0, self.corpo[0] + self.direcao)
        if self.adicionar_parte == True:
            self.adicionar_parte = False
        else:
            self.corpo = self.corpo[:-1]

    def reinicio(self):
        self.corpo = [Vector2(6,9), Vector2(5,9)]
        self.direcao = Vector2(1, 0)

class Jogo:
    def __init__(self):
        self.cobra = Cobra()
        self.comida = Comida(self.cobra.corpo)
        self.pontos = 0
        self.estado = "rodando"
    
    def mostrar(self):
        self.cobra.mostrar()
        self.comida.mostrar()

    def recarga(self):
        if self.estado == "rodando":
            self.cobra.mover()
            self.colisao()

    def colisao(self):
        #cantos
        if self.cobra.corpo[0].x == total_celula or self.cobra.corpo[0].x == -1:
            self.fim_de_jogo()
        if self.cobra.corpo[0].y == total_celula or self.cobra.corpo[0].y == -1:
            self.fim_de_jogo()
        #comida
        if self.cobra.corpo[0] == self.comida.posicao:
            self.comida.posicao = self.comida.geracao_pos_aleatoria(self.cobra.corpo)
            self.cobra.adicionar_parte = True
            self.pontos += 1
        #cauda
        corpo_sem_cabeca = self.cobra.corpo[1:]
        if self.cobra.corpo[0] in corpo_sem_cabeca:
            self.fim_de_jogo()

    def fim_de_jogo(self):
        self.cobra.reinicio()
        self.comida.posicao = self.comida.geracao_pos_aleatoria(self.cobra.corpo)
        self.estado = "parado"
        self.pontos = 0


async def main():
    tempo_ultimo_passo = pygame.time.get_ticks()
    intervalo_movimento = 200

    fonte_titulo = pygame.font.SysFont(None, 60)
    fonte_pontos = pygame.font.SysFont(None, 40)
    jogo = Jogo()
    while True:
        tempo_atual = pygame.time.get_ticks()
        if jogo.estado == "rodando":
            if tempo_atual - tempo_ultimo_passo > intervalo_movimento:
                jogo.recarga()
                tempo_ultimo_passo = tempo_atual
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if jogo.estado == "parado":
                    jogo.estado = "rodando"
                if event.key == pygame.K_UP and jogo.cobra.direcao != Vector2(0, 1):
                    jogo.cobra.direcao = Vector2(0, -1)
                elif event.key == pygame.K_DOWN and jogo.cobra.direcao != Vector2(0, -1):
                    jogo.cobra.direcao = Vector2(0, 1)
                elif event.key == pygame.K_LEFT and jogo.cobra.direcao != Vector2(1, 0):
                    jogo.cobra.direcao = Vector2(-1, 0)
                elif event.key == pygame.K_RIGHT and jogo.cobra.direcao != Vector2(-1, 0):
                    jogo.cobra.direcao = Vector2(1, 0)
            
                
        tela.fill("black")
        pygame.draw.rect(tela, "white",
                         (fora_das_celulas-5, fora_das_celulas-5, tamanho_celula*total_celula+10, tamanho_celula*total_celula+10), 5)
        jogo.mostrar()
        local_titulo = fonte_titulo.render("Snake", True, "white")
        local_pontos = fonte_pontos.render(str(jogo.pontos), True, "white")
        tela.blit(local_titulo, (fora_das_celulas-5, 20))
        tela.blit(local_pontos, (fora_das_celulas-5, fora_das_celulas+tamanho_celula*total_celula + 10))
        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())