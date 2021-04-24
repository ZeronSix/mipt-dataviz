class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @staticmethod
    def parse(string: str):
        x, y = map(int, string.split(','))
        return Point(x, y)

    def __repr__(self):
        return f'({self.x}, {self.y})'


class Rect:
    def __init__(self, left: int, top: int, right: int, bottom: int):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def intersects(self, other) -> bool:
        return self.left <= other.right and self.right >= other.left \
               and self.top <= other.bottom and self.bottom >= other.top

    def __repr__(self):
        return f'Rectangle[{self.left}, {self.top}, {self.right}, {self.bottom}]'

    def pil_shape(self) -> list:
        return [self.left, self.top, self.right, self.bottom]

    def is_inside_canvas(self, width, height):
        return 0 <= self.left <= self.right < width and 0 <= self.top <= self.bottom < height


class Label:
    def __init__(self, pos: Point, size: Point, placement_offsets: list):
        self.pos = pos
        self.size = size
        self.placement_offsets = placement_offsets

    def generate_rect(self, offset: Point) -> Rect:
        left = self.pos.x - offset.x
        top = self.pos.y - offset.y
        right = left + self.size.x
        bottom = top + self.size.y

        return Rect(left, top, right, bottom)

    @staticmethod
    def parse(string: str):
        splits = string.split('\t')

        pos = Point.parse(splits[0])
        size = Point.parse(splits[1])
        offsets = [Point.parse(coordinates) for coordinates in splits[2].split(' ')]

        return Label(pos, size, offsets)

    def filter_offsets(self, width: int, height: int):
        self.placement_offsets = list(
            filter(lambda offset: self.generate_rect(offset).is_inside_canvas(width, height), self.placement_offsets))


def parse_labels(lines: list) -> list:
    labels = []
    for line in lines:
        labels.append(Label.parse(line))

    return labels
