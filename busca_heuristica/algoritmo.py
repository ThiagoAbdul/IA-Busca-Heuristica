from queue import PriorityQueue

from gui.gui import clicou_fechar_janela, fechar_janela
from model.classes import Bloco


def heuristica(ponto1, ponto2):
    x1, y1 = ponto1
    x2, y2 = ponto2
    return (abs(x1 - x2) + abs(y1 - y2)) * 2


def melhor_camiho(blocos_anteriores, bloco_atual, desenhar):
    blocos_melhor_caminho = [bloco_atual]
    while bloco_atual in blocos_anteriores:
        bloco_atual = blocos_anteriores[bloco_atual]
        bloco_atual.virar_caminho()
        desenhar()
        blocos_melhor_caminho.append(bloco_atual)
    return blocos_melhor_caminho


def a_estrela(desenhar, grade, bloco_inicial: Bloco, bloco_final: Bloco):
    caminhos = PriorityQueue()
    caminhos.put((0, bloco_inicial))
    infinito = float("inf")
    veio_de = {}
    custos_percorridos = {bloco: infinito for linha in grade for bloco in linha}
    custos_percorridos[bloco_inicial] = 0
    heuristicas = {bloco: infinito for linha in grade for bloco in linha}
    heuristicas[bloco_inicial] = heuristica(bloco_inicial.posicao(), bloco_final.posicao())

    hash_blocos = {bloco_inicial}

    while not caminhos.empty():
        if clicou_fechar_janela():
            fechar_janela()
        bloco_atual: Bloco = caminhos.get()[1]
        hash_blocos.remove(bloco_atual)

        if bloco_atual == bloco_final:
            blocos_melhor_caminho = melhor_camiho(veio_de, bloco_final, desenhar)
            bloco_final.virar_destino()
            return blocos_melhor_caminho

        for bloco_adjacente in bloco_atual.blocos_adjacentes:
            # MODIFY
            custo_percorrido_temp = custos_percorridos[bloco_atual] + bloco_adjacente.custo

            if custo_percorrido_temp < custos_percorridos[bloco_adjacente]:
                veio_de[bloco_adjacente] = bloco_atual
                custos_percorridos[bloco_adjacente] = custo_percorrido_temp
                heuristicas[bloco_adjacente] = custo_percorrido_temp + heuristica(bloco_adjacente.posicao(),
                                                                                  bloco_final.posicao())

                if bloco_adjacente not in hash_blocos:

                    caminhos.put((heuristicas[bloco_adjacente],  bloco_adjacente))
                    hash_blocos.add(bloco_adjacente)
                    bloco_adjacente.abrir()

        desenhar()

        if bloco_atual != bloco_inicial:
            bloco_atual.clarear()

    return False
