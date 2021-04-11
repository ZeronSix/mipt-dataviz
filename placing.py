from graph import *
from itertools import product, permutations


def map_node_to_x(layer: list):
    node_map = dict()
    for x in range(len(layer)):
        node = layer[x]
        node_map[node.id] = x

    return node_map


def intervals_intersect(first: tuple, second: tuple):
    return first[0] < second[1] and second[0] < first[1]


def make_interval(interval: tuple):
    return interval if interval[0] < interval[1] else (interval[1], interval[0])


def count_intersections(first_layer: list, second_layer: list):
    first_node_map = map_node_to_x(first_layer)
    second_node_map = map_node_to_x(second_layer)

    segments = []
    for second_node in second_layer:
        x2 = second_node_map[second_node.id]
        for first_node in second_node.next:
            x1 = first_node_map[first_node.id]
            segments.append(make_interval((x1, x2)))

    intersections = 0

    for segment1, segment2 in product(segments, segments):
        if segment1 is segment2:
            continue

        if intervals_intersect(segment1, segment2):
            intersections += 1

    return intersections


def optimize_intersections(layering: list, reversed_order: bool = False):
    layer_indices = [y for y in range(len(layering))]
    if reversed_order:
        layer_indices.reverse()

    for layer_index in layer_indices:
        min_intersections = float('inf')
        best_layer = None
        for permuted_layer in permutations(layering[layer_index]):
            intersections = 0
            if layer_index != 0:
                intersections += count_intersections(layering[layer_index - 1], permuted_layer)
            if layer_index != len(layering) - 1:
                intersections += count_intersections(permuted_layer, layering[layer_index + 1])
            if intersections < min_intersections:
                min_intersections = intersections
                best_layer = permuted_layer

        layering[layer_index] = best_layer


def place_nodes(layering: list) -> dict:
    placement = dict()
    y = len(layering) - 1

    for layer in layering:
        x = 0
        for node in layer:
            placement[node.id] = (x, y)
            x += 1
        y -= 1

    return placement
