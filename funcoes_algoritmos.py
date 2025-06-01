import heapq  
from itertools import count  
from copy import deepcopy
from typing import Optional, Set, List, Dict  
from modelos import Item, Tarefa, montar_mochilas, mostrar_resultado, GRADE_EXEMPLO, TAREFAS_EXEMPLO, heuristica_balanceamento, scheduling_min_lateness 
class Estado:
    def __init__(self, distribuicao: Dict[str, List['Item']]):
        self.distribuicao = deepcopy(distribuicao) 
    def __hash__(self):
        rep = []
        for dia in sorted(self.distribuicao.keys()):
            nomes = tuple(sorted(item.nome for item in self.distribuicao[dia]))
            rep.append((dia, nomes))
        return hash(tuple(rep))
    def __eq__(self, other):
        return isinstance(other, Estado) and self.__hash__() == other.__hash__()
def peso_dia(itens: List['Item']) -> int:
    return sum(i.peso for i in itens)
def custo_estado(estado: Estado) -> int:
    return heuristica_balanceamento(estado.distribuicao)
def gerar_sucessores(estado: Estado) -> List[Estado]:
    sucessores = []
    dias = list(estado.distribuicao.keys())
    for d_origem in dias:
        itens_no_dia_origem = list(estado.distribuicao[d_origem])
        for item in itens_no_dia_origem:
            for d_destino in dias:
                if d_destino != d_origem: 
                    novo_estado_dist = deepcopy(estado.distribuicao)
                    if item in novo_estado_dist[d_origem]: 
                        novo_estado_dist[d_origem].remove(item)
                    novo_estado_dist[d_destino].append(item)
                    sucessores.append(Estado(novo_estado_dist))
    return sucessores
def a_estrela(inicial: Estado, limite_iter=2000) -> Optional[Estado]:
    aberto = []
    fechado: Set[int] = set()
    contador = count()
    g_scores = {hash(inicial): 0}
    f_score_inicial = custo_estado(inicial)
    heapq.heappush(aberto, (f_score_inicial, 0, next(contador), inicial))
    iter_count = 0
    while aberto and iter_count < limite_iter:
        iter_count += 1
        f, g, _, atual = heapq.heappop(aberto)
        if custo_estado(atual) == 0:
            return atual  
        fechado.add(hash(atual))
        for succ in gerar_sucessores(atual):
            h = custo_estado(succ) 
            g_succ = g + 1 
            f_succ = g_succ + h 
            h_hash = hash(succ)
            if h_hash in fechado:
                continue
            if h_hash not in g_scores or g_succ < g_scores[h_hash]:
                g_scores[h_hash] = g_succ
                heapq.heappush(aberto, (f_succ, g_succ, next(contador), succ))
    return None  
def otimizar_distribuicao(mochilas: Dict[str, List['Item']]) -> Optional[Dict[str, List['Item']]]:
    estado_inicial = Estado(mochilas)
    resultado = a_estrela(estado_inicial)
    if resultado:
        return resultado.distribuicao
    return None
if __name__ == "__main__":
    print("--- Otimização A* de Mochilas ---")
    mochilas_iniciais = montar_mochilas(GRADE_EXEMPLO)
    print("\nDistribuição Inicial:")
    mostrar_resultado(mochilas_iniciais)
    mochilas_otimizadas = otimizar_distribuicao(mochilas_iniciais)
    if mochilas_otimizadas:
        print("\nDistribuição Otimizada:")
        mostrar_resultado(mochilas_otimizadas)
    else:
        print("\nNão foi possível encontrar uma distribuição otimizada dentro do limite de iterações.")
