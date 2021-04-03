from binary_tree import *
from PIL import Image, ImageDraw
from copy import copy


class SubtreeCanvas:
    def __init__(self):
        self.root_node = None
        self.width = 0
        self.height = 0
        self.left_child_canvas = None
        self.right_child_canvas = None
        self.left_child_canvas_offset = (0, 0)
        self.right_child_canvas_offset = (0, 0)
        self.subtree_size = 0

    def aspect_ratio(self) -> float:
        if self.width + self.height == 0:
            return 1
        else:
            return self.width / self.height

    def horizontal_join(self):
        self.width = 1 + self.left_child_canvas.width + self.right_child_canvas.width
        self.height = max(1 + self.left_child_canvas.height, self.right_child_canvas.height)
        self.left_child_canvas_offset = (0, 1)
        self.right_child_canvas_offset = (self.left_child_canvas.width + 1, 0)

    def vertical_join(self):
        self.width = max(1 + self.right_child_canvas.width, self.left_child_canvas.width)
        self.height = self.left_child_canvas.height + 1 + self.right_child_canvas.height
        self.left_child_canvas_offset = (0, self.right_child_canvas.height + 1)
        self.right_child_canvas_offset = (1, 0)

    @staticmethod
    def build(node: BinaryTreeNode):
        canvas = SubtreeCanvas()

        if node is None:
            return canvas

        canvas.root_node = node
        canvas.left_child_canvas = SubtreeCanvas.build(node.left_child())
        canvas.right_child_canvas = SubtreeCanvas.build(node.right_child())

        hor_joined_canvas = copy(canvas)
        hor_joined_canvas.horizontal_join()
        vert_joined_canvas = copy(canvas)
        vert_joined_canvas.vertical_join()

        return SubtreeCanvas.choose_canvas(hor_joined_canvas, vert_joined_canvas)

    @staticmethod
    def choose_canvas(first, second):
        """
        Returns the canvas with the aspect ratio closest to 1.
        """
        return min((first, second), key=lambda canvas: abs(1.0 - canvas.aspect_ratio()))


class HvBinaryTreeDrawer:
    def __init__(self, tree: BinaryTree, grid_size: int = 20):
        self.tree = tree
        self.root_canvas = SubtreeCanvas.build(tree.root)
        self.grid_size = grid_size
        self.border_size = 10

    def draw(self, rotate: bool = True) -> Image:
        image = Image.new('RGB', self.image_size())
        draw = ImageDraw.Draw(image)

        self.draw_canvas(self.root_canvas, draw, (0, 0))
        if rotate:
            image = image.rotate(-45, expand=True, resample=Image.BILINEAR)

        return image

    def image_size(self) -> tuple:
        return self.root_canvas.width * self.grid_size + 2 * self.border_size, \
               self.root_canvas.height * self.grid_size + 2 * self.border_size

    def draw_canvas(self, canvas: SubtreeCanvas, draw: ImageDraw, origin_hv: tuple):
        if canvas.root_node is None:
            return

        self.draw_node(draw, origin_hv)
        if canvas.left_child_canvas.root_node is not None:
            left_origin_hv = (
                origin_hv[0] + canvas.left_child_canvas_offset[0], origin_hv[1] + canvas.left_child_canvas_offset[1])
            self.draw_canvas(canvas.left_child_canvas, draw, left_origin_hv)
            self.draw_edge(draw, origin_hv, left_origin_hv)
        if canvas.right_child_canvas.root_node is not None:
            right_origin_hv = (
                origin_hv[0] + canvas.right_child_canvas_offset[0], origin_hv[1] + canvas.right_child_canvas_offset[1])
            self.draw_canvas(canvas.right_child_canvas, draw, right_origin_hv)
            self.draw_edge(draw, origin_hv, right_origin_hv)

    def draw_node(self, draw: ImageDraw, hv: tuple):
        node_radius = 5
        center_xy = self.hv_to_xy(hv)
        bbox = [(center_xy[0] - node_radius, center_xy[1] - node_radius),
                (center_xy[0] + node_radius, center_xy[1] + node_radius)]
        draw.ellipse(bbox, 'red')

    def draw_edge(self, draw: ImageDraw, from_hv: tuple, to_hv: tuple):
        draw.line([self.hv_to_xy(from_hv), self.hv_to_xy(to_hv)])

    def hv_to_xy(self, hv: tuple):
        return hv[0] * self.grid_size + self.border_size, hv[1] * self.grid_size + self.border_size
