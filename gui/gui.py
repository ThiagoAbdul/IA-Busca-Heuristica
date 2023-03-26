import pygame
from pygame import Surface
from pygame.event import Event

from model import cores


def get_posicao_click(linhas, largura):
    posicao = pygame.mouse.get_pos()
    espaco = largura // linhas
    x, y = posicao
    linha = x // espaco
    coluna = y // espaco
    return linha, coluna


def desenhar_grade(janela, linhas, largura):
    espaco = largura // linhas
    for i in range(linhas):
        pygame.draw.line(janela, cores.CINZA, (0, i * espaco), (largura, i * espaco))
        for j in range(linhas):
            pygame.draw.line(janela, cores.CINZA, (j * espaco, 0), (j * espaco, largura))


def desenhar(janela: Surface, grade, linhas, largura):
    janela.fill(cores.BRANCO)
    for linha in grade:
        for bloco in linha:
            bloco.desenhar(janela)
            if bloco.tem_esfera():
                bloco.esfera.desenhar(janela)
            if bloco.tem_agente():
                bloco.agente.desenhar(janela)
    desenhar_grade(janela, linhas, largura)
    pygame.display.update()


def clicou_botao_esquerdo_mouse():
    return pygame.mouse.get_pressed()[0]


def clicou_botao_direito_mouse():
    return pygame.mouse.get_pressed()[2]


def teclou(evento: Event):
    return evento.type == pygame.KEYDOWN


def teclou_c(evento: Event):
    if evento.type == pygame.KEYDOWN:
        return evento.key == pygame.K_c
    return False


def teclou_espaco(evento: Event):
    if evento.type == pygame.KEYDOWN:
        return evento.key == pygame.K_SPACE
    return False


def clicou_fechar_janela():
    for evento in pygame.event.get():
        return evento.type == pygame.QUIT


def fechar_janela():
    pygame.quit()


