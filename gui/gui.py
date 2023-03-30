import pygame
from pygame import Surface
from pygame.event import Event

from model import cores


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


def clicou_fechar_janela():
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return True
    return False


def fechar_janela():
    pygame.quit()


def fechar_janela_ao_clicar():
    while True:
        if clicou_fechar_janela():
            pygame.quit()
            return


def alterar_titulo(titulo: str):
    pygame.display.set_caption(titulo)


def carregar_musica_de_fundo():
    pygame.init()
    pygame.mixer.init()
    musica_fundo = pygame.mixer.Sound('./arquivos/musica.mpeg')
    musica_fundo.set_volume(0.4)
    musica_fundo.play(-1)
    return musica_fundo


def emitir_som_de_pegar_esfera():
    efeito_sonoro = pygame.mixer.Sound('./arquivos/efeito.mpeg')
    efeito_sonoro.set_volume(0.6)
    efeito_sonoro.play()
