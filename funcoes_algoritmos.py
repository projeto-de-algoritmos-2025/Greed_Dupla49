import heapq  # Fila de prioridade para A*
from itertools import count  # Gerador incremental para desempate no heap
from copy import deepcopy
from typing import Optional, Set, List, Dict  # Tipos usados nas anotações
from modelos import Item, Tarefa, montar_mochilas, mostrar_resultado, GRADE_EXEMPLO, TAREFAS_EXEMPLO
class Estado:  # Representa um estado da distribuição
    def __init__(self, distribuicao: Dict[str, List['Item']]): self.distribuicao = distribuicao
    def __hash__(self):  # Define representação única baseada em nomes
        rep = []
        for dia in sorted(self.distribuicao.keys()): nomes = tuple(sorted(item.nome for item in self.distribuicao[dia])); rep.append((dia, nomes))
        return hash(tuple(rep))
    def __eq__(self, other): return isinstance(other, Estado) and self.__hash__() == other.__hash__()  #
def peso_dia(itens: List['Item']) -> int: return sum(i.peso for i in itens)  # Soma os pesos de um dia
def custo_estado(estado: Estado) -> int:  # Diferença entre dia mais cheio e mais leve
    pesos = [peso_dia(estado.distribuicao[dia]) for dia in estado.distribuicao]
    return max(pesos) - min(pesos)
def gerar_sucessores(estado: Estado) -> List[Estado]:  # Move um item entre dias
    sucessores = []
    dias = list(estado.distribuicao.keys())
    for d_origem in dias:
        for item in estado.distribuicao[d_origem]:
            for d_destino in dias:
                if d_destino != d_origem:
                    novo_estado = deepcopy(estado.distribuicao)
                    novo_estado[d_origem].remove(item)
                    novo_estado[d_destino].append(item)
                    sucessores.append(Estado(novo_estado))
    return sucessores
def a_estrela(inicial: Estado, limite_iter=1000) -> Optional[Estado]:  # Busca A* limitada
    aberto = []
    fechado: Set[int] = set()
    contador = count()
    heapq.heappush(aberto, (custo_estado(inicial), 0, next(contador), inicial))
    g_scores = {hash(inicial): 0}
    iter_count = 0
    while aberto and iter_count < limite_iter:
        iter_count += 1
        f, g, _, atual = heapq.heappop(aberto)
        if custo_estado(atual) == 0: return atual  # Solução ótima encontrada
        fechado.add(hash(atual))
        for succ in gerar_sucessores(atual):
            h = custo_estado(succ)
            g_succ = g + 1
            f_succ = g_succ + h
            h_hash = hash(succ)
            if h_hash in fechado: continue  # Já visitado
            if h_hash not in g_scores or g_succ < g_scores[h_hash]:  # Melhor caminho até agora
                g_scores[h_hash] = g_succ
                heapq.heappush(aberto, (f_succ, g_succ, next(contador), succ))
    return None  # Nenhuma solução dentro do limite
def otimizar_distribuicao(mochilas: Dict[str, List['Item']]) -> Optional[Dict[str, List['Item']]]:  # Interface de otimização
    estado_inicial = Estado(mochilas)
    resultado = a_estrela(estado_inicial)
    if resultado: return resultado.distribuicao
    return None
