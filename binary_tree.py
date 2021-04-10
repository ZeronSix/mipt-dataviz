from pygraphml import Graph


class BinaryTreeNode:
    def __init__(self):
        self.parent = None
        self.children = []

    def left_child(self):
        return self.children[0] if len(self.children) >= 1 else None

    def right_child(self):
        return self.children[1] if len(self.children) == 2 else None

    def has_one_child(self) -> bool:
        return len(self.children) == 1

    def has_two_children(self) -> bool:
        return len(self.children) == 2


class BinaryTree:
    def __init__(self, source_graph: Graph, root_id: str):
        self.nodes = dict()

        for node in source_graph.nodes():
            self.nodes[node.id] = BinaryTreeNode()

        for edge in source_graph.edges():
            parent_node = self.nodes[edge.node1.id]
            child_node = self.nodes[edge.node2.id]

            parent_node.children.append(child_node)
            assert len(parent_node.children) <= 2, 'The tree is not binary'

            assert child_node.parent is None, 'The graph is not a tree'
            child_node.parent = parent_node

        self.root = self.nodes[root_id]
