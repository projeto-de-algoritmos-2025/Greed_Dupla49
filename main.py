import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import json
from typing import List, Dict
from modelos import Item, Tarefa, knapsack, interval_scheduling, montar_mochilas, scheduling_min_lateness
from funcoes_algoritmos import otimizar_distribuicao
from manipulacao import Perfil, salvar_perfil, carregar_perfil 
from interface_utils import knapsack_para_disciplina
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Planejamento UNB - Algoritmos")
        self.geometry("800x600")
        self.perfil = None
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(expand=1, fill='both', padx=10, pady=10)
        self.criar_tab_perfil()
        self.criar_tab_visualizar()
        self.criar_tab_algoritmos()
    def criar_tab_perfil(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Perfil")
        btn_criar = ttk.Button(tab, text="Criar Novo Perfil", command=self._show_create_profile_dialog) 
        btn_criar.pack(pady=10)
        btn_carregar = ttk.Button(tab, text="Carregar Perfil de JSON", command=self.carregar_perfil)
        btn_carregar.pack(pady=10)
        btn_salvar = ttk.Button(tab, text="Salvar Perfil em JSON", command=self.salvar_perfil)
        btn_salvar.pack(pady=10)
        self.label_perfil = ttk.Label(tab, text="Nenhum perfil carregado.")
        self.label_perfil.pack(pady=20)
    def criar_tab_visualizar(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Visualizar")
        self.text_visualizar = tk.Text(tab, wrap='word', font=('Arial', 10))
        self.text_visualizar.pack(expand=1, fill='both', padx=10, pady=10)
        btn_atualizar = ttk.Button(tab, text="Atualizar Visualização", command=self.atualizar_visualizacao)
        btn_atualizar.pack(pady=5)
    def criar_tab_algoritmos(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Algoritmos")
        self.alg_label = ttk.Label(tab, text="Selecione o algoritmo para executar:")
        self.alg_label.pack(pady=10)
        self.alg_combo = ttk.Combobox(tab, values=["Knapsack", "Interval Scheduling", "A*", "Scheduling Min. Lateness"], state="readonly")
        self.alg_combo.set("Knapsack")
        self.alg_combo.pack(pady=5)
        self.btn_rodar = ttk.Button(tab, text="Executar Algoritmo", command=self.executar_algoritmo)
        self.btn_rodar.pack(pady=10)
        self.text_resultado = tk.Text(tab, height=20, wrap='word', font=('Arial', 10))
        self.text_resultado.pack(expand=1, fill='both', padx=10, pady=10)
    def _show_create_profile_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Criar Novo Perfil")
        dialog.geometry("600x700") 
        dialog.transient(self) 
        dialog.grab_set() 
        frame_nome = ttk.LabelFrame(dialog, text="Nome do Perfil")
        frame_nome.pack(padx=10, pady=5, fill='x')
        ttk.Label(frame_nome, text="Nome:").pack(side='left', padx=5)
        entry_nome_perfil = ttk.Entry(frame_nome)
        entry_nome_perfil.pack(side='left', fill='x', expand=True, padx=5)
        new_perfil = Perfil("TempProfile") 
        frame_tarefas = ttk.LabelFrame(dialog, text="Adicionar Tarefas")
        frame_tarefas.pack(padx=10, pady=5, fill='x')
        ttk.Label(frame_tarefas, text="Dia:").grid(row=0, column=0, padx=2, pady=2, sticky='w')
        entry_dia_tarefa = ttk.Entry(frame_tarefas)
        entry_dia_tarefa.grid(row=0, column=1, padx=2, pady=2, sticky='ew')
        ttk.Label(frame_tarefas, text="Nome:").grid(row=1, column=0, padx=2, pady=2, sticky='w')
        entry_nome_tarefa = ttk.Entry(frame_tarefas)
        entry_nome_tarefa.grid(row=1, column=1, padx=2, pady=2, sticky='ew')
        ttk.Label(frame_tarefas, text="Início (h):").grid(row=2, column=0, padx=2, pady=2, sticky='w')
        entry_inicio_tarefa = ttk.Entry(frame_tarefas)
        entry_inicio_tarefa.grid(row=2, column=1, padx=2, pady=2, sticky='ew')
        ttk.Label(frame_tarefas, text="Fim (h):").grid(row=3, column=0, padx=2, pady=2, sticky='w')
        entry_fim_tarefa = ttk.Entry(frame_tarefas)
        entry_fim_tarefa.grid(row=3, column=1, padx=2, pady=2, sticky='ew')
        ttk.Label(frame_tarefas, text="Prioridade:").grid(row=4, column=0, padx=2, pady=2, sticky='w')
        entry_prioridade_tarefa = ttk.Entry(frame_tarefas)
        entry_prioridade_tarefa.grid(row=4, column=1, padx=2, pady=2, sticky='ew')
        ttk.Label(frame_tarefas, text="Duração (h):").grid(row=5, column=0, padx=2, pady=2, sticky='w')
        entry_duracao_tarefa = ttk.Entry(frame_tarefas)
        entry_duracao_tarefa.grid(row=5, column=1, padx=2, pady=2, sticky='ew')
        ttk.Label(frame_tarefas, text="Prazo (h):").grid(row=6, column=0, padx=2, pady=2, sticky='w')
        entry_prazo_tarefa = ttk.Entry(frame_tarefas)
        entry_prazo_tarefa.grid(row=6, column=1, padx=2, pady=2, sticky='ew')
        def add_tarefa():
            dia = entry_dia_tarefa.get().strip().lower()
            nome = entry_nome_tarefa.get().strip()
            inicio_str = entry_inicio_tarefa.get().strip()
            fim_str = entry_fim_tarefa.get().strip()
            prioridade_str = entry_prioridade_tarefa.get().strip()
            duracao_str = entry_duracao_tarefa.get().strip()
            prazo_str = entry_prazo_tarefa.get().strip()
            if not (dia and nome and inicio_str and fim_str and prioridade_str):
                messagebox.showwarning("Erro", "Campos de tarefa (Dia, Nome, Início, Fim, Prioridade) são obrigatórios.", parent=dialog)
                return
            try:
                inicio = int(inicio_str)
                fim = int(fim_str)
                prioridade = int(prioridade_str)
                duracao = int(duracao_str) if duracao_str else 0
                prazo = int(prazo_str) if prazo_str else 0
                if dia not in new_perfil.grade:
                    new_perfil.grade[dia] = []
                new_perfil.grade[dia].append(Tarefa(nome=nome, inicio=inicio, fim=fim, prioridade=prioridade, duracao=duracao, prazo=prazo))
                messagebox.showinfo("Sucesso", f"Tarefa '{nome}' adicionada para {dia}.", parent=dialog)
                entry_nome_tarefa.delete(0, tk.END)
                entry_inicio_tarefa.delete(0, tk.END)
                entry_fim_tarefa.delete(0, tk.END)
                entry_prioridade_tarefa.delete(0, tk.END)
                entry_duracao_tarefa.delete(0, tk.END)
                entry_prazo_tarefa.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Erro", "Início, Fim, Prioridade, Duração e Prazo devem ser números inteiros.", parent=dialog)
        ttk.Button(frame_tarefas, text="Adicionar Tarefa", command=add_tarefa).grid(row=7, column=0, columnspan=2, pady=5)
        frame_materiais = ttk.LabelFrame(dialog, text="Adicionar Materiais")
        frame_materiais.pack(padx=10, pady=5, fill='x')
        ttk.Label(frame_materiais, text="Disciplina:").grid(row=0, column=0, padx=2, pady=2, sticky='w')
        entry_disciplina_material = ttk.Entry(frame_materiais)
        entry_disciplina_material.grid(row=0, column=1, padx=2, pady=2, sticky='ew')
        ttk.Label(frame_materiais, text="Nome Item:").grid(row=1, column=0, padx=2, pady=2, sticky='w')
        entry_nome_item = ttk.Entry(frame_materiais)
        entry_nome_item.grid(row=1, column=1, padx=2, pady=2, sticky='ew')
        ttk.Label(frame_materiais, text="Peso (kg):").grid(row=2, column=0, padx=2, pady=2, sticky='w')
        entry_peso_item = ttk.Entry(frame_materiais)
        entry_peso_item.grid(row=2, column=1, padx=2, pady=2, sticky='ew')
        ttk.Label(frame_materiais, text="Utilidade:").grid(row=3, column=0, padx=2, pady=2, sticky='w')
        entry_utilidade_item = ttk.Entry(frame_materiais)
        entry_utilidade_item.grid(row=3, column=1, padx=2, pady=2, sticky='ew')
        def add_material():
            disciplina = entry_disciplina_material.get().strip().lower()
            nome = entry_nome_item.get().strip()
            peso_str = entry_peso_item.get().strip()
            utilidade_str = entry_utilidade_item.get().strip()
            if not (disciplina and nome and peso_str and utilidade_str):
                messagebox.showwarning("Erro", "Todos os campos de material são obrigatórios.", parent=dialog)
                return
            try:
                peso = int(peso_str)
                utilidade = int(utilidade_str)
                if disciplina not in new_perfil.materiais:
                    new_perfil.materiais[disciplina] = []
                new_perfil.materiais[disciplina].append(Item(nome=nome, peso=peso, utilidade=utilidade))
                messagebox.showinfo("Sucesso", f"Material '{nome}' adicionado para {disciplina}.", parent=dialog)
                entry_nome_item.delete(0, tk.END)
                entry_peso_item.delete(0, tk.END)
                entry_utilidade_item.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Erro", "Peso e Utilidade devem ser números inteiros.", parent=dialog)
        ttk.Button(frame_materiais, text="Adicionar Material", command=add_material).grid(row=4, column=0, columnspan=2, pady=5)
        def finalize_profile():
            nome_final = entry_nome_perfil.get().strip()
            if not nome_final:
                messagebox.showwarning("Aviso", "O nome do perfil não pode ser vazio.", parent=dialog)
                return
            new_perfil.nome = nome_final 
            self.perfil = new_perfil
            self.label_perfil.config(text=f"Perfil '{self.perfil.nome}' criado e carregado.")
            messagebox.showinfo("Sucesso", f"Perfil '{self.perfil.nome}' criado e carregado com sucesso!", parent=dialog)
            self.atualizar_visualizacao()
            dialog.destroy() 
        ttk.Button(dialog, text="Criar Perfil", command=finalize_profile).pack(pady=10)
        frame_tarefas.grid_columnconfigure(1, weight=1)
        frame_materiais.grid_columnconfigure(1, weight=1)
    def criar_perfil(self): 
        self._show_create_profile_dialog()
    def carregar_perfil(self):
        path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
        if path:
            try:
                self.perfil = carregar_perfil(path)
                self.label_perfil.config(text=f"Perfil '{self.perfil.nome}' carregado.")
                messagebox.showinfo("Sucesso", f"Perfil '{self.perfil.nome}' carregado com sucesso.")
                self.atualizar_visualizacao()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar perfil: {e}\nVerifique se o arquivo é um JSON válido.")
        else:
            messagebox.showinfo("Informação", "Nenhum arquivo selecionado para carregar.")
    def salvar_perfil(self):
        if not self.perfil:
            messagebox.showwarning("Aviso", "Nenhum perfil carregado para salvar.")
            return

        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
        if path:
            try:
                salvar_perfil(self.perfil, path)
                messagebox.showinfo("Sucesso", f"Perfil '{self.perfil.nome}' salvo com sucesso em '{path}'.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar perfil: {e}")
        else:
            messagebox.showinfo("Informação", "Operação de salvar cancelada.")
    def atualizar_visualizacao(self):
        self.text_visualizar.delete("1.0", tk.END)

        if not self.perfil:
            self.text_visualizar.insert(tk.END, "Nenhum perfil carregado.\nCrie ou carregue um perfil na aba 'Perfil'.")
            return
        texto = f"--- Perfil: {self.perfil.nome} ---\n\n"
        texto += "--- Grade Semanal (Dia, Disciplina, Início, Fim, Prioridade, Duração, Prazo) ---\n"
        if not self.perfil.grade:
            texto += "Nenhuma tarefa cadastrada.\n"
        else:
            for dia in sorted(self.perfil.grade.keys()):
                texto += f"{dia.title()}:\n"
                if not self.perfil.grade[dia]:
                    texto += "  - Nenhuma tarefa para este dia.\n"
                else:
                    for t in self.perfil.grade[dia]:
                        texto += (f"  - {t.nome}: {t.inicio}h às {t.fim}h (Prio {t.prioridade})"
                                  f" (Duração: {t.duracao}h, Prazo: {t.prazo}h)\n")
        texto += "\n"
        texto += "--- Materiais (Disciplina, Nome do Item, Peso, Utilidade) ---\n"
        if not self.perfil.materiais:
            texto += "Nenhum material cadastrado.\n"
        else:
            for disc in sorted(self.perfil.materiais.keys()):
                texto += f"{disc.title()}:\n"
                if not self.perfil.materiais[disc]:
                    texto += "  - Nenhum material para esta disciplina.\n"
                else:
                    for i in self.perfil.materiais[disc]:
                        texto += f"  - {i.nome} (Peso: {i.peso}kg, Utilidade: {i.utilidade})\n"
        texto += "\n"
        texto += "Para editar, você pode salvar o perfil, editar o JSON manualmente e recarregar.\n"
        texto += "Ou, para adicionar novos dados, use a função de criação de perfil interativa no console.\n"
        self.text_visualizar.insert(tk.END, texto)
    def executar_algoritmo(self):
        if not self.perfil:
            messagebox.showwarning("Aviso", "Nenhum perfil carregado. Por favor, crie ou carregue um perfil primeiro.")
            return
        alg = self.alg_combo.get()
        self.text_resultado.delete("1.0", tk.END)
        if alg == "Knapsack":
            self.resultado_knapsack()
        elif alg == "Interval Scheduling":
            self.resultado_interval_scheduling()
        elif alg == "A*":
            self.resultado_a_estrela()
        elif alg == "Scheduling Min. Lateness":
            self.resultado_min_lateness()
        else:
            messagebox.showwarning("Aviso", "Selecione um algoritmo válido na lista.")
    def resultado_knapsack(self):
        texto_resultado = "--- Resultado do Algoritmo Knapsack ---\n"
        if not self.perfil.materiais:
            texto_resultado += "Nenhum material cadastrado no perfil para aplicar o Knapsack.\n"
            self.text_resultado.insert(tk.END, texto_resultado)
            return
        capacidade_padrao_knapsack = 10
        for disc, itens in self.perfil.materiais.items():
            texto_resultado += f"\nDisciplina: {disc.title()}\n"
            texto_resultado += f"Capacidade da Mochila: {capacidade_padrao_knapsack}kg\n"
            if not itens:
                texto_resultado += "  - Não há materiais cadastrados para esta disciplina.\n"
                continue
            utilidade_total, selecionados = knapsack_para_disciplina(itens, capacidade_padrao_knapsack)
            peso_total_selecionado = sum(item.peso for item in selecionados)
            texto_resultado += f"Utilidade Total Selecionada: {utilidade_total}\n"
            texto_resultado += f"Peso Total dos Itens Selecionados: {peso_total_selecionado}kg\n"
            texto_resultado += "Itens selecionados:\n"
            if not selecionados:
                texto_resultado += "  - Nenhum item selecionado para esta capacidade.\n"
            else:
                for item in selecionados:
                    texto_resultado += f"  - {item.nome} (peso {item.peso}kg, utilidade {item.utilidade})\n"
        self.text_resultado.insert(tk.END, texto_resultado)
    def resultado_interval_scheduling(self):
        texto_resultado = "--- Resultado do Algoritmo Interval Scheduling ---\n"
        if not self.perfil.grade:
            texto_resultado += "Nenhuma grade semanal cadastrada no perfil para aplicar o Interval Scheduling.\n"
            self.text_resultado.insert(tk.END, texto_resultado)
            return
        for dia in sorted(self.perfil.grade.keys()):
            tarefas_do_dia = self.perfil.grade[dia]
            agendadas = interval_scheduling(tarefas_do_dia)
            texto_resultado += f"\nDia: {dia.title()}\n"
            texto_resultado += "Tarefas agendadas:\n"
            if not agendadas:
                texto_resultado += "  - Nenhuma tarefa pôde ser agendada neste dia.\n"
            else:
                for t in agendadas:
                    texto_resultado += f"  - {t.nome} ({t.inicio}h às {t.fim}h, Prioridade {t.prioridade})\n"
        self.text_resultado.insert(tk.END, texto_resultado)
    def resultado_min_lateness(self):
        texto_resultado = "--- Resultado do Algoritmo Scheduling Minimum Lateness ---\n"
        if not self.perfil.grade:
            texto_resultado += "Nenhuma grade semanal cadastrada no perfil para aplicar o Scheduling Min Lateness.\n"
            self.text_resultado.insert(tk.END, texto_resultado)
            return
        todas_tarefas = []
        for dia_tarefas in self.perfil.grade.values():
            todas_tarefas.extend(dia_tarefas)
        tarefas_validas = [t for t in todas_tarefas if t.duracao > 0 and t.prazo > 0]
        if not tarefas_validas:
            texto_resultado += "Nenhuma tarefa com duração e prazo definidos para aplicar o Scheduling Min Lateness.\n"
            self.text_resultado.insert(tk.END, texto_resultado)
            return
        lateness_total, tarefas_agendadas = scheduling_min_lateness(tarefas_validas)
        texto_resultado += f"\nLateness Total (soma das latenesses individuais): {lateness_total} horas\n"
        texto_resultado += "Tarefas Agendadas (Ordem de Execução):\n"
        if not tarefas_agendadas:
            texto_resultado += "  - Nenhuma tarefa pôde ser agendada com os critérios fornecidos.\n"
        else:
            for t, inicio_real, termino_real in tarefas_agendadas:
                lateness_individual = max(0, termino_real - t.prazo)
                texto_resultado += (f"  - {t.nome} (Duração: {t.duracao}h, Prazo: {t.prazo}h) -> "
                                    f"Início Real: {inicio_real}h, Término Real: {termino_real}h, "
                                    f"Lateness: {lateness_individual}h\n")
        self.text_resultado.insert(tk.END, texto_resultado)
    def resultado_a_estrela(self):
        texto_resultado = "--- Resultado do Algoritmo A* (Balanceamento de Mochilas) ---\n"
        if not self.perfil.grade:
            texto_resultado += "Nenhuma grade semanal cadastrada para montar as mochilas e aplicar A*.\n"
            self.text_resultado.insert(tk.END, texto_resultado)
            return
        mochilas_iniciais = montar_mochilas(self.perfil.grade)
        texto_resultado += "--- Distribuição Antes da Otimização ---\n"
        texto_resultado += self.formatar_mochilas_a_estrela(mochilas_iniciais)
        texto_resultado += "\nIniciando busca A* para otimização do balanceamento...\n"
        otimizado = otimizar_distribuicao(mochilas_iniciais)
        if otimizado:
            texto_resultado += "\n--- Distribuição Depois da Otimização ---\n"
            texto_resultado += self.formatar_mochilas_a_estrela(otimizado)
        else:
            texto_resultado += "\nNão foi possível encontrar uma melhoria significativa com A* dentro do limite de iterações.\n"
            texto_resultado += "A distribuição inicial pode já estar otimizada ou o limite de iterações foi atingido."
        self.text_resultado.insert(tk.END, texto_resultado)
    def formatar_mochilas_a_estrela(self, mochilas: Dict[str, List[Item]]) -> str:
        texto = ""
        for dia in sorted(mochilas.keys()):
            itens = mochilas[dia]
            nomes_itens = [item.nome for item in itens]
            peso_total = sum(item.peso for item in itens)
            utilidade_total = sum(item.utilidade for item in itens)
            texto += f"{dia.title()}: {', '.join(nomes_itens)} (Peso Total: {peso_total}kg, Utilidade Total: {utilidade_total})\n"
        return texto
if __name__ == "__main__":
    app = App()
    app.mainloop()
