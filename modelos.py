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
    def __init__(self, nome: str, inicio: int = 0, fim: int = 0, prioridade: int = 0, duracao: int = 0, prazo: int = 0):
        self.nome = nome
        self.inicio = inicio 
        self.fim = fim       
        self.prioridade = prioridade
        self.duracao = duracao 
        self.prazo = prazo   
    def to_dict(self):
        return {
            "nome": self.nome,
            "inicio": self.inicio,
            "fim": self.fim,
            "prioridade": self.prioridade,
            "duracao": self.duracao,
            "prazo": self.prazo
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
def scheduling_min_lateness(tarefas: List[Tarefa]) -> Tuple[int, List[Tuple[Tarefa, int, int]]]:
    tarefas_validas = [t for t in tarefas if t.duracao > 0 and t.prazo > 0]
    tarefas_ordenadas = sorted(tarefas_validas, key=lambda t: t.prazo)
    tempo_atual = 0 
    lateness_maxima = 0 
    lateness_total = 0 
    tarefas_agendadas_com_tempos = [] 
    for t in tarefas_ordenadas:
        tempo_inicio_real = tempo_atual
        tempo_termino_real = tempo_atual + t.duracao
        lateness_individual = max(0, tempo_termino_real - t.prazo) 
        lateness_maxima = max(lateness_maxima, lateness_individual)
        lateness_total += lateness_individual 
        tarefas_agendadas_com_tempos.append((t, tempo_inicio_real, tempo_termino_real))
        tempo_atual = tempo_termino_real 
    return lateness_total, tarefas_agendadas_com_tempos
def knapsack(capacidade: int, itens: List[Item]) -> List[Item]:
    n = len(itens)
    dp = [[0] * (capacidade + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(capacidade + 1):
            peso_atual = itens[i - 1].peso
            utilidade_atual = itens[i - 1].utilidade
            if peso_atual <= w:
                dp[i][w] = max(
                    dp[i - 1][w],  
                    dp[i - 1][w - peso_atual] + utilidade_atual  
                )
            else:
                dp[i][w] = dp[i - 1][w]
    resultado_itens = []
    w = capacidade
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            resultado_itens.append(itens[i - 1])
            w -= itens[i - 1].peso
    return resultado_itens[::-1]  
def heuristica_balanceamento(mochilas: Dict[str, List[Item]]) -> int:
    pesos = [sum(item.peso for item in lista) for lista in mochilas.values()]
    return max(pesos) - min(pesos) if pesos else 0
GRADE_EXEMPLO = {
    "segunda": ["SO", "Cálculo"],
    "terca": ["Algoritmos"],
    "quarta": ["SO", "Arquitetura"],
    "quinta": ["Cálculo", "Algoritmos"],
    "sexta": []
}
MATERIAIS = {
    "SO": [Item("Livro SO", 2, 8), Item("Notebook", 3, 9)],
    "Cálculo": [Item("Livro Cálculo", 2, 7), Item("Caderno", 1, 5)],
    "Algoritmos": [Item("Notebook", 3, 9), Item("Caderno", 1, 5)],
    "Física": [Item("Livro Arquitetura", 2, 6), Item("Calculadora", 1, 4)]
}
ITENS_FIXOS = [
    Item("Garrafa", 1, 3),
    Item("Fone de ouvido", 1, 2),
    Item("Lanche", 1, 4)
]

CAPACIDADE_PADRAO = 7
TAREFAS_EXEMPLO = [
    Tarefa("Revisar SO", inicio=8, fim=10, prioridade=5, duracao=2, prazo=10),
    Tarefa("Listas Cálculo", inicio=9, fim=11, prioridade=8, duracao=3, prazo=12),
    Tarefa("Projeto Algoritmos", inicio=10, fim=12, prioridade=10, duracao=4, prazo=15),
    Tarefa("Trabalho de Arquitetura", inicio=13, fim=15, prioridade=7, duracao=2, prazo=16),
    Tarefa("Resumo geral", inicio=11, fim=13, prioridade=6, duracao=2, prazo=13)
]
def montar_mochilas(grade: Dict[str, List[str]]) -> Dict[str, List[Item]]:
    resultado = {}
    for dia, disciplinas in grade.items():
        itens_dia = ITENS_FIXOS[:]  
        for d in disciplinas:
            itens_dia.extend(MATERIAIS.get(d, []))
        resultado[dia] = knapsack(CAPACIDADE_PADRAO, itens_dia)
    return resultado
def mostrar_resultado(mochilas: Dict[str, List[Item]]):
    """Exibe o resultado da montagem das mochilas."""
    print("\n--- Mochilas da Semana ---")
    for dia, itens in mochilas.items():
        nomes = [item.nome for item in itens]
        peso_total = sum(i.peso for i in itens)
        utilidade_total = sum(i.utilidade for i in itens)
        print(f"{dia.title()}: {nomes} (Peso Total: {peso_total}kg, Utilidade Total: {utilidade_total})")
    print("\nHeurística de Balanceamento (Diferença de peso entre a mochila mais pesada e a mais leve):", heuristica_balanceamento(mochilas))
def mostrar_estudo_intervalado(tarefas: List[Tarefa]):
    """Exibe o plano de estudo otimizado usando Interval Scheduling."""
    print("\n--- Plano de Estudo Otimizado (Interval Scheduling) ---")
    selecionadas = interval_scheduling(tarefas)
    if not selecionadas:
        print("Nenhuma tarefa pôde ser agendada.")
    else:
        for t in selecionadas:
            print(f"{t.nome}: {t.inicio}h - {t.fim}h (Prioridade {t.prioridade})")
def mostrar_min_lateness(tarefas: List[Tarefa]):
    print("\n--- Plano de Estudo Otimizado (Scheduling Minimum Lateness) ---")
    lateness_total, tarefas_agendadas = scheduling_min_lateness(tarefas)
    if not tarefas_agendadas:
        print("Nenhuma tarefa pôde ser agendada com duração e prazo definidos.")
    else:
        print(f"Lateness Máxima Total: {lateness_total} horas")
        for t, inicio_real, termino_real in tarefas_agendadas:
            lateness_individual = max(0, termino_real - t.prazo)
            print(f" - {t.nome} (Duração: {t.duracao}h, Prazo: {t.prazo}h) -> "
                  f"Início Real: {inicio_real}h, Término Real: {termino_real}h, "
                  f"Lateness: {lateness_individual}h")

if __name__ == "__main__":
    mochilas = montar_mochilas(GRADE_EXEMPLO)
    mostrar_resultado(mochilas)
    mostrar_estudo_intervalado(TAREFAS_EXEMPLO)
    mostrar_min_lateness(TAREFAS_EXEMPLO)
