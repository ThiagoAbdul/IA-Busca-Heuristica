import random

import pygame.draw

from exceptions.exception import NaoTemBlocosNoRadarException
from model import cores


class Sprite:

    def __init__(self, linha, coluna, largura, total_linhas, cor):
        self.linha = linha
        self.coluna = coluna
        self.largura = largura
        self.x = linha * largura
        self.y = coluna * largura
        self.total_linhas = total_linhas
        self.COR_PADRAO = cor
        self.cor_atual = cor

    def posicao(self):
        return self.linha, self.coluna

    def coordenada(self):
        return self.x, self.y, self.largura, self.largura

    def desenhar(self, janela):
        pygame.draw.rect(janela, self.cor_atual, self.coordenada())


class Bloco(Sprite):

    @staticmethod
    def random_factory(linha, coluna, largura, total_linhas):
        return random.choice((BlocoGrama(linha, coluna, largura, total_linhas),
                              BlocoAgua(linha, coluna, largura, total_linhas),
                              BlocoMontanha(linha, coluna, largura, total_linhas)))

    def __init__(self, linha, coluna, largura, total_linhas, cor, custo, esfera=None, agente=None):
        super().__init__(linha, coluna, largura, total_linhas, cor)
        self.blocos_adjacentes: list[Bloco] = []
        self.custo = custo
        self.esfera = esfera
        self.agente = agente

    def tem_esfera(self):
        return self.esfera is not None

    def tem_agente(self):
        return self.agente is not None

    def reiniciar(self):
        self.cor_atual = self.COR_PADRAO

    def clarear(self):
        self.cor_atual = cores.clarear(self.COR_PADRAO)

    def abrir(self):
        self.cor_atual = cores.escurecer(self.COR_PADRAO)

    def iniciar(self):
        self.cor_atual = cores.VERMELHO

    def virar_destino(self):
        self.cor_atual = cores.TURQUESA

    def virar_caminho(self):
        self.cor_atual = cores.ROXO

    def atualizar_blocos_adjacentes(self, grade):
        self.blocos_adjacentes = []
        if 0 < self.linha:
            self.blocos_adjacentes.append(grade[self.linha - 1][self.coluna])

        if self.linha < self.total_linhas - 1:
            self.blocos_adjacentes.append(grade[self.linha + 1][self.coluna])

        if self.coluna > 0:
            self.blocos_adjacentes.append(grade[self.linha][self.coluna - 1])

        if self.coluna < self.total_linhas - 1:
            self.blocos_adjacentes.append(grade[self.linha][self.coluna + 1])

    def __lt__(self, other):
        return False


class BlocoGrama(Bloco):

    def __init__(self, linha, coluna, largura, total_linhas):
        super().__init__(linha, coluna, largura, total_linhas, cores.VERDE, 1)


class BlocoAgua(Bloco):

    def __init__(self, linha, coluna, largura, total_linhas):
        super().__init__(linha, coluna, largura, total_linhas, cores.AZUL, 10)


class BlocoMontanha(Bloco):

    def __init__(self, linha, coluna, largura, total_linhas):
        super().__init__(linha, coluna, largura, total_linhas, cores.MARROM, 60)


class Agente(Sprite):

    @staticmethod
    def criar_agente_no_bloco(bloco):
        agente = Agente(bloco.linha, bloco.coluna, bloco.largura, bloco.total_linhas)
        bloco.agente = agente
        agente.bloco_atual = bloco
        return agente

    def __init__(self, linha, coluna, largura, total_linhas, bloco=None):
        super().__init__(linha, coluna, largura, total_linhas, cores.VERMELHO)
        self.bloco_atual = bloco
        self.blocos_no_radar = None
        self.custo_percorrido = 0

    def area_radar(self, grade):
        self.blocos_no_radar = []
        x, y = self.posicao()
        for i in range(x - 3, x + 4):
            for j in range(y - 3, y + 4):
                if 0 <= i < 42 and 0 <= j < 42:
                    self.blocos_no_radar.append(grade[i][j])
        return self.blocos_no_radar

    def abrir_radar(self, grade):
        for bloco in self.area_radar(grade):
            bloco.clarear()

    def fechar_radar(self, grade):
        for bloco in self.area_radar(grade):
            bloco.reiniciar()

    def ir_para_bloco(self, bloco: Bloco):
        self.bloco_atual.agente = None
        self.linha = bloco.linha
        self.coluna = bloco.coluna
        self.x = bloco.x
        self.y = bloco.y
        bloco.agente = self
        self.bloco_atual = bloco
        self.custo_percorrido += bloco.custo

    def esferas_localizadas(self):
        esferas = []
        if self.blocos_no_radar is None:
            raise NaoTemBlocosNoRadarException
        for bloco in self.blocos_no_radar:
            if bloco.tem_esfera():
                esferas.append(bloco.esfera)
        return esferas


class Esfera(Sprite):

    def __init__(self, linha, coluna, largura, total_linhas):
        super().__init__(linha, coluna, largura, total_linhas, cores.LARANJA)

    def desenhar(self, janela):
        pygame.draw.ellipse(janela, self.cor_atual, self.coordenada())
