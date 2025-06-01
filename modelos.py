from typing import List, Dict, Tuple
import heapq
import json
class Item:
    def __init__(self, nome: str, peso: int, utilidade: int):
        self.nome = nome
        self.peso = peso
        self.utilidade = utilidade
    def to_dict(self):
        return {
            "nome": self.nome,
            "peso": self.peso,
            "utilidade": self.utilidade
        }
class Tarefa:
    def __init__(self, nome: str, inicio: int, fim: int, prioridade: int):
        self.nome = nome
        self.inicio = inicio
        self.fim = fim
        self.prioridade = prioridade
    def to_dict(self):
        return {
            "nome": self.nome,
            "inicio": self.inicio,
            "fim": self.fim,
            "prioridade": self.prioridade
        }
def interval_scheduling(tarefas: List[Tarefa]) -> List[Tarefa]:
    tarefas_ordenadas = sorted(tarefas, key=lambda t: t.fim)
    resultado = []
    fim_atual = -1
    for t in tarefas_ordenadas:
        if t.inicio >= fim_atual:
            resultado.append(t)
            fim_atual = t.fim
    return resultado
def knapsack(capacidade: int, itens: List[Item]) -> List[Item]:
    n = len(itens)
    dp = [[0] * (capacidade + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(capacidade + 1):
            if itens[i - 1].peso <= w:
                dp[i][w] = max(
                    dp[i - 1][w],
                    dp[i - 1][w - itens[i - 1].peso] + itens[i - 1].utilidade
                )
            else:
                dp[i][w] = dp[i - 1][w]
    resultado = []
    w = capacidade
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            resultado.append(itens[i - 1])
            w -= itens[i - 1].peso

    return resultado[::-1]  
def heuristica_balanceamento(mochilas: Dict[str, List[Item]]) -> int:
    pesos = [sum(item.peso for item in lista) for lista in mochilas.values()]
    return max(pesos) - min(pesos) if pesos else 0
GRADE_EXEMPLO = {
    "segunda": ["SO", "Cálculo"],
    "terca": ["Algoritmos"],
    "quarta": ["SO", "Física"],
    "quinta": ["Cálculo", "Algoritmos"],
    "sexta": []
}
MATERIAIS = {
    "SO": [Item("Livro SO", 2, 8), Item("Notebook", 3, 9)],
    "Cálculo": [Item("Livro Cálculo", 2, 7), Item("Caderno", 1, 5)],
    "Algoritmos": [Item("Notebook", 3, 9), Item("Caderno", 1, 5)],
    "Física": [Item("Livro Física", 2, 6), Item("Calculadora", 1, 4)]
}

ITENS_FIXOS = [
    Item("Garrafa", 1, 3),
    Item("Fone de ouvido", 1, 2),
    Item("Lanche", 1, 4)
]
CAPACIDADE_PADRAO = 7
TAREFAS_EXEMPLO = [
    Tarefa("Revisar SO", 8, 10, 5),
    Tarefa("Listas Cálculo", 9, 11, 8),
    Tarefa("Projeto Algoritmos", 10, 12, 10),
    Tarefa("Trabalho de Arquitetura", 13, 15, 7),
    Tarefa("Resumo geral", 11, 13, 6)
]
def montar_mochilas(grade: Dict[str, List[str]]) -> Dict[str, List[Item]]:
    resultado = {}
    for dia, disciplinas in grade.items():
        itens = ITENS_FIXOS[:]
        for d in disciplinas:
            itens.extend(MATERIAIS.get(d, []))
        resultado[dia] = knapsack(CAPACIDADE_PADRAO, itens)
    return resultado
def mostrar_resultado(mochilas: Dict[str, List[Item]]):
    print("\n--- Mochilas da Semana ---")
    for dia, itens in mochilas.items():
        nomes = [item.nome for item in itens]
        peso_total = sum(i.peso for i in itens)
        print(f"{dia.title()}: {nomes} (Total: {peso_total}kg)")
    print("\nHeurística de Balanceamento:", heuristica_balanceamento(mochilas))
def mostrar_estudo_intervalado(tarefas: List[Tarefa]):
    print("\n--- Plano de Estudo Otimizado (Interval Scheduling) ---")
    selecionadas = interval_scheduling(tarefas)
    for t in selecionadas:
        print(f"{t.nome}: {t.inicio}h - {t.fim}h (Prioridade {t.prioridade})")
if __name__ == "__main__":
    mochilas = montar_mochilas(GRADE_EXEMPLO)
    mostrar_resultado(mochilas)
    mostrar_estudo_intervalado(TAREFAS_EXEMPLO)
