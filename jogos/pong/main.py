import pygame, sys, random, asyncio

#CLASSES

class Raquete:
    def __init__(self, tela, cor, posX, posY, largura_r, altura_r):
        self.tela = tela
        self.cor = cor
        self.posX = posX
        self.posY = posY
        self.largura_r = largura_r
        self.altura_r = altura_r
        self.momento = "parado"
        self.mostrar()

    def mostrar(self):
        pygame.draw.rect(self.tela, self.cor, (self.posX, self.posY, self.largura_r, self.altura_r))

    def movimentacao(self):
        if self.momento == "cima":
            self.posY -= 10

        elif self.momento == "baixo":
            self.posY += 10

    def limite(self):
        if self.posY <= 0:
            self.posY = 0

        if self.posY + self.altura_r >= altura:
            self.posY = altura - self.altura_r

    def posicao_recomeco(self):
        self.posY = altura//2 - self.altura_r//2
        self.momento = 'parado'
        self.mostrar()

class Bolas:
    def __init__(self, tela, cor, posX, posY, tamanho):
        self.tela = tela
        self.cor = cor
        self.posX = posX
        self.posY = posY
        self.tamanho = tamanho
        self.dx = 0
        self.dy = 0
        self.mostrar()

    def mostrar(self):
        pygame.draw.circle(self.tela, self.cor, (self.posX, self.posY), self.tamanho)

    def iniciar_movimento(self):
        self.dx = random.choice([-1, 1]) * random.randint(4, 8)
        self.dy = random.choice([-1, 1]) * random.randint(2, 6)

    def mover(self):
        self.posX += self.dx
        self.posY += self.dy

    def raquete_colisao(self):
        self.dx = self.dx*-1

    def colisao_parede(self):
        self.dy = self.dy*-1

class Pontuacao:
    def __init__(self, tela, pontos, posX, posY):
        self.tela = tela
        self.pontos = pontos
        self.posX = posX
        self.posY = posY
        self.fonte = pygame.font.SysFont("nonospace", 80, bold=True)
        self.aparecer = self.fonte.render(self.pontos, 0, "White")
        self.mostrar()

    def mostrar(self):
        self.tela.blit(self.aparecer, (self.posX - self.aparecer.get_rect().width//2, self.posY))

    def aumento(self):
        pontos = int(self.pontos) + 1
        self.pontos = str(pontos)
        self.aparecer = self.fonte.render(self.pontos, 0, "White")

    def reinicio(self):
        self.pontos = '0'
        self.aparecer = self.fonte.render(self.pontos, 0, "White")

class ManuseadorColisao:
    def entre_bola_e_Raquete_esquerda(self, bola, raquete_esquerda):
        if bola.posY + bola.tamanho > raquete_esquerda.posY and bola.posY - bola.tamanho < raquete_esquerda.posY + raquete_esquerda.altura_r:
            if bola.posX - bola.tamanho <= raquete_esquerda.posX + raquete_esquerda.largura_r:
                return True
        else:
            return False

    def entre_bola_e_Raquete_direita(self, bola, raquete_direita):
        if bola.posY + bola.tamanho > raquete_direita.posY and bola.posY - bola.tamanho < raquete_direita.posY + raquete_direita.altura_r:
            if bola.posX + bola.tamanho >= raquete_direita.posX:
                return True
        else:
            return False

    def entre_bola_e_paredes(self, bola):
        #topo
        if bola.posY - bola.tamanho <= 0:
            return True

        #chão
        if bola.posY + bola.tamanho >= altura:
            return True

        else:
            return False

    def verificacao_gol_player1(self, bola):
        return bola.posX - bola.tamanho >= largura

    def verificacao_gol_player2(self, bola):
        return bola.posX + bola.tamanho <= 0

largura, altura = 900, 500

#tela
pygame.init()
clock = pygame.time.Clock()
tela = pygame.display.set_mode( (largura, altura) )
pygame.display.set_caption('PONG')

#funções

def desenhar_campo():
    tela.fill("black")
    pygame.draw.line( tela, "White",  (largura//2, 0), (largura//2, altura), 5)

def recomeco():
    desenhar_campo()
    pontuacao1.reinicio()
    pontuacao2.reinicio()
    reiniciar_bola()

def reiniciar_bola():
    bolas.clear()
    nova = Bolas(tela, "white", largura // 2, altura // 2, 20)
    nova.iniciar_movimento()
    bolas.append(nova)
    raquete_esquerda.posicao_recomeco()
    raquete_direita.posicao_recomeco()

desenhar_campo()

#Objetos
async def main():
    global bolas, raquete_esquerda, raquete_direita, pontuacao1, pontuacao2, jogando, tempo_inicial
    bolas = [Bolas(tela, "white", largura//2, altura//2, 20)]
    raquete_esquerda = Raquete(tela, "white", 15, altura//2 - 60, 20, 120)
    raquete_direita = Raquete(tela, "white", largura-35, altura//2 - 60, 20, 120)
    colisao = ManuseadorColisao()
    pontuacao1 = Pontuacao(tela, '0', largura//4, 15)
    pontuacao2 = Pontuacao(tela, '0', largura - largura//4, 15)

    jogando = False
    tempo_inicial = pygame.time.get_ticks()
    intervalo_bola = 20000
    max_bolas = 4
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not jogando:
                        for bola in bolas:
                            bola.iniciar_movimento()
                        jogando = True

                if event.key == pygame.K_r:
                    recomeco()
                    jogando = False

                if event.key == pygame.K_w:
                    raquete_esquerda.momento = "cima"

                if event.key == pygame.K_s:
                    raquete_esquerda.momento = "baixo"

                if event.key == pygame.K_UP:
                    raquete_direita.momento = "cima"

                if event.key == pygame.K_DOWN:
                    raquete_direita.momento = "baixo"

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    raquete_esquerda.momento = "parado"
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    raquete_direita.momento = "parado"

        if jogando:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - tempo_inicial >= intervalo_bola and len(bolas) < max_bolas:
                centro_x = largura // 2
                centro_y = altura // 2
                margem = 50

                posX = random.randint(centro_x - margem, centro_x + margem)
                posY = random.randint(centro_y - margem, centro_y + margem)
                nova_bola = Bolas(tela, "white", posX, posY, 20)
                nova_bola.iniciar_movimento()
                bolas.append(nova_bola)
                tempo_inicial = tempo_atual
            desenhar_campo()
            #movimento da bola
            for bola in bolas:
                bola.mover()
                bola.mostrar()

            #Raquete esquerdo
            raquete_esquerda.movimentacao()
            raquete_esquerda.limite()
            raquete_esquerda.mostrar()

            #Raquete direito
            raquete_direita.movimentacao()
            raquete_direita.limite()
            raquete_direita.mostrar()

            #checagem de colisão
            for bola in bolas:
                if colisao.entre_bola_e_Raquete_esquerda(bola, raquete_esquerda):
                    bola.raquete_colisao()
                    bola.posX = raquete_esquerda.posX + raquete_esquerda.largura_r + bola.tamanho

                if colisao.entre_bola_e_Raquete_direita(bola, raquete_direita):
                    bola.raquete_colisao()
                    bola.posX = raquete_direita.posX - bola.tamanho

                if colisao.entre_bola_e_paredes(bola):
                    bola.colisao_parede()

                if colisao.verificacao_gol_player1(bola):
                    desenhar_campo()
                    pontuacao1.aumento()
                    reiniciar_bola()
                    jogando = False
                    break

                if colisao.verificacao_gol_player2(bola):
                    desenhar_campo()
                    pontuacao2.aumento()
                    reiniciar_bola()
                    jogando = False
                    break

        pontuacao1.mostrar()
        pontuacao2.mostrar()

        clock.tick(60)
        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())