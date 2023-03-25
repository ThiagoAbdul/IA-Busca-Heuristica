import random

from busca_heuristica.algoritmo import a_estrela
from gui.gui import *

from model.classes import Bloco, Esfera


def criar_esferas(grade, linhas, largura):
    esferas = []
    espaco = largura // linhas
    while len(esferas) < 7:
        i = random.randint(0, 41)
        j = random.randint(0, 41)
        nova_esfera = Esfera(i, j, espaco, linhas)
        bloco = grade[i][j]
        if bloco.tem_esfera():
            continue
        bloco.esfera = nova_esfera
        esferas.append(nova_esfera)
    return esferas


def criar_grade(linhas, largura):
    grade = []
    espaco = largura // linhas

    for i in range(linhas):
        linha = []
        for j in range(linhas):
            bloco = Bloco.random_factory(i, j, espaco, linhas)
            linha.append(bloco)
        grade.append(linha)
    return grade


def main(janela, largura):
    LINHAS = 42
    grade = criar_grade(LINHAS, largura)
    esferas = criar_esferas(grade, LINHAS, largura)

    bloco_inicial = bloco_final = None
    em_execucao = True

    while em_execucao:
        desenhar(janela, grade, LINHAS, largura)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                em_execucao = False
            if clicou_botao_esquerdo_mouse():
                linha, coluna = get_posicao_click(LINHAS, largura)
                bloco = grade[linha][coluna]
                if bloco_inicial is None and bloco != bloco_final:
                    bloco_inicial = bloco
                    bloco.iniciar()
                elif bloco_final is None and bloco != bloco_inicial:
                    bloco_final = bloco
                    bloco_final.finalizar()

                elif bloco != bloco_final and bloco != bloco_inicial:
                    bloco.virar_barreira()

            elif clicou_botao_direito_mouse():
                pass
            # TODO
            if teclou(evento):
                if evento.key == pygame.K_SPACE and bloco_inicial is not None and bloco_final is not None:
                    for linha in grade:
                        for bloco in linha:
                            bloco.atualizar_blocos_adjacentes(grade)
                    a_estrela(
                        lambda: desenhar(janela, grade, LINHAS, largura),
                        grade,
                        bloco_inicial,
                        bloco_final
                    )
                if teclou_c(evento):
                    bloco_inicial = bloco_final = None
                    grade = criar_grade(LINHAS, largura)

    fechar_janela()


LARGURA_TELA = 600
ALTURA_TELA = 600
JANELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Algoritmo a*")

main(JANELA, LARGURA_TELA)
