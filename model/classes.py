import pygame.draw

from model import cores


class Bloco:

    def __init__(self, linha, coluna, largura, total_linhas):
        self.linha = linha
        self.coluna = coluna
        self.largura = largura
        self.x = linha * largura
        self.y = coluna * largura
        self.cor = cores.BRANCO
        self.largura = largura
        self.blocos_adjacentes: list[Bloco] = []
        self.total_linhas = total_linhas

    def posicao(self):
        return self.coluna, self.linha

    def coordenada(self):
        return self.x, self.y, self.largura, self.largura

    def is_fechado(self):
        return self.cor == cores.VERMELHO

    def is_aberto(self):
        return self.cor == cores.VERDE

    def is_barreira(self):
        return self.cor == cores.PRETO

    def virar_barreira(self):
        self.cor = cores.PRETO

    def is_inicio(self):
        return self.cor == cores.LARANJA

    def is_final(self):
        return self.cor == cores.TURQUESA

    def reiniciar(self):
        self.cor = cores.BRANCO

    def fechar(self):
        self.cor = cores.VERMELHO

    def abrir(self):
        self.cor = cores.VERDE

    def iniciar(self):
        self.cor = cores.LARANJA

    def finalizar(self):
        self.cor = cores.TURQUESA

    def virar_caminho(self):
        self.cor = cores.ROXO

    def desenhar(self, janela):
        pygame.draw.rect(janela, self.cor, self.coordenada())

    def atualizar_blocos_adjacentes(self, grade):
        self.blocos_adjacentes = []
        if self.linha < self.total_linhas - 1:
            self.blocos_adjacentes.append(grade[self.linha - 1][self.coluna])

        if self.linha < self.total_linhas - 1:
            self.blocos_adjacentes.append(grade[self.linha + 1][self.coluna])

        if self.coluna > 0:
            self.blocos_adjacentes.append(grade[self.linha][self.coluna - 1])

        if self.coluna < self.total_linhas - 1:
            self.blocos_adjacentes.append(grade[self.linha][self.coluna + 1])

    def __lt__(self, other):
        return False

