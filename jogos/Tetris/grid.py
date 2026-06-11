import pygame
from cores import Cores

class Grid:
    def __init__(self):
        self.num_linhas = 20
        self.num_colunas = 10
        self.tamanho_celula = 30
        self.grid = [[0 for j in range(self.num_colunas)] for i in range(self.num_linhas)]
        self.cores = Cores.cores_celulas()
    
    def esta_dentro(self, linha, coluna):
        if linha >= 0 and linha < self.num_linhas and coluna >= 0 and coluna < self.num_colunas:
            return True
        return False
    
    def esta_vazio(self, linha, coluna):
        if self.grid[linha][coluna] == 0:
            return True
        return False
    
    def esta_cheio(self, linha):
        for coluna in range(self.num_colunas):
            if self.grid[linha][coluna] == 0:
                return False
        return True
    
    def limpar_linha(self, linha):
        for coluna in range(self.num_colunas):
            self.grid[linha][coluna] = 0
    
    def mover_linha_baixo(self, linha, num_linhas):
        for coluna in range(self.num_colunas):
            self.grid[linha+num_linhas][coluna] = self.grid[linha][coluna]
            self.grid[linha][coluna] = 0
    
    def limpar_linhas_completa(self):
        completado = 0
        for linha in range(self.num_linhas-1, 0, -1):
            if self.esta_cheio(linha):
                self.limpar_linha(linha)
                completado += 1
            elif completado > 0:
                self.mover_linha_baixo(linha, completado)
        return completado
    
    def reset(self):
        for linha in range(self.num_linhas):
            for coluna in range(self.num_colunas):
                self.grid[linha][coluna] = 0

    def mostrar(self, tela):
        for linha in range(self.num_linhas):
            for coluna in range(self.num_colunas):
                valor_celula = self.grid[linha][coluna]
                retangulo_celula = pygame.Rect(coluna*self.tamanho_celula + 11, linha*self.tamanho_celula + 11, self.tamanho_celula-1, self.tamanho_celula-1)
                pygame.draw.rect(tela, self.cores[valor_celula], retangulo_celula)