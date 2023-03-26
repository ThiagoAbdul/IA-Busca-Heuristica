import random

from busca_heuristica.algoritmo import a_estrela, heuristica
from gui.gui import *

from model.classes import Bloco, Esfera, Agente


def definir_pontos_de_busca(grade):
    pontos = []
    x = 3
    while x <= 42:
        y = 3
        while y <= 42:
            pontos.append((x, y))
            y += 7
        x += 7
    return pontos


def get_ponto_mais_proximo(ponto_atual, pontos):
    ponto_mais_proximo = None
    for ponto in pontos:
        if ponto_mais_proximo is None:
            ponto_mais_proximo = ponto
        elif heuristica(ponto_atual, ponto) < heuristica(ponto_atual, ponto_mais_proximo):
            ponto_mais_proximo = ponto
    return ponto_mais_proximo


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
    pontos_de_busca = definir_pontos_de_busca(grade)
    for i, j in pontos_de_busca:
        grade[i][j].cor_atual = (0, 0, 0)
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
                    # bloco.iniciar()
                    agente = Agente.criar_agente_no_bloco(bloco_inicial)
                    agente.abrir_radar(grade)
                    x, y = ponto_mais_proximo = get_ponto_mais_proximo(bloco.posicao(), pontos_de_busca)
                    # bloco_final = grade[x][y]
                elif bloco_final is None and bloco != bloco_inicial:
                    bloco_final = bloco
                    bloco_final.virar_destino()
                    # TODO

                elif bloco != bloco_final and bloco != bloco_inicial:
                    pass
                # TODO

            elif clicou_botao_direito_mouse():
                pass
            # TODO
            if teclou(evento):
                if teclou_espaco(evento) and bloco_inicial is not None and bloco_final is not None:
                    agente.fechar_radar(grade)
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
