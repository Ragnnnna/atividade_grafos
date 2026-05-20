from bibgrafo.grafo_lista_adj_nao_dir import GrafoListaAdjacenciaNaoDirecionado
from bibgrafo.vertice import Vertice

g = GrafoListaAdjacenciaNaoDirecionado()

# Adicionando vértices
for rotulo in ['J', 'C', 'E', 'P', 'M', 'T', 'Z']:
    g.adiciona_vertice(Vertice(rotulo))

# Adicionando arestas
g.adiciona_aresta('a1', 'J', 'C')
g.adiciona_aresta('a2', 'C', 'E')
g.adiciona_aresta('a3', 'C', 'E')  # paralela a a2
g.adiciona_aresta('a4', 'C', 'P')
g.adiciona_aresta('a5', 'C', 'P')  # paralela a a4
g.adiciona_aresta('a6', 'C', 'M')
g.adiciona_aresta('a7', 'C', 'T')
g.adiciona_aresta('a8', 'M', 'T')
g.adiciona_aresta('a9', 'T', 'Z')

print(g)