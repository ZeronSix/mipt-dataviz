from graph import *
from queue import PriorityQueue
from collections import defaultdict
from scipy.optimize import linprog
import numpy as np


def find_nodes_without_incoming_edges(graph: DirectedGraph) -> list:
    return list(filter(lambda node: len(node.prev) == 0, graph.nodes.values()))


def find_nodes_without_outcoming_edges(graph: DirectedGraph) -> list:
    return list(filter(lambda node: len(node.next) == 0, graph.nodes.values()))


class HeapLabelListContainer:
    def __init__(self, label_list: list, node: Node):
        self.label_list = sorted(label_list, reverse=True)
        self.node = node

    def __lt__(self, other):
        return self.label_list < other.label_list


def coffman_graham_topological_sort(graph: DirectedGraph) -> dict:
    prev_labels = defaultdict(list)
    labels = dict()
    queue = PriorityQueue()

    for node in find_nodes_without_incoming_edges(graph):
        queue.put(HeapLabelListContainer([], node))

    for label in range(len(graph.nodes)):
        top = queue.get()
        labels[top.node.id] = label

        for next_node in graph.nodes[top.node.id].next:
            prev_labels[next_node.id].append(label)
            if len(prev_labels[next_node.id]) == len(next_node.prev):
                queue.put(HeapLabelListContainer(prev_labels[next_node.id], next_node))

    return labels


def coffman_graham_layering(graph: DirectedGraph, max_width: int) -> list:
    labels = coffman_graham_topological_sort(graph)
    # print(labels)
    layering = [[]]
    layering_labels_set = [set()]
    current_layer = 0
    next_placed_labels = defaultdict(list)

    queue = PriorityQueue()
    for node in find_nodes_without_outcoming_edges(graph):
        queue.put((-labels[node.id], node))

    while queue.qsize() != 0:
        max_label, node = queue.get()
        max_label = -max_label

        for prev_node in graph.nodes[node.id].prev:
            next_placed_labels[prev_node.id].append(max_label)
            if len(next_placed_labels[prev_node.id]) == len(prev_node.next):
                queue.put((-labels[prev_node.id], prev_node))

        is_next_on_current_layer = len(
            layering_labels_set[current_layer].intersection(next_placed_labels[node.id])) != 0
        if len(layering[current_layer]) == max_width or is_next_on_current_layer:
            current_layer += 1
            layering.append([])
            layering_labels_set.append(set())

        layering[current_layer].append(node)
        layering_labels_set[current_layer].add(max_label)

    return layering


def map_node_to_layer(layering: list) -> dict:
    node_to_layer = dict()
    for current_layer in range(len(layering)):
        for node in layering[current_layer]:
            node_to_layer[node.id] = current_layer

    return node_to_layer


def insert_dummy_vertices(layering: list, graph: DirectedGraph):
    node_to_layer = map_node_to_layer(layering)

    for layer_index in range(len(layering)):
        layer = layering[layer_index]

        for node in layer:
            for prev_node in node.prev.copy():
                if node_to_layer[prev_node.id] != layer_index + 1:
                    dummy = graph.insert_dummy_vertex(prev_node, node)
                    node_to_layer[dummy.id] = layer_index + 1

                    layering[layer_index + 1].append(dummy)


def map_node_id_to_int(graph: DirectedGraph):
    node_map = dict()
    index_map = dict()

    index = 0
    for node_id in graph.nodes.keys():
        node_map[node_id] = index
        index_map[index] = node_id
        index += 1

    return node_map, index_map


def min_dummy_layering(graph: DirectedGraph) -> list:
    node_id_to_int, int_to_node_id = map_node_id_to_int(graph)

    obj_func_coeffs = np.zeros(len(graph.nodes))
    inequeality_coeffs = np.zeros((len(graph.edges), len(graph.nodes)))
    inequeality_b = np.zeros(len(graph.edges))

    edge_index = 0
    for edge in graph.edges:
        first_index = node_id_to_int[edge.node1.id]
        second_index = node_id_to_int[edge.node2.id]

        obj_func_coeffs[first_index] += 1
        obj_func_coeffs[second_index] -= 1
        inequeality_coeffs[edge_index][first_index] = -1
        inequeality_coeffs[edge_index][second_index] = 1
        inequeality_b[edge_index] = -1
        edge_index += 1

    # Use simplex method to produce integer solutions
    result = linprog(obj_func_coeffs, inequeality_coeffs, inequeality_b, method='revised simplex')
    num_layers = int(np.max(result.x) + 1)

    layering = []
    for _ in range(num_layers):
        layering.append([])

    for node_index in range(len(graph.nodes)):
        node_id = int_to_node_id[node_index]
        layer = int(result.x[node_index])
        layering[layer].append(graph.nodes[node_id])

    return layering
