import random
import time


from busca_heuristica.algoritmo import a_estrela, heuristica
from gui.gui import *

from model.classes import Bloco, Esfera, Agente, BlocoGrama, BlocoAgua, BlocoMontanha


def definir_pontos_de_busca(grade):
    pontos = []
    x = 3
    while x <= len(grade):
        y = 3
        while y <= len(grade):
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


def criar_grade_aleatoriamente(linhas, largura):
    grade = []
    espaco = largura // linhas

    for i in range(linhas):
        linha = []
        for j in range(linhas):
            bloco = Bloco.random_factory(i, j, espaco, linhas)
            linha.append(bloco)
        grade.append(linha)
    return grade


def criar_grade_por_arquivo(linhas, largura):
    grade = []
    espaco = largura // linhas

    with open('arquivos/mapa.txt', 'r') as f:
        data = f.read()
        rows = data.split('\n')
        numbers = [[int(x) for x in row.split()] for row in rows]

        #for row in numbers:
        #    print(' '.join(map(str, row)))

        for i in range(linhas):
            linha = []
            for j in range(linhas):
                if numbers[j][i] == 1:
                    bloco = BlocoGrama(i, j, espaco, linhas)
                if numbers[j][i] == 2:
                    bloco = BlocoAgua(i, j, espaco, linhas)
                if numbers[j][i] == 3:
                    bloco = BlocoMontanha(i, j, espaco, linhas)
                linha.append(bloco)
            grade.append(linha)
    return grade


def limpar_grade(grade):
    for linha in grade:
        for bloco in linha:
            bloco.reiniciar()


def main(janela, largura, ler_arquivo=False):
    contador_esferas = 0
    LINHAS = 42

    if ler_arquivo:
        grade = criar_grade_por_arquivo(LINHAS, largura)
    else:
        grade = criar_grade_aleatoriamente(LINHAS, largura)

    esferas = criar_esferas(grade, LINHAS, largura)
    pontos_de_busca = definir_pontos_de_busca(grade)
    for i, j in pontos_de_busca:
        grade[i][j].cor_atual = (0, 0, 0)
    em_execucao = True
    achou_esfera = False
    finalizou = False

    CASA_DO_KAMI = bloco_inicial = grade[LINHAS // 2][LINHAS // 2]
    agente = Agente.criar_agente_no_bloco(bloco_inicial)
    agente.abrir_radar(grade)

    for linha in grade:
        for bloco in linha:
            bloco.atualizar_blocos_adjacentes(grade)

    carregar_musica_de_fundo()

    ponto_mais_proximo = None
    try:
        while em_execucao:
            alterar_titulo(f"Custo total: {agente.custo_percorrido} \t\tEsferas coletadas: {contador_esferas}")
            desenhar(janela, grade, LINHAS, largura)
            time.sleep(0.5)
            limpar_grade(grade)
            if finalizou:
                x, y = CASA_DO_KAMI.posicao()
            else:
                esferas_localizadas = agente.esferas_localizadas()
                if len(esferas_localizadas) > 0:
                    x, y = ponto_mais_proximo = get_ponto_mais_proximo(bloco_inicial.posicao(),
                                                                       map(Bloco.posicao,
                                                                           esferas_localizadas))
                    achou_esfera = True
                else:
                    x, y = ponto_mais_proximo = get_ponto_mais_proximo(bloco_inicial.posicao(), pontos_de_busca)
            bloco_final = grade[x][y]
            blocos_melhor_caminho = a_estrela(
                lambda: desenhar(janela, grade, LINHAS, largura),
                grade,
                bloco_inicial,
                bloco_final
            )
            while len(blocos_melhor_caminho) > 0:
                b = blocos_melhor_caminho.pop()
                agente.ir_para_bloco(b)
                limpar_grade(grade)
                agente.abrir_radar(grade)
                if not achou_esfera:
                    esferas_localizadas = agente.esferas_localizadas()
                    if len(esferas_localizadas) > 0:
                        x, y = ponto_mais_proximo = get_ponto_mais_proximo(bloco.posicao(),
                                                                           map(Bloco.posicao,
                                                                               esferas_localizadas))
                        bloco_final = grade[x][y]
                        achou_esfera = True
                        blocos_melhor_caminho = a_estrela(
                            lambda: desenhar(janela, grade, LINHAS, largura),
                            grade,
                            agente.bloco_atual,
                            bloco_final
                        )
                desenhar(janela, grade, LINHAS, largura)
                time.sleep(0.2)
            if finalizou:
                alterar_titulo(f"Custo final: {agente.custo_percorrido}")
                em_execucao = False
                while not clicou_fechar_janela():
                    pass
            if achou_esfera:
                emitir_som_de_pegar_esfera()
                esferas.remove(bloco_final.esfera)
                contador_esferas += 1
                if len(esferas) == 0:
                    finalizou = True
                    desenhar(janela, grade, LINHAS, largura)
                bloco_final.esfera = None
                achou_esfera = False
            elif ponto_mais_proximo in pontos_de_busca:
                pontos_de_busca.remove(ponto_mais_proximo)
            for i, j in pontos_de_busca:
                grade[i][j].cor_atual = (0, 0, 0)
            bloco_inicial = agente.bloco_atual
            if clicou_fechar_janela():
                em_execucao = False
        fechar_janela()
    except pygame.error:
        print('Até mais')


LARGURA_TELA = 630
ALTURA_TELA = 630
JANELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Algoritmo A*")

main(JANELA, LARGURA_TELA, ler_arquivo=True)
