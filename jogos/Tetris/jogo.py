from blocos import *
from grid import Grid
import random

class Jogo:
    def __init__(self):
        self.grid = Grid()
        self.blocos = [LBloco(), JBloco(), IBloco(), OBloco(), SBloco(), TBloco(), ZBloco()]
        self.bloco_atual = self.random_bloco()
        self.proximo_bloco = self.random_bloco()
        self.fim_de_jogo = False
        self.pontos = 0
    
    def reler_pontos(self, linhas_completas, mover_baixo_pontos):
        if linhas_completas == 1:
            self.pontos+= 100
        elif linhas_completas == 2:
            self.pontos+= 300
        elif linhas_completas == 3:
            self.pontos+= 500
        self.pontos += mover_baixo_pontos

    def random_bloco(self):
        if len(self.blocos) == 0:
            self.blocos = [LBloco(), JBloco(), IBloco(), OBloco(), SBloco(), TBloco(), ZBloco()]
        bloco = random.choice(self.blocos)
        self.blocos.remove(bloco)
        return bloco

    def mostrar(self, tela):
        self.grid.mostrar(tela)
        self.bloco_atual.mostrar(tela, 11, 11)
        if self.proximo_bloco.id == 3:
            self.proximo_bloco.mostrar(tela, 255, 290)
        elif self.proximo_bloco.id == 4:
            self.proximo_bloco.mostrar(tela, 255, 280)
        else:
            self.proximo_bloco.mostrar(tela, 270, 270)
    
    def mover_esq(self):
        self.bloco_atual.mover(0,-1)
        if self.bloco_dentro() == False or self.bloco_encaixa() == False:
            self.bloco_atual.mover(0,1)
    
    def mover_dir(self):
        self.bloco_atual.mover(0,1)
        if self.bloco_dentro() == False or self.bloco_encaixa() == False:
            self.bloco_atual.mover(0,-1)
    
    def mover_baixo(self):
        self.bloco_atual.mover(1,0)
        if self.bloco_dentro() == False or self.bloco_encaixa() == False:
            self.bloco_atual.mover(-1,0)
            self.prender_bloco()
    
    def prender_bloco(self):
        quadrados = self.bloco_atual.posicao_celulas()
        for posicao in quadrados:
            self.grid.grid[posicao.linha][posicao.coluna] = self.bloco_atual.id
        self.bloco_atual = self.proximo_bloco
        self.proximo_bloco = self.random_bloco()
        linhas_completas = self.grid.limpar_linhas_completa()
        self.reler_pontos(linhas_completas, 0)
        if self.bloco_encaixa() == False:
            self.fim_de_jogo = True
    
    def reset(self):
        self.grid.reset()
        self.blocos = [LBloco(), JBloco(), IBloco(), OBloco(), SBloco(), TBloco(), ZBloco()]
        self.bloco_atual = self.random_bloco()
        self.proximo_bloco = self.random_bloco()
        self.pontos = 0
    
    def bloco_encaixa(self):
        quadrados = self.bloco_atual.posicao_celulas()
        for quadrado in quadrados:
            if self.grid.esta_vazio(quadrado.linha, quadrado.coluna) == False:
                return False
        return True
    
    def rotacao(self):
        self.bloco_atual.rotacao()
        if self.bloco_dentro() == False or self.bloco_encaixa() == False:
            self.bloco_atual.desfazer_rotacao()
    
    def bloco_dentro(self):
        quadrados = self.bloco_atual.posicao_celulas()
        for quadrado in quadrados:
            if self.grid.esta_dentro(quadrado.linha, quadrado.coluna) == False:
                return False
        return True