import csv

class Graph:
    def __init__(self):
        self.grafo = {}
        self.nomes = {}  # Dicionário para armazenar nomes das atividades

    def add_edge(self, u, v, w):
        if u not in self.grafo:
            self.grafo[u] = {'dependencias': [], 'duracao': 0, 'dependentes': []}
        if v not in self.grafo:
            self.grafo[v] = {'dependencias': [], 'duracao': 0, 'dependentes': []}
        self.grafo[u]['dependentes'].append((v, w))  # (nodo dependente, peso)

    def longest_path(self, start, end):
        # Inicializa distâncias e predecessores
        dist = {node: -float('inf') for node in self.grafo}
        pred = {node: None for node in self.grafo}
        dist[start] = 0

        # Relaxação das arestas
        for _ in range(len(self.grafo) - 1):
            for u in self.grafo:
                for v, w in self.grafo[u]['dependentes']:
                    if dist[u] != -float('inf'):
                        new_dist = dist[u] + self.grafo[v]['duracao']  # Usando a duração correta
                        if dist[v] < new_dist:
                            dist[v] = new_dist
                            pred[v] = u

        # Verifica se há ciclos negativos
        for u in self.grafo:
            for v, w in self.grafo[u]['dependentes']:
                if dist[u] != -float('inf') and dist[v] < dist[u] + self.grafo[v]['duracao']:
                    return False, None  # ciclo negativo encontrado

        return True, dist[end], self._get_path(pred, end)

    def _get_path(self, pred, end):
        path = []
        while end is not None:
            path.append(end)
            end = pred[end]
        path.reverse()  # Inverter para obter a ordem correta
        return path

def ler_csv_como_grafo_como_s_t(caminho_csv):
    grafo = Graph()

    with open(caminho_csv, mode='r', encoding='utf-8') as arquivo:
        leitor_csv = csv.reader(arquivo)
        next(leitor_csv)  # Ignorar cabeçalho

        for linha in leitor_csv:
            codigo, nome, periodo, duracao, dependencias = linha
            duracao = int(duracao)

            # Adiciona o nodo ao grafo e armazena o nome
            grafo.nomes[codigo] = nome  # Armazena o nome da atividade
            grafo.grafo[codigo] = {'dependencias': [], 'duracao': duracao, 'dependentes': []}  # Adiciona a duração

            # Adiciona as dependências se existirem
            if dependencias:
                dependencias_lista = dependencias.split(';')
                for dep in dependencias_lista:
                    grafo.add_edge(dep, codigo, 0)  # Não usamos a duração aqui, pois a dependência é um ponto de conexão

    # Adicionando nós fictícios 's' e 't'
    grafo.add_edge('s', 's', 0)  # Nó inicial
    grafo.add_edge('t', 't', 0)  # Nó final

    # Conectar nodos que não têm dependências ao nó inicial 's'
    for codigo in grafo.grafo:
        if codigo != 's' and not grafo.grafo[codigo]['dependencias']:
            grafo.add_edge('s', codigo, 0)

    # Conectar nodos que não têm mais dependências ao nó final 't'
    for codigo in grafo.grafo:
        if codigo != 't' and all(dep in grafo.grafo for dep in grafo.grafo[codigo]['dependencias']):
            grafo.add_edge(codigo, 't', 0)

    return grafo

def main():
    while True:
        caminho_csv = input("Informe o arquivo (0 para sair): ")
        if caminho_csv == "0":
            break

        print("Processando ...")
        
        try:
            grafo = ler_csv_como_grafo_como_s_t(caminho_csv)

            # Calcular o caminho mais longo do nó 's' para o nó 't'
            resultado = grafo.longest_path('s', 't')

            if resultado[0] is False:
                print("Ciclo negativo encontrado.")
            else:
                _, comprimento, caminho = resultado
                print("\nCaminho Crítico :")
                for atividade in caminho:
                    if atividade not in ['s', 't']:  # Ignorar nós fictícios
                        print(f"- {grafo.nomes[atividade]}")  # Imprimir o nome da atividade
                print(f"\nTempo Mínimo : {comprimento}")

        except FileNotFoundError:
            print("Arquivo não encontrado. Verifique o caminho e tente novamente.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()
