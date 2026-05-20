from bibgrafo.grafo_matriz_adj_dir import *
from bibgrafo.grafo_errors import *

class MeuGrafo(GrafoMatrizAdjacenciaDirecionado):

    def vertices_nao_adjacentes(self):
        '''
        Provê uma lista de vértices não adjacentes no grafo. A lista terá o seguinte formato: [X-Z, X-W, ...]
        Onde X, Z e W são vértices no grafo que não tem uma aresta entre eles.
        :return: Uma lista com os pares de vértices não adjacentes
        '''
        nao_adjacentes = set()
        n = len(self.vertices)

        for i in range(n):
            for j in range(n):
                # célula vazia significa que não há aresta de i -> j
                if not self.matriz[i][j]:
                    v1 = self.vertices[i].rotulo
                    v2 = self.vertices[j].rotulo
                    nao_adjacentes.add(f"{v1}-{v2}")

        return nao_adjacentes

    def ha_laco(self):
        '''
        Verifica se existe algum laço no grafo.
        :return: Um valor booleano que indica se existe algum laço.
        '''
        for i in range(len(self.vertices)):
            if self.matriz[i][i]:  # dicionário não vazio = tem aresta
                return True
        return False


    def grau_entrada(self, V=''):
        '''
        Provê o grau do vértice passado como parâmetro
        :param V: O rótulo do vértice a ser analisado
        :return: Um valor inteiro que indica o grau do vértice
        :raises: VerticeInvalidoException se o vértice não existe no grafo
        '''
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError(f"O vértice '{V}' não existe no grafo.")

        j = self.indice_do_vertice(self.get_vertice(V))
        grau = 0
        for i in range(len(self.vertices)):
            grau += len(self.matriz[i][j])  # conta arestas que chegam em V
        return grau

    def grau_saida(self, V=''):
        '''
        Provê o grau do vértice passado como parâmetro
        :param V: O rótulo do vértice a ser analisado
        :return: Um valor inteiro que indica o grau do vértice
        :raises: VerticeInvalidoException se o vértice não existe no grafo
        '''
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError(f"O vértice '{V}' não existe no grafo.")

        i = self.indice_do_vertice(self.get_vertice(V))
        grau = 0
        for j in range(len(self.vertices)):
            grau += len(self.matriz[i][j])  # conta arestas que partem de V
        return grau

    def ha_paralelas(self):
        '''
        Verifica se há arestas paralelas no grafo
        :return: Um valor booleano que indica se existem arestas paralelas no grafo.
        '''
        n = len(self.vertices)
        for i in range(n):
            for j in range(n):
                if len(self.matriz[i][j]) > 1:
                    return True
        return False

    def arestas_sobre_vertice(self, V):
        '''
        Provê uma lista que contém os rótulos das arestas que incidem sobre o vértice passado como parâmetro
        :param V: O vértice a ser analisado
        :return: Uma lista os rótulos das arestas que incidem sobre o vértice
        :raises: VerticeInvalidoException se o vértice não existe no grafo
        '''
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError(f"O vértice '{V}' não existe no grafo.")

        idx = self.indice_do_vertice(self.get_vertice(V))
        arestas = set()
        n = len(self.vertices)

        for j in range(n):
            # arestas que SAEM de V (linha)
            for rotulo in self.matriz[idx][j]:
                arestas.add(rotulo)
            # arestas que CHEGAM em V (coluna)
            for rotulo in self.matriz[j][idx]:
                arestas.add(rotulo)

        return arestas

    def eh_completo(self):
        '''
        Verifica se o grafo é completo.
        :return: Um valor booleano que indica se o grafo é completo
        '''
        if self.ha_laco() or self.ha_paralelas():
            return False

        n = len(self.vertices)
        for i in range(n):
            for j in range(n):
                if i != j and not self.matriz[i][j]:
                    return False
        return True

    def warshall(self):
        '''
        Provê a matriz de alcançabilidade de Warshall do grafo
        :return: Uma lista de listas que representa a matriz de alcançabilidade de Warshall associada ao grafo
        '''
        n = len(self.vertices)

        # Inicializa a matriz: True se há aresta direta, False caso contrário
        matriz_w = []
        for i in range(n):
            linha = []
            for j in range(n):
                linha.append(bool(self.matriz[i][j]))
            matriz_w.append(linha)

        # Algoritmo de Warshall
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if matriz_w[i][k] and matriz_w[k][j]:
                        matriz_w[i][j] = True

        return matriz_w

    def menor_caminho(self, vi, vf):
        '''
            Encontra o menor caminho entre dois vértices em um grafo direcionado ponderado.
            Utiliza o algoritmo de Dijkstra. Se houver pesos negativos, informa que não é possível calcular.
            :param vi: O rótulo do vértice de partida
            :param vf: O rótulo do vértice de destino
            :return: Uma tupla (custo, caminho) onde custo é o peso total e caminho é a lista de vértices
            :raises: VerticeInvalidoError se algum dos vértices não existe no grafo
            '''
        if not self.existe_rotulo_vertice(vi):
            raise VerticeInvalidoError(f"O vértice '{vi}' não existe no grafo.")
        if not self.existe_rotulo_vertice(vf):
            raise VerticeInvalidoError(f"O vértice '{vf}' não existe no grafo.")

        # Verifica pesos negativos
        n = len(self.vertices)
        for i in range(n):
            for j in range(n):
                for rotulo, aresta in self.matriz[i][j].items():
                    if aresta.peso < 0:
                        return "Não é possível calcular o menor caminho: há pesos negativos no grafo."

        # Inicializa estruturas do Dijkstra
        infinito = float('inf')
        distancia = {v.rotulo: infinito for v in self.vertices}
        distancia[vi] = 0
        anterior = {v.rotulo: None for v in self.vertices}
        nao_visitados = {v.rotulo for v in self.vertices}

        while nao_visitados:
            # Escolhe o vértice não visitado com menor distância
            atual = min(nao_visitados, key=lambda v: distancia[v])

            if distancia[atual] == infinito:
                break  # restante inacessível

            if atual == vf:
                break

            nao_visitados.remove(atual)

            idx_atual = self.indice_do_vertice(self.get_vertice(atual))

            # Percorre os vizinhos (arestas que saem de atual)
            for j in range(n):
                vizinho = self.vertices[j].rotulo
                if vizinho not in nao_visitados:
                    continue
                for rotulo, aresta in self.matriz[idx_atual][j].items():
                    nova_dist = distancia[atual] + aresta.peso
                    if nova_dist < distancia[vizinho]:
                        distancia[vizinho] = nova_dist
                        anterior[vizinho] = atual

        # Reconstrói o caminho
        if distancia[vf] == infinito:
            return f"Não existe caminho de '{vi}' até '{vf}'."

        caminho = []
        atual = vf
        while atual is not None:
            caminho.insert(0, atual)
            atual = anterior[atual]

        return distancia[vf], caminho