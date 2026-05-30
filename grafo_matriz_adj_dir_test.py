import unittest
from bibgrafo.aresta import ArestaDirecionada
from bibgrafo.grafo_errors import VerticeInvalidoError, ArestaInvalidaError
from bibgrafo.grafo_json import GrafoJSON
from bibgrafo.grafo_builder import GrafoBuilder
from meu_grafo_matriz_adj_dir import *

class TestGrafo(unittest.TestCase):

    def setUp(self):
        # Grafo da Paraíba
        self.g_p = GrafoJSON.json_to_grafo('test_json/grafo_pb.json', MeuGrafo())

        # Clone do Grafo da Paraíba para ver se o método equals está funcionando
        self.g_p2 = GrafoJSON.json_to_grafo('test_json/grafo_pb2.json', MeuGrafo())

        # Outro clone do Grafo da Paraíba para ver se o método equals está funcionando
        # Esse tem um pequena diferença na primeira aresta
        self.g_p3 = GrafoJSON.json_to_grafo('test_json/grafo_pb3.json', MeuGrafo())

        # Outro clone do Grafo da Paraíba para ver se o método equals está funcionando
        # Esse tem um pequena diferença na segunda aresta
        self.g_p4 = GrafoJSON.json_to_grafo('test_json/grafo_pb4.json', MeuGrafo())

        # Grafo da Paraíba sem arestas paralelas
        self.g_p_sem_paralelas = GrafoJSON.json_to_grafo('test_json/grafo_pb_simples.json', MeuGrafo())

        # Grafos completos
        self.g_c = GrafoBuilder().tipo(MeuGrafo()) \
            .vertices(['J', 'C', 'E', 'P']).arestas(True).build()

        self.g_c2 = GrafoBuilder().tipo(MeuGrafo()) \
            .vertices(3).arestas(True).build()

        self.g_c3 = GrafoBuilder().tipo(MeuGrafo()) \
            .vertices(1).build()


        # Grafos com laco
        self.g_l1 = GrafoJSON.json_to_grafo('test_json/grafo_l1.json', MeuGrafo())

        self.g_l2 = GrafoJSON.json_to_grafo('test_json/grafo_l2.json', MeuGrafo())

        self.g_l3 = GrafoJSON.json_to_grafo('test_json/grafo_l3.json', MeuGrafo())

        self.g_l4 = GrafoBuilder().tipo(MeuGrafo()).vertices([(v:=Vertice('D'))]) \
            .arestas([ArestaDirecionada('a1', v, v)]).build()

        self.g_l5 = GrafoBuilder().tipo(MeuGrafo()).vertices(3) \
            .arestas(3, lacos=1).build()

        # Grafos desconexos
        self.g_d = GrafoBuilder().tipo(MeuGrafo()) \
            .vertices([a:=Vertice('A'), b:=Vertice('B'), Vertice('C'), Vertice('D')]) \
            .arestas([ArestaDirecionada('asd', a, b)]).build()

        self.g_d2 = GrafoBuilder().tipo(MeuGrafo()).vertices(4).build()

        # Grafo com ciclos e laços
        self.g_e = MeuGrafo()
        self.g_e.adiciona_vertice("A")
        self.g_e.adiciona_vertice("B")
        self.g_e.adiciona_vertice("C")
        self.g_e.adiciona_vertice("D")
        self.g_e.adiciona_vertice("E")
        self.g_e.adiciona_aresta('1', 'A', 'B')
        self.g_e.adiciona_aresta('2', 'A', 'C')
        self.g_e.adiciona_aresta('3', 'C', 'A')
        self.g_e.adiciona_aresta('4', 'C', 'B')
        self.g_e.adiciona_aresta('10', 'C', 'B')
        self.g_e.adiciona_aresta('5', 'C', 'D')
        self.g_e.adiciona_aresta('6', 'D', 'D')
        self.g_e.adiciona_aresta('7', 'D', 'B')
        self.g_e.adiciona_aresta('8', 'D', 'E')
        self.g_e.adiciona_aresta('9', 'E', 'A')
        self.g_e.adiciona_aresta('11', 'E', 'B')

    def test_adiciona_aresta(self):
        self.assertTrue(self.g_p.adiciona_aresta('a10', 'J', 'C'))
        a = ArestaDirecionada("zxc", self.g_p.get_vertice("C"), self.g_p.get_vertice("Z"))
        self.assertTrue(self.g_p.adiciona_aresta(a))
        with self.assertRaises(ArestaInvalidaError):
            self.assertTrue(self.g_p.adiciona_aresta(a))
        with self.assertRaises(VerticeInvalidoError):
            self.assertTrue(self.g_p.adiciona_aresta('b1', '', 'C'))
        with self.assertRaises(VerticeInvalidoError):
            self.assertTrue(self.g_p.adiciona_aresta('b1', 'A', 'C'))
        with self.assertRaises(TypeError):
            self.g_p.adiciona_aresta('')
        with self.assertRaises(TypeError):
            self.g_p.adiciona_aresta('aa-bb')
        with self.assertRaises(VerticeInvalidoError):
            self.g_p.adiciona_aresta('x', 'J', 'V')
        with self.assertRaises(ArestaInvalidaError):
            self.g_p.adiciona_aresta('a1', 'J', 'C')

    def test_remove_vertice(self):
        self.assertTrue(self.g_p.remove_vertice("J"))
        with self.assertRaises(VerticeInvalidoError):
            self.g_p.remove_vertice("J")
        with self.assertRaises(VerticeInvalidoError):
            self.g_p.remove_vertice("K")
        self.assertTrue(self.g_p.remove_vertice("C"))
        self.assertTrue(self.g_p.remove_vertice("Z"))

    def test_remove_aresta(self):
        self.assertTrue(self.g_p.remove_aresta("a1"))
        self.assertFalse(self.g_p.remove_aresta("a1"))
        self.assertTrue(self.g_p.remove_aresta("a7"))
        self.assertFalse(self.g_c.remove_aresta("a"))
        self.assertTrue(self.g_c.remove_aresta("a6"))
        self.assertTrue(self.g_c.remove_aresta("a1", "J"))
        self.assertTrue(self.g_c.remove_aresta("a5", "C"))
        with self.assertRaises(VerticeInvalidoError):
            self.g_p.remove_aresta("a2", "X", "C")
        with self.assertRaises(VerticeInvalidoError):
            self.g_p.remove_aresta("a3", "X")
        with self.assertRaises(VerticeInvalidoError):
            self.g_p.remove_aresta("a3", v2="X")

    def test_eq(self):
        self.assertEqual(self.g_p, self.g_p2)
        self.assertNotEqual(self.g_p, self.g_p3)
        self.assertNotEqual(self.g_p, self.g_p_sem_paralelas)
        self.assertNotEqual(self.g_p, self.g_p4)

    def test_vertices_nao_adjacentes(self):
        self.assertEqual(set(self.g_p.vertices_nao_adjacentes()), {'J-E', 'J-P', 'J-M', 'J-T', 'J-Z', 'C-J', 'C-T', 'C-Z', 'C-M', 'C-P', 'E-C', 'E-J', 'E-P',
                                                                   'E-M', 'E-T', 'E-Z', 'P-J', 'P-E', 'P-M', 'P-T', 'P-Z', 'M-J', 'M-E', 'M-P', 'M-Z', 'T-J',
                                                                   'T-M', 'T-E', 'T-P', 'Z-J', 'Z-C', 'Z-E', 'Z-P', 'Z-M', 'Z-T'})


        self.assertEqual(set(self.g_c.vertices_nao_adjacentes()), {'C-J', 'E-C', 'P-C', 'E-J', 'P-E', 'P-J'})
        self.assertEqual(self.g_c3.vertices_nao_adjacentes(), [])
        self.assertEqual(set(self.g_e.vertices_nao_adjacentes()), {'A-D', 'A-E', 'B-A', 'B-C', 'B-D', 'B-E', 'C-E', 'D-C', 'D-A', 'E-D', 'E-C'})

    def test_ha_laco(self):
        self.assertFalse(self.g_p.ha_laco())
        self.assertFalse(self.g_p_sem_paralelas.ha_laco())
        self.assertFalse(self.g_c2.ha_laco())
        self.assertTrue(self.g_l1.ha_laco())
        self.assertTrue(self.g_l2.ha_laco())
        self.assertTrue(self.g_l3.ha_laco())
        self.assertTrue(self.g_l4.ha_laco())
        self.assertTrue(self.g_l5.ha_laco())
        self.assertTrue(self.g_e.ha_laco())

    def test_grau(self):
        # Paraíba
        self.assertEqual(self.g_p.grau_saida('J'), 1)
        self.assertEqual(self.g_p.grau_entrada('J'), 0)
        self.assertEqual(self.g_p.grau_saida('C'), 2)
        self.assertEqual(self.g_p.grau_entrada('C'), 5)
        self.assertEqual(self.g_p.grau_saida('E'), 0)
        self.assertEqual(self.g_p.grau_entrada('E'), 2)
        self.assertEqual(self.g_p.grau_saida('P'), 2)
        self.assertEqual(self.g_p.grau_entrada('P'), 0)
        self.assertEqual(self.g_p.grau_saida('M'), 2)
        self.assertEqual(self.g_p.grau_entrada('M'), 0)
        self.assertEqual(self.g_p.grau_saida('T'), 2)
        self.assertEqual(self.g_p.grau_entrada('T'), 1)
        self.assertEqual(self.g_p.grau_saida('Z'), 0)
        self.assertEqual(self.g_p.grau_entrada('Z'), 1)
        with self.assertRaises(VerticeInvalidoError):
            self.assertEqual(self.g_p.grau_saida('G'), 5)

        self.assertEqual(self.g_d.grau_entrada('A'), 0)
        self.assertEqual(self.g_d.grau_saida('A'), 1)
        self.assertEqual(self.g_d.grau_entrada('C'), 0)
        self.assertEqual(self.g_d.grau_saida('C'), 0)
        self.assertNotEqual(self.g_d.grau_entrada('D'), 2)
        self.assertNotEqual(self.g_d.grau_entrada('D'), 2)
        self.assertEqual(self.g_d2.grau_entrada('A'), 0)
        self.assertNotEqual(self.g_d.grau_saida('D'), 2)

        # Completos
        self.assertEqual(self.g_c.grau_entrada('J'), 0)
        self.assertEqual(self.g_c.grau_saida('J'), 3)
        self.assertEqual(self.g_c.grau_entrada('C'), 1)
        self.assertEqual(self.g_c.grau_saida('C'), 2)
        self.assertEqual(self.g_c.grau_saida('E'), 1)
        self.assertEqual(self.g_c.grau_entrada('E'), 2)
        self.assertEqual(self.g_c.grau_saida('P'), 0)
        self.assertEqual(self.g_c.grau_entrada('P'), 3)

        # Com laço.
        self.assertEqual(self.g_l1.grau_saida('A'), 2)
        self.assertEqual(self.g_l1.grau_entrada('A'), 3)
        self.assertEqual(self.g_l2.grau_entrada('B'), 2)
        self.assertEqual(self.g_l2.grau_saida('B'), 2)
        self.assertEqual(self.g_l4.grau_entrada('D'), 1)
        self.assertEqual(self.g_l4.grau_saida('D'), 1)

    def test_ha_paralelas(self):
        self.assertTrue(self.g_p.ha_paralelas())
        self.assertFalse(self.g_p_sem_paralelas.ha_paralelas())
        self.assertFalse(self.g_c.ha_paralelas())
        self.assertFalse(self.g_c2.ha_paralelas())
        self.assertFalse(self.g_c3.ha_paralelas())
        self.assertTrue(self.g_l1.ha_paralelas())
        self.assertTrue(self.g_e.ha_paralelas())

    def test_arestas_sobre_vertice(self):
        self.assertEqual(set(self.g_p.arestas_sobre_vertice('J')), {'a1'})
        self.assertEqual(set(self.g_p.arestas_sobre_vertice('C')), {'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7'})
        self.assertEqual(set(self.g_p.arestas_sobre_vertice('M')), {'a7', 'a8'})
        self.assertEqual(set(self.g_l2.arestas_sobre_vertice('B')), {'a1', 'a2', 'a3'})
        self.assertEqual(set(self.g_d.arestas_sobre_vertice('C')), set())
        self.assertEqual(set(self.g_d.arestas_sobre_vertice('A')), {'asd'})
        with self.assertRaises(VerticeInvalidoError):
            self.g_p.arestas_sobre_vertice('A')
        self.assertEqual(set(self.g_e.arestas_sobre_vertice('D')), {'5', '6', '7', '8'})

    def test_warshall(self):
        w = self.g_p.warshall()
        vertices = [v.rotulo for v in self.g_p.vertices]

        def idx(r): return vertices.index(r)

        # J alcança C diretamente
        self.assertTrue(w[idx('J')][idx('C')])
        # J alcança E via J->C->E
        self.assertTrue(w[idx('J')][idx('E')])
        # Z não alcança ninguém (grau de saída 0)
        self.assertFalse(w[idx('Z')][idx('J')])
        self.assertFalse(w[idx('Z')][idx('C')])
        self.assertFalse(w[idx('Z')][idx('E')])
        # E não alcança ninguém (grau de saída 0)
        self.assertFalse(w[idx('E')][idx('J')])
        self.assertFalse(w[idx('E')][idx('C')])

        # Grafo desconexo: A alcança B, mas não C nem D
        w2 = self.g_d.warshall()
        vertices2 = [v.rotulo for v in self.g_d.vertices]

        def idx2(r): return vertices2.index(r)

        self.assertTrue(w2[idx2('A')][idx2('B')])
        self.assertFalse(w2[idx2('A')][idx2('C')])
        self.assertFalse(w2[idx2('A')][idx2('D')])
        self.assertFalse(w2[idx2('C')][idx2('A')])
        self.assertFalse(w2[idx2('D')][idx2('B')])

        # Grafo g_e: verifica alguns caminhos
        w3 = self.g_e.warshall()
        vertices3 = [v.rotulo for v in self.g_e.vertices]

        def idx3(r): return vertices3.index(r)

        self.assertTrue(w3[idx3('A')][idx3('B')])
        self.assertTrue(w3[idx3('A')][idx3('D')])
        self.assertTrue(w3[idx3('A')][idx3('E')])
        self.assertFalse(w3[idx3('B')][idx3('A')])
        self.assertFalse(w3[idx3('B')][idx3('C')])
        self.assertTrue(w3[idx3('E')][idx3('A')])
        self.assertTrue(w3[idx3('E')][idx3('D')])

    def test_menor_caminho(self):
        # Grafo g_e com pesos padrão 1
        # A->B direto, custo 1
        self.assertEqual(self.g_e.menor_caminho('A', 'B'), (1, ['A', 'B']))

        # A->D via A->C->D, custo 2
        self.assertEqual(self.g_e.menor_caminho('A', 'D'), (2, ['A', 'C', 'D']))

        # A->E via A->C->D->E, custo 3
        self.assertEqual(self.g_e.menor_caminho('A', 'E'), (3, ['A', 'C', 'D', 'E']))

        # E->B direto via aresta '11', custo 1
        self.assertEqual(self.g_e.menor_caminho('E', 'B'), (1, ['E', 'B']))

        # B não alcança ninguém
        self.assertEqual(self.g_e.menor_caminho('B', 'A'), "Não existe caminho de 'B' até 'A'.")

        # Grafo desconexo: A não alcança C
        self.assertEqual(self.g_d.menor_caminho('A', 'C'), "Não existe caminho de 'A' até 'C'.")

        # Mesmo vértice de origem e destino, custo 0
        self.assertEqual(self.g_e.menor_caminho('A', 'A'), (0, ['A']))

        # Vértice inválido deve lançar exceção
        with self.assertRaises(VerticeInvalidoError):
            self.g_e.menor_caminho('X', 'A')
        with self.assertRaises(VerticeInvalidoError):
            self.g_e.menor_caminho('A', 'X')

        # Grafo com peso negativo deve retornar aviso
        g_neg = MeuGrafo()
        g_neg.adiciona_vertice('A')
        g_neg.adiciona_vertice('B')
        g_neg.adiciona_aresta('a1', 'A', 'B', -1)  # peso negativo
        self.assertEqual(g_neg.menor_caminho('A', 'B'),
                         "Não é possível calcular o menor caminho: há pesos negativos no grafo.")