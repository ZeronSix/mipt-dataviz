#!/usr/bin/env python3
from argparse import ArgumentParser
from label import parse_labels
from placer import Placer
from drawer import Drawer


def _main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument('-i', '--input', type=str, required=True, help='Input filename')
    arg_parser.add_argument('-o', '--output', type=str, required=True, help='Output PNG filename')
    arg_parser.add_argument('--width', type=int, required=True, help='Image width')
    arg_parser.add_argument('--height', type=int, required=True, help='Image height')

    args = arg_parser.parse_args()
    with open(args.input, "r") as f:
        labels = parse_labels(f.readlines())

    try:
        for label in labels:
            label.filter_offsets(args.width, args.height)
            if len(label.placement_offsets) == 0:
                raise ValueError(f'Can\'t fit label {label.pos} inside {args.width}x{args.height} canvas!')

        placer = Placer(labels)
        drawer = Drawer(args.width, args.height)
        image = drawer.draw(placer.place())
        image.save(args.output, 'PNG')
    except Exception as ex:
        print(f'{args.input}: {ex}')


if __name__ == '__main__':
    _main()
