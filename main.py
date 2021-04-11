#!/usr/bin/env python3
from pygraphml import GraphMLParser
from layering import *
from placing import *
from drawing import GraphDrawer
from argparse import ArgumentParser
from pprint import pprint


def _main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument('-i', '--input', type=str, required=True, help='Input DAG in GraphML format')
    arg_parser.add_argument('-o', '--output', type=str, required=True, help='Output PNG image filename')
    arg_parser.add_argument('--max-width', type=int, default=None,
                            help='Max layer width. If set, Coffman-Graham layering is used, min-dummy otherwise')
    arg_parser.add_argument('--opt-steps', type=int, default=2,
                            help='Number of steps for optimization of intersections in the placement')
    arg_parser.add_argument('--print-layering', action='store_true', help='Print text representation of the layering')

    args = arg_parser.parse_args()

    parser = GraphMLParser()
    graph = DirectedGraph(parser.parse(args.input))

    layering = coffman_graham_layering(graph, args.max_width) if args.max_width is not None else min_dummy_layering(
        graph)
    insert_dummy_vertices(layering, graph)
    for _ in range(args.opt_steps):
        optimize_intersections(layering)
        optimize_intersections(layering, reversed_order=True)
    placement = place_nodes(layering)

    if args.print_layering:
        pprint(layering)

    drawer = GraphDrawer()
    image = drawer.draw(graph, placement)
    image.save(args.output)


if __name__ == '__main__':
    _main()
