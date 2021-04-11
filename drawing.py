from graph import *
import cv2
import numpy as np
from PIL import Image


class GraphDrawer:
    def __init__(self):
        self.node_color = (200, 200, 200)
        self.font_color = (0, 0, 0)
        self.font_scale = 0.5
        self.node_radius = 15
        self.grid_size = (48, 48)

    @staticmethod
    def find_grid_dimensions(placement: dict) -> tuple:
        max_x = 0
        max_y = 0
        for coords in placement.values():
            x, y = coords
            max_x = max(x, max_x)
            max_y = max(y, max_y)

        return max_x, max_y

    def find_image_size(self, placement: dict) -> tuple:
        grid_dim = GraphDrawer.find_grid_dimensions(placement)
        return 64 + grid_dim[0] * self.grid_size[0], \
               40 + grid_dim[1] * self.grid_size[1]

    def draw(self, graph: DirectedGraph, placement: dict) -> Image:
        image = np.array(Image.new('RGB', self.find_image_size(placement), 'white'))

        for node_id, coords in placement.items():
            node = graph.nodes[node_id]
            node_xy = self.grid_to_xy(coords)
            for prev_node in node.prev:
                prev_xy = self.grid_to_xy(placement[prev_node.id])
                image = cv2.line(image, prev_xy, node_xy, (0, 0, 0), thickness=1, lineType=cv2.LINE_AA)

        for node_id, coords in placement.items():
            node = graph.nodes[node_id]
            if node.is_dummy():
                continue

            xy = self.grid_to_xy(coords)
            image = cv2.circle(image, xy, radius=self.node_radius, color=self.node_color,
                               thickness=-1)

            text_size, _ = cv2.getTextSize(node_id, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=self.font_scale,
                                           thickness=1)
            text_xy = xy[0] - text_size[0] // 2, xy[1] + text_size[1] // 2
            image = cv2.putText(image, node_id, text_xy, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=self.font_scale,
                                color=self.font_color,
                                thickness=1, lineType=cv2.LINE_AA)

        return Image.fromarray(image)

    def grid_to_xy(self, coords: tuple):
        x, y = coords
        return 32 + x * self.grid_size[0], 20 + y * self.grid_size[1]
