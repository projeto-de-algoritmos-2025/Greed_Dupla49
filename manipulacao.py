import json
from typing import Any, List, Dict
from modelos import Item, Tarefa
class Perfil:
    def __init__(self, nome: str):
        self.nome = nome
        self.grade: Dict[str, List[Tarefa]] = {}
        self.materiais: Dict[str, List[Item]] = {}
    def to_dict(self) -> Dict[str, Any]:
        return {
            "nome": self.nome, 
            "grade": {dia: [tarefa.to_dict() for tarefa in tarefas] for dia, tarefas in self.grade.items()},
            "materiais": {disc: [item.to_dict() for item in itens] for disc, itens in self.materiais.items()},
        }
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Perfil":
        perfil = cls(data["nome"])
        perfil.grade = {dia: [Tarefa(**tarefa_data) for tarefa_data in tarefas_list]
                        for dia, tarefas_list in data.get("grade", {}).items()}
        perfil.materiais = {disc: [Item(**item_data) for item_data in itens_list]
                            for disc, itens_list in data.get("materiais", {}).items()}
        return perfil
def salvar_perfil(perfil: Perfil, caminho: str) -> None:
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(perfil.to_dict(), f, indent=4, ensure_ascii=False)
        print(f"Perfil '{perfil.nome}' salvo em '{caminho}'.")
    except IOError as e:
        print(f"Erro ao salvar o perfil: {e}")
def carregar_perfil(caminho: str) -> Perfil:
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            data = json.load(f)
        perfil = Perfil.from_dict(data)
        print(f"Perfil '{perfil.nome}' carregado de '{caminho}'.")
        return perfil
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho}' não encontrado.")
        raise
    except json.JSONDecodeError:
        print(f"Erro: Conteúdo inválido no arquivo JSON '{caminho}'.")
        raise
    except Exception as e:
        print(f"Erro inesperado ao carregar perfil: {e}")
        raise
def criar_perfil_interativo() -> Perfil:
    nome = input("Digite o nome do perfil: ").strip()
    if not nome:
        print("Nome do perfil não pode ser vazio. Usando 'Novo Perfil'.")
        nome = "Novo Perfil"
    perfil = Perfil(nome)
    print("\n--- Inserir Grade Semanal ---")
    print("Formato: dia,disciplina,horario_inicio,horario_fim,prioridade[,duracao,prazo]")
    print("Ex: segunda,SO,8,10,5,2,10 (duracao e prazo são opcionais, mas necessários para Scheduling Min. Lateness)")
    print("Digite 'fim' para terminar.")
    while True:
        entrada = input("Tarefa: ").strip()
        if entrada.lower() == "fim":
            break
        try:
            partes = [x.strip() for x in entrada.split(",")]
            if not (5 <= len(partes) <= 7):
                raise ValueError("Formato incorreto. Use: dia,disciplina,horario_inicio,horario_fim,prioridade[,duracao,prazo]")
            dia, disc, ini_str, fim_str, prio_str = partes[0:5]
            inicio = int(ini_str)
            fim = int(fim_str)
            prioridade = int(prio_str)
            duracao = int(partes[5]) if len(partes) > 5 else 0
            prazo = int(partes[6]) if len(partes) > 6 else 0
            if dia not in perfil.grade:
                perfil.grade[dia] = []
            perfil.grade[dia].append(Tarefa(nome=disc, inicio=inicio, fim=fim, prioridade=prioridade, duracao=duracao, prazo=prazo))
            print(f"Tarefa '{disc}' adicionada para {dia}.")
        except ValueError as e:
            print(f"Erro de valor: {e}. Certifique-se de que horários, prioridade, duracao e prazo são números inteiros.")
        except Exception as e:
            print(f"Entrada inválida: {e}")
    print("\n--- Inserir Materiais por Disciplina ---")
    print("Formato: disciplina,nome_do_item,peso_do_item,utilidade_do_item (ex: SO,Livro SO,2,8)")
    print("Digite 'fim' para terminar.")
    while True:
        entrada = input("Material: ").strip()
        if entrada.lower() == "fim":
            break
        try:
            partes = [x.strip() for x in entrada.split(",")]
            if len(partes) != 4:
                raise ValueError("Formato incorreto. Use: disciplina,nome_do_item,peso_do_item,utilidade_do_item")
            disc, nome_item, peso_str, util_str = partes
            peso = int(peso_str)
            utilidade = int(util_str)
            if disc not in perfil.materiais:
                perfil.materiais[disc] = []
            perfil.materiais[disc].append(Item(nome=nome_item, peso=peso, utilidade=utilidade))
            print(f"Material '{nome_item}' adicionado para {disc}.")
        except ValueError as e:
            print(f"Erro de valor: {e}. Certifique-se de que peso e utilidade são números inteiros.")
        except Exception as e:
            print(f"Entrada inválida: {e}")
    return perfil
def menu_principal():
    perfis: Dict[str, Perfil] = {}
    print("Bem-vindo ao Planejamento - UNB!")
    while True:
        print("\n--- Menu Principal ---")
        print("1 - Criar novo perfil")
        print("2 - Carregar perfil existente")
        print("3 - Salvar perfil atual")
        print("4 - Listar perfis carregados na sessão")
        print("5 - Sair")
        opc = input("Escolha uma opção: ").strip()
        if opc == "1":
            p = criar_perfil_interativo()
            perfis[p.nome] = p
            print(f"Perfil '{p.nome}' criado e carregado.")
        elif opc == "2":
            caminho = input("Digite o caminho do arquivo JSON do perfil: ").strip()
            try:
                p = carregar_perfil(caminho)
                perfis[p.nome] = p
                print(f"Perfil '{p.nome}' carregado com sucesso.")
            except Exception:
                print("Falha ao carregar o perfil. Verifique o caminho e o formato do arquivo.")
        elif opc == "3":
            if not perfis:
                print("Nenhum perfil para salvar. Crie ou carregue um primeiro.")
                continue
            nome_perfil_salvar = input("Digite o nome do perfil a ser salvo: ").strip()
            if nome_perfil_salvar in perfis:
                caminho_salvar = input("Digite o caminho completo para salvar o arquivo JSON (Ex: perfil.json): ").strip()
                salvar_perfil(perfis[nome_perfil_salvar], caminho_salvar)
            else:
                print(f"Perfil '{nome_perfil_salvar}' não encontrado na sessão.")
        elif opc == "4":
            if not perfis:
                print("Nenhum perfil carregado na sessão.")
            else:
                print("Perfis carregados:", list(perfis.keys()))
        elif opc == "5":
            print("Saindo do Planejamento UNB. Até mais!")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção de 1 a 5.")
if __name__ == "__main__":
    menu_principal()