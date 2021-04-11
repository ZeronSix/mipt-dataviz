import pygraphml


class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.prev = []
        self.next = []

    def __repr__(self):
        repr_str = f'Node(id={self.id}'
        if self.is_dummy():
            repr_str += f' prev={self.prev[0].id} next={self.next[0].id}'
        repr_str += ')'
        return repr_str

    def is_dummy(self) -> bool:
        return str(self.id).startswith('dummy')


class DirectedGraph:
    def __init__(self, source: pygraphml.Graph):
        self.nodes = dict()

        for node in source.nodes():
            self.nodes[node.id] = Node(node.id)

        self.edges = source.edges()
        for edge in self.edges:
            self.nodes[edge.node1.id].next.append(self.nodes[edge.node2.id])
            self.nodes[edge.node2.id].prev.append(self.nodes[edge.node1.id])

        self.num_dummy_vertices = 0

    def create_dummy_vertex(self):
        dummy_id = f'dummy{self.num_dummy_vertices}'
        dummy = Node(dummy_id)
        self.num_dummy_vertices += 1
        self.nodes[dummy_id] = dummy

        return dummy

    def insert_dummy_vertex(self, from_node: Node, to_node: Node):
        dummy = self.create_dummy_vertex()

        from_node.next.remove(to_node)
        from_node.next.append(dummy)
        to_node.prev.remove(from_node)
        to_node.prev.append(dummy)
        dummy.prev.append(from_node)
        dummy.next.append(to_node)

        return dummy
