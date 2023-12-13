from pyamaze import maze, agent
from queue import PriorityQueue

destino = (1, 1)


def h_score(celula, destino):
    linha_celula = celula[0]
    coluna_celula = celula[1]

    linha_destino = destino[0]
    coluna_destino = destino[1]

    return abs(coluna_celula - coluna_destino) + abs(linha_celula - linha_destino)


def estrela(labirinto):
    f_score = {celula: float("inf") for celula in labirinto.grid}
    g_score = {}
    celula_inicial = (labirinto.rows, labirinto.cols)
    g_score[celula_inicial] = 0
    f_score[celula_inicial] = g_score[celula_inicial] + h_score(celula_inicial, destino)

    print(f_score)

    fila = PriorityQueue()
    item = (f_score[celula_inicial], h_score(celula_inicial, destino), celula_inicial)
    fila.put(item)

    caminho = {}
    while not fila.empty():
        celula = fila.get()[2]

        if celula == destino:
            break

        for direcao in "NSEW":
            if labirinto.maze_map[celula][direcao] == 1:
                linha_celula = celula[0]
                coluna_celula = celula[1]
                if direcao == "N":
                    proxima_celula = (linha_celula - 1, coluna_celula)
                elif direcao == "S":
                    proxima_celula = (linha_celula + 1, coluna_celula)
                elif direcao == "E":
                    proxima_celula = (linha_celula, coluna_celula + 1)
                elif direcao == "W":
                    proxima_celula = (linha_celula, coluna_celula - 1)

                novo_g_score = g_score[celula] + 1
                novo_f_score = novo_g_score + h_score(proxima_celula, destino)

                if novo_f_score < f_score[proxima_celula]:
                    f_score[proxima_celula] = novo_f_score
                    g_score[proxima_celula] = novo_g_score
                    item = (
                        novo_f_score,
                        h_score(proxima_celula, destino),
                        proxima_celula,
                    )
                    fila.put(item)
                    caminho[proxima_celula] = celula

    caminho_final = {}
    celula_analisada = destino
    while celula_analisada != celula_inicial:
        caminho_final[caminho[celula_analisada]] = celula_analisada
        celula_analisada = caminho[celula_analisada]
    return caminho_final


labirinto = maze(20, 20)
labirinto.CreateMaze()

# print(labirinto.grid)

agente = agent(labirinto, filled=True, footprints=True)
caminho = estrela(labirinto)
labirinto.tracePath({agente: caminho}, delay=100)
labirinto.run()
