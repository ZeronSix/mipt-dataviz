#!/usr/bin/env python3
from pygraphml import GraphMLParser
from binary_tree import *
from hv_tree_drawing import HvBinaryTreeDrawer
from argparse import ArgumentParser


def draw_tree(input_filename: str, output_filename: str, root_node: str):
    parser = GraphMLParser()
    graph = parser.parse(input_filename)
    tree = BinaryTree(graph, root_node)

    drawer = HvBinaryTreeDrawer(tree)
    image = drawer.draw(True)
    image.save(output_filename, 'PNG')


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument('-i', '--input', type=str, required=True, help='Input binary tree in GraphML format')
    arg_parser.add_argument('-o', '--output', type=str, required=True, help='Output PNG image filename')
    arg_parser.add_argument('-r', '--root-node', type=str, default='n0', help='Tree root node ID (n0 by default)')

    args = arg_parser.parse_args()
    draw_tree(args.input, args.output, args.root_node)


if __name__ == '__main__':
    main()
