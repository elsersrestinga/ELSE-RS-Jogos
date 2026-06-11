import pygame
from cores import Cores
from posicao import Posicao

class Bloco:
    def __init__(self, id):
        self.id = id
        self.celulas = {}
        self.tamanho_celula = 30
        self.linha_offset = 0
        self.coluna_offset = 0
        self.status_rotacao = 0
        self.cores = Cores.cores_celulas()

    def mover(self, linhas, colunas):
        self.linha_offset += linhas
        self.coluna_offset += colunas

    def mostrar(self, tela, offset_x, offset_y):
        quadrados = self.posicao_celulas()
        for quadrado in quadrados:
            quadrado_retangulo = pygame.Rect(offset_x + quadrado.coluna*self.tamanho_celula, offset_y + quadrado.linha*self.tamanho_celula, self.tamanho_celula-1, self.tamanho_celula-1)
            pygame.draw.rect(tela, self.cores[self.id], quadrado_retangulo)

    def posicao_celulas(self):
        quadrados = self.celulas[self.status_rotacao]
        quadrados_movidos = []
        for posicao in quadrados:
            posicao = Posicao(posicao.linha + self.linha_offset, posicao.coluna + self.coluna_offset)
            quadrados_movidos.append(posicao)
        return quadrados_movidos

    def rotacao(self):
        self.status_rotacao += 1
        if self.status_rotacao == len(self.celulas):
            self.status_rotacao = 0

    def desfazer_rotacao(self):
        self.status_rotacao -= 1
        if self.status_rotacao == -1:
            self.status_rotacao = len(self.celulas)-1
