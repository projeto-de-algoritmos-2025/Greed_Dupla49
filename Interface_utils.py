from typing import List, Dict, Tuple
from modelos import Item, Tarefa, knapsack, interval_scheduling, montar_mochilas, mostrar_resultado, scheduling_min_lateness
from funcoes_algoritmos import otimizar_distribuicao
from manipulacao import Perfil, criar_perfil_interativo
def knapsack_para_disciplina(itens: List[Item], capacidade: int) -> Tuple[int, List[Item]]:
    selecionados = knapsack(capacidade, itens)
    utilidade_total = sum(item.utilidade for item in selecionados)
    return utilidade_total, selecionados
def rodar_knapsack(perfil: Perfil):
    print("\n--- Knapsack para cada disciplina ---")
    if not perfil.materiais:
        print("Nenhum material cadastrado no perfil para aplicar o Knapsack.")
        return
    for disc, itens in perfil.materias.items():
        print(f"\nDisciplina: {disc.title()}")
        try:
            capacidade_str = input(f"Capacidade da mochila para {disc.title()} (kg, padrão 10): ").strip()
            capacidade = int(capacidade_str) if capacidade_str else 10
            if capacidade <= 0:
                raise ValueError("A capacidade deve ser um número positivo.")
        except ValueError as e:
            print(f"Entrada inválida: {e}. Usando capacidade padrão de 10kg.")
            capacidade = 10
        if not itens:
            print(f"Não há materiais cadastrados para {disc.title()}.")
            continue
        utilidade, selecionados = knapsack_para_disciplina(itens, capacidade)
        peso_total = sum(item.peso for item in selecionados)
        print(f"Capacidade da Mochila: {capacidade}kg")
        print(f"Utilidade Total Selecionada: {utilidade}")
        print(f"Peso Total dos Itens Selecionados: {peso_total}kg")
        print("Itens selecionados:")
        if not selecionados:
            print(" - Nenhum item selecionado para esta capacidade.")
        else:
            for item in selecionados:
                print(f" - {item.nome} (peso {item.peso}kg, utilidade {item.utilidade})")
def rodar_interval_scheduling(perfil: Perfil):
    print("\n--- Interval Scheduling para cada dia ---")
    if not perfil.grade:
        print("Nenhuma grade semanal cadastrada no perfil para aplicar o Interval Scheduling.")
        return
    for dia, tarefas in perfil.grade.items():
        agendadas = interval_scheduling(tarefas)
        print(f"\nDia: {dia.title()}")
        print("Tarefas agendadas:")
        if not agendadas:
            print(" - Nenhuma tarefa pôde ser agendada neste dia.")
        else:
            for t in agendadas:
                print(f" - {t.nome} ({t.inicio}h às {t.fim}h, Prioridade {t.prioridade})")
def rodar_min_lateness(perfil: Perfil):
    print("\n--- Scheduling Minimum Lateness ---")
    if not perfil.grade:
        print("Nenhuma grade semanal cadastrada no perfil para aplicar o Scheduling Min Lateness.")
        return
    todas_tarefas = []
    for dia_tarefas in perfil.grade.values():
        todas_tarefas.extend(dia_tarefas)
    tarefas_validas = [t for t in todas_tarefas if t.duracao > 0 and t.prazo > 0]
    if not tarefas_validas:
        print("Nenhuma tarefa com duração e prazo definidos para aplicar o Scheduling Min Lateness.")
        return
    lateness_total, tarefas_agendadas = scheduling_min_lateness(tarefas_validas)
    print(f"\nLateness Total (soma das latenesses individuais): {lateness_total} horas")
    print("Tarefas Agendadas (Ordem de Execução):")
    if not tarefas_agendadas:
        print(" - Nenhuma tarefa pôde ser agendada.")
    else:
        for t, inicio_real, termino_real in tarefas_agendadas:
            lateness_individual = max(0, termino_real - t.prazo)
            print(f" - {t.nome} (Duração: {t.duracao}h, Prazo: {t.prazo}h) -> "
                  f"Início Real: {inicio_real}h, Término Real: {termino_real}h, "
                  f"Lateness: {lateness_individual}h")
def rodar_a_estrela(perfil: Perfil):
    print("\n--- Otimização A* da distribuição semanal ---")
    if not perfil.grade:
        print("Nenhuma grade semanal cadastrada para montar as mochilas e aplicar A*.")
        return
    mochilas_iniciais = montar_mochilas(perfil.grade)
    print("Antes da otimização:")
    mostrar_resultado(mochilas_iniciais)
    print("\nIniciando busca A* para otimização...")
    otimizado = otimizar_distribuicao(mochilas_iniciais)
    if otimizado:
        print("\nDepois da otimização:")
        mostrar_resultado(otimizado)
    else:
        print("Nenhuma melhoria significativa encontrada com A* dentro do limite de iterações.")
def menu_algoritmos(perfil: Perfil):
    while True:
        print("\n--- Escolha o algoritmo para executar ---")
        print("1 - Knapsack (otimização de material por disciplina)")
        print("2 - Interval Scheduling (otimização de tarefas diárias)")
        print("3 - A* (balancear peso da mochila semanal)")
        print("4 - Scheduling Minimum Lateness (otimização de prazo de tarefas)") # Nova opção
        print("5 - Voltar ao Menu Principal")
        opc = input("Opção: ").strip()
        if opc == "1":
            rodar_knapsack(perfil)
        elif opc == "2":
            rodar_interval_scheduling(perfil)
        elif opc == "3":
            rodar_a_estrela(perfil)
        elif opc == "4":
            rodar_min_lateness(perfil)
        elif opc == "5":
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção de 1 a 5.")
if __name__ == "__main__":
    print("Este é um módulo utilitário para interfaces. Para uma experiência completa, execute App_gui.py.")
    print("Você pode criar um perfil de exemplo aqui para testar as funções de algoritmo.")
    perfil_teste = criar_perfil_interativo()
    if perfil_teste:
        menu_algoritmos(perfil_teste)