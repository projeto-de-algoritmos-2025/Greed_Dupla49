import heapq  # Fila de prioridade para A*
from typing import List, Dict, Optional, Set  # Tipos auxiliares
from copy import deepcopy
from itertools import count  # Contador incremental para desempate no heap
class Item:  # Representa um objeto com nome e peso
    def __init__(self, nome: str, peso: int): self.nome = nome; self.peso = peso
    def __eq__(self, other): return isinstance(other, Item) and self.nome == other.nome and self.peso == other.peso
    def __hash__(self): return hash((self.nome, self.peso))
    def __repr__(self): return f"Item('{self.nome}', {self.peso})"
class Estado:  # representa o estado da distribuição de itens
    def __init__(self, distribuicao: Dict[str, List[Item]]): self.distribuicao = distribuicao
    def __eq__(self, other): return isinstance(other, Estado) and self.distribuicao == other.distribuicao
    def __hash__(self): return hash(frozenset((dia, tuple(sorted(itens, key=lambda x: x.nome))) for dia, itens in self.distribuicao.items()))
    def __repr__(self): return str(self.distribuicao)
def custo_estado(estado: Estado) -> int:  # Calcula diferença entre dia mais cheio e mais leve
    pesos = [sum(item.peso for item in itens) for itens in estado.distribuicao.values()]
    return max(pesos) - min(pesos)
def gerar_sucessores(estado: Estado) -> List[Estado]:  # Move um item de um dia para outro
    dias = list(estado.distribuicao.keys()); sucessores = []
    for d_origem in dias:
        for item in estado.distribuicao[d_origem]:
            for d_destino in dias:
                if d_destino != d_origem:
                    novo_estado = deepcopy(estado.distribuicao)
                    try: novo_estado[d_origem].remove(item); novo_estado[d_destino].append(item); sucessores.append(Estado(novo_estado))
                    except ValueError: continue  # Item não encontrado
    return sucessores
def a_estrela(inicial: Estado, limite_iter: int = 1000) -> Optional[Estado]:  # Busca A* para encontrar distribuição ideal
    aberto = []; fechado: Set[int] = set(); contador = count()
    heapq.heappush(aberto, (custo_estado(inicial), 0, next(contador), inicial))
    g_scores = {hash(inicial): 0}
    for _ in range(limite_iter):
        if not aberto: break
        _, g, _, atual = heapq.heappop(aberto); h = hash(atual)
        if h in fechado: continue
        fechado.add(h)
        if custo_estado(atual) == 0: return atual
        for succ in gerar_sucessores(atual):
            h_succ = hash(succ); g_succ = g + 1; f_succ = g_succ + custo_estado(succ)
            if h_succ not in g_scores or g_succ < g_scores[h_succ]:
                g_scores[h_succ] = g_succ
                heapq.heappush(aberto, (f_succ, g_succ, next(contador), succ))
    return None
def otimizar_distribuicao(distribuicao: Dict[str, List[Item]]) -> Optional[Dict[str, List[Item]]]:  # Executa A* e retorna resultado
    estado_inicial = Estado(distribuicao); resultado = a_estrela(estado_inicial)
    return resultado.distribuicao if resultado else None
def mostrar_resultado(distribuicao: Dict[str, List[Item]]) -> None:  # Exibe itens por dia e peso total
    for dia, itens in distribuicao.items():
        total = sum(item.peso for item in itens)
        nomes = ', '.join(item.nome for item in itens)
        print(f"{dia.capitalize()}: {nomes} (Total: {total}kg)")
