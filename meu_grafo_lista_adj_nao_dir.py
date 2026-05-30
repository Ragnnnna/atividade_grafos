from bibgrafo.grafo_lista_adj_nao_dir import GrafoListaAdjacenciaNaoDirecionado
from bibgrafo.grafo_errors import *


class MeuGrafo(GrafoListaAdjacenciaNaoDirecionado):

    def vertices_nao_adjacentes(self):
        '''
        Provê um conjunto de vértices não adjacentes no grafo.
        O conjunto terá o seguinte formato: {X-Z, X-W, ...}
        Onde X, Z e W são vértices no grafo que não tem uma aresta entre eles.
        :return: Um objeto do tipo set que contém os pares de vértices não adjacentes
        '''
        nao_adjacentes = set()
        adjacentes = set()

        for rotulo, aresta in self.arestas.items():
            par1 = f"{aresta.v1.rotulo}-{aresta.v2.rotulo}"
            par2 = f"{aresta.v2.rotulo}-{aresta.v1.rotulo}"
            adjacentes.add(par1)
            adjacentes.add(par2)

        vertices = self.vertices
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                par = f"{vertices[i].rotulo}-{vertices[j].rotulo}"
                par_inv = f"{vertices[j].rotulo}-{vertices[i].rotulo}"
                if par not in adjacentes and par_inv not in adjacentes:
                    nao_adjacentes.add(par)

        return nao_adjacentes

    def ha_laco(self):
        '''
        Verifica se existe algum laço no grafo.
        :return: Um valor booleano que indica se existe algum laço.
        '''
        for rotulo, aresta in self.arestas.items():
            if aresta.v1.rotulo == aresta.v2.rotulo:
                return True
        return False

    def grau(self, V=''):
        '''
        Provê o grau do vértice passado como parâmetro
        :param V: O rótulo do vértice a ser analisado
        :return: Um valor inteiro que indica o grau do vértice
        :raises: VerticeInvalidoError se o vértice não existe no grafo
        '''
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError(f"O vértice '{V}' não existe no grafo.")

        grau = 0
        for rotulo, aresta in self.arestas.items():
            if aresta.v1.rotulo == V and aresta.v2.rotulo == V:
                grau += 2  # laço conta duas vezes
            elif aresta.v1.rotulo == V or aresta.v2.rotulo == V:
                grau += 1
        return grau

    def ha_paralelas(self):
        '''
        Verifica se há arestas paralelas no grafo
        :return: Um valor booleano que indica se existem arestas paralelas no grafo.
        '''
        pares_vistos = set()
        for rotulo, aresta in self.arestas.items():
            # Uso frozenset para ignorar ordem: {A,B} == {B,A}
            par = frozenset([aresta.v1.rotulo, aresta.v2.rotulo])
            if par in pares_vistos:
                return True
            pares_vistos.add(par)
        return False

    def arestas_sobre_vertice(self, V):
        '''
        Provê uma lista que contém os rótulos das arestas que incidem sobre o vértice passado como parâmetro
        :param V: Um string com o rótulo do vértice a ser analisado
        :return: Uma lista os rótulos das arestas que incidem sobre o vértice
        :raises: VerticeInvalidoException se o vértice não existe no grafo
        '''

        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError(f"O vértice '{V}' não existe no grafo.")

        arestas = set()
        for rotulo, aresta in self.arestas.items():
            if aresta.v1.rotulo == V or aresta.v2.rotulo == V:
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
        # Um grafo não direcionado completo tem n*(n-1)/2 arestas
        return len(self.arestas) == n * (n - 1) // 2

    def ha_ciclo(self):
        '''
        Verifica se existe algum ciclo no grafo usando DFS.
        :return: False se não houver ciclo, ou uma lista com os vértices do ciclo encontrado.
        '''
        visitados = {}
        pai = {}

        for v in self.vertices:
            visitados[v.rotulo] = False
            pai[v.rotulo] = None

        def dfs(atual, pai_atual, caminho):
            visitados[atual] = True
            caminho.append(atual)

            for rotulo, aresta in self.arestas.items():
                # Verifica laço primeiro (aresta que sai e volta pro mesmo vértice)
                if aresta.v1.rotulo == atual and aresta.v2.rotulo == atual:
                    return [atual, atual]

                vizinho = None
                if aresta.v1.rotulo == atual and aresta.v2.rotulo != atual:
                    vizinho = aresta.v2.rotulo
                elif aresta.v2.rotulo == atual and aresta.v1.rotulo != atual:
                    vizinho = aresta.v1.rotulo

                if vizinho is None:
                    continue

                if not visitados[vizinho]:
                    resultado = dfs(vizinho, atual, caminho)
                    if resultado:
                        return resultado
                elif vizinho != pai_atual and vizinho in caminho:
                    idx = caminho.index(vizinho)
                    return caminho[idx:]

            caminho.pop()
            return False

        for v in self.vertices:
            if not visitados[v.rotulo]:
                resultado = dfs(v.rotulo, None, [])
                if resultado:
                    return resultado

        return False

    def eh_arvore(self):
        '''
        Verifica se o grafo é uma árvore (conexo e sem ciclos).
        Se for árvore, retorna uma lista com os vértices folha (grau 1).
        :return: False se não for árvore, ou uma lista com os nós folha.
        '''
        # Árvore não pode ter ciclo
        if self.ha_ciclo():
            return False

        # Árvore deve ser conexa — verifica com BFS
        visitados = set()
        inicio = self.vertices[0].rotulo
        fila = [inicio]
        visitados.add(inicio)

        while fila:
            atual = fila.pop(0)
            for rotulo, aresta in self.arestas.items():
                vizinho = None
                if aresta.v1.rotulo == atual:
                    vizinho = aresta.v2.rotulo
                elif aresta.v2.rotulo == atual:
                    vizinho = aresta.v1.rotulo

                if vizinho and vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append(vizinho)

        if len(visitados) != len(self.vertices):
            return False  # grafo desconexo

        # Coleta os nós folha (grau 1)
        folhas = [v.rotulo for v in self.vertices if self.grau(v.rotulo) == 1]
        return folhas

    def eh_bipartido(self):
        '''
        Verifica se o grafo é bipartido usando BFS com coloração.
        Um grafo é bipartido se seus vértices podem ser divididos em dois conjuntos
        sem que haja arestas entre vértices do mesmo conjunto.
        :return: Um valor booleano que indica se o grafo é bipartido.
        '''
        if self.ha_laco():
            return False

        cor = {}

        for v in self.vertices:
            if v.rotulo in cor:
                continue

            fila = [v.rotulo]
            cor[v.rotulo] = 0

            while fila:
                atual = fila.pop(0)

                for rotulo, aresta in self.arestas.items():
                    vizinho = None
                    if aresta.v1.rotulo == atual and aresta.v2.rotulo != atual:
                        vizinho = aresta.v2.rotulo
                    elif aresta.v2.rotulo == atual and aresta.v1.rotulo != atual:
                        vizinho = aresta.v1.rotulo

                    if vizinho is None:
                        continue

                    if vizinho not in cor:
                        cor[vizinho] = 1 - cor[atual]
                        fila.append(vizinho)
                    elif cor[vizinho] == cor[atual]:
                        return False
                    # se cor[vizinho] != cor[atual] → está correto, ignora

        return True