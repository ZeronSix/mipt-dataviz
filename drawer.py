from PIL import Image, ImageDraw
import random


class Drawer:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    @staticmethod
    def random_color() -> str:
        radices = [random.randint(0, 255) for _ in range(3)]
        color = f'#{radices[0]:02x}{radices[1]:02x}{radices[2]:02x}'
        return color

    def draw(self, placements: list) -> Image:
        image = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(image)

        for rectangle, position in placements:
            draw.rectangle(rectangle.pil_shape(), fill=self.random_color())
            draw.ellipse((position.x - 1, position.y - 1, position.x + 1, position.y + 1), fill=self.random_color())

        return image
