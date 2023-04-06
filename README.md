# Trabalho de IA

## Desafio
#### Criar um agente que ajuda o Goku a localizar as esferas do Dragão para ressucitar o Kuririn.
#### Implementação do algoritmo A* na *Busca Heurística* do agente.

## Regras
O agente deve coletar as 7 esferas do dragão e voltar para a casa do mestre Kami (centro do mapa) com o menor custo possível.
O mapa é composto por 3 tipos de terreno, sendo eles grama, água e montanha com os respectivos custos 1, 10 e 60.
O algoritmo calcula a melhor rota para as esferas, porém o agente só sabe a posição das esferas quando a mesma aparece em seu radar (de 3 blocos adjacentes, totalizando uma matriz de 7 x 7).

## Estratégia
Enquanto o agente não sabe a coordenada da esfera, ele procura por pontos predefinidos na mapa, sendo 36 pontos distribuídos de tal forma que o radar consiga cobrir 100% do mapa sem repetição, pois o mapa é representado por uma matriz 42 x 42, e a área do radar é 7 x 7; dividindo o produto cartesiano de cada matriz, o resultado é justamente 36, que é a quantidade de pontos predefinidos.
O agente calcula qual ponto está mais próxima e já executa o algoritmo de *Busca Heurística* para traçar o melhor caminho para este ponto.  A cada passo ele verifica se há uma esfera no radar, e caso haja, calcula o melhor caminho à esfera.

## Conhecimentos
1. Python
1. OO
1. Algoritmo A*
1. Pygame
1. Estruturas de dados
