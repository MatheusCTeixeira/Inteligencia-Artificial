import BFS
import DFSIterative
import DFSRecursive

from modelo_quebra_cabeca import listarAcoes
from modelo_quebra_cabeca import executarAcao
from modelo_quebra_cabeca import funcao_hash
from modelo_quebra_cabeca import comparar_estados
from modelo_quebra_cabeca import encoding
from modelo_quebra_cabeca import decoding

import modelo_quebra_cabeca_Astar

from time import time

def BFS_solution(estado_inicial, estado_objetivo):

    time_init = time()
    busca = BFS.BFS_algorithmcs(list_action_function=listarAcoes,
                                execute_action_function=executarAcao,
                                hash_function=funcao_hash,
                                cmp_function=comparar_estados)

    N = len(estado_inicial)
    estado_inicial = encoding(estado_inicial)
    estado_objetivo = encoding(estado_objetivo)

    solution = busca.BFS(estado_inicial, estado_objetivo)
    solution.E0 = decoding(estado_inicial)
    solution.Ef = decoding(estado_objetivo)
    solution.states = [decoding(x) for x in solution.states]
    solution.duration = time() - time_init
    solution.deepth = busca.graph.branching_factor()
    solution.width = busca.graph.deepth_factor()

    return solution


def DFS_Iter_solution(estado_inicial, estado_objetivo, deepth = 3):

    time_init = time()
    busca = DFSIterative.DFS_algorithmcs(list_action_function=listarAcoes,
                                         execute_action_function=executarAcao,
                                         hash_function=funcao_hash,
                                         cmp_function=comparar_estados)

    N = len(estado_inicial)
    estado_inicial = encoding(estado_inicial)
    estado_objetivo = encoding(estado_objetivo)

    solution = busca.DFS(estado_inicial, estado_objetivo, deepth)
    
    solution.E0 = decoding(estado_inicial)
    solution.Ef = decoding(estado_objetivo)    
    solution.states = [decoding(x) for x in solution.states]   
    solution.duration = time() - time_init
    solution.deepth = busca.graph.branching_factor()
    solution.width = busca.graph.deepth_factor()


    return solution


def DFS_Recr_solution(estado_inicial, estado_objetivo, deepth = 3):

    time_init = time()
    busca = DFSRecursive.DFS_algorithmcs(list_action_function=listarAcoes,
                                         execute_action_function=executarAcao,
                                         hash_function=funcao_hash,
                                         cmp_function=comparar_estados)

    N = len(estado_inicial)
    estado_inicial = encoding(estado_inicial)
    estado_objetivo = encoding(estado_objetivo)

    solution = busca.DFS(estado_inicial, estado_objetivo, deepth)
    
    solution.E0 = decoding(estado_inicial)
    solution.Ef = decoding(estado_objetivo)    
    solution.states = [decoding(x) for x in solution.states]
    solution.duration = time() - time_init
    solution.deepth = busca.graph.branching_factor()
    solution.width = busca.graph.deepth_factor()    

    return solution
