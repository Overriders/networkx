#!/usr/bin/env python
from nose.tools import *
import networkx as nx
import math


class TestCommunity:

    def test_louvain_undirected(self):
        G = nx.Graph()
        G.add_edges_from([(0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (1, 4),
                          (1, 7), (2, 4), (2, 5), (2, 6), (3, 7), (4, 10),
                          (5, 7), (5, 11), (6, 7), (6, 11), (8, 9), (8, 10),
                          (8, 11), (8, 14), (8, 15), (9, 12), (9, 14), (10, 11),
                          (10, 12), (10, 13), (10, 14), (11, 13)])
        tree = nx.louvain(G)
        assert_equal(len(tree), 23)
        assert_true(tree.is_directed())
        assert_equals(list(tree.neighbors('comm4-1')), [0, 1, 2, 4, 5])
        assert_equals(list(tree.neighbors('comm12-1')), [8, 9, 10, 12, 14, 15])
        assert_equals(list(tree.neighbors('comm13-1')), [11, 13])
        assert_equals(list(tree.neighbors('comm7-1')), [3, 6, 7])
        assert_equals(list(tree.neighbors('comm1-2')), ['comm12-1', 'comm13-1'])
        assert_equals(list(tree.neighbors('comm3-2')), ['comm4-1', 'comm7-1'])
        assert_equals(list(tree.neighbors('comm1-3')), ['comm3-2', 'comm1-2'])

    def test_louvain_ring_of_cliques(self):
        num_cliques = 8
        clique_size = 4
        G = nx.ring_of_cliques(num_cliques, clique_size)
        tree = nx.louvain(G)
        total = num_cliques * clique_size
        for i in range(0, int(math.ceil(math.log(num_cliques, 2))) + 1):
            total += int(num_cliques / 2 ** i)
        assert_equal(len(tree), total)
        assert_true(tree.is_directed())

    @raises(nx.NetworkXError)
    def test_louvain_directed(self):
        G = nx.DiGraph()
        G.add_weighted_edges_from([('0', '3', 3), ('0', '1', -5),
                                   ('1', '0', -2), ('0', '2', 2),
                                   ('1', '2', -3), ('2', '3', 1)])
        assert_raises(nx.NetworkXError, nx.louvain(G))

    @raises(nx.NetworkXError)
    def test_louvain_no_edges(self):
        G = nx.Graph()
        G.add_nodes_from([1, 2, 3, 4])
        assert_raises(nx.NetworkXError, nx.louvain(G))

