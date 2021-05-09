#!/usr/bin/env python3
from argparse import ArgumentParser
import numpy as np
from preprocessing import reduce_dimensions_pca
from t_sne import t_sne
from visualization import visualize_clusters


def _main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument('--objects', type=str, required=True, help='Input dataset objects filename')
    arg_parser.add_argument('--labels', type=str, required=True, help='Input dataset labels filename')
    arg_parser.add_argument('--perplexity', type=float, default=30, help='Perplexity')
    arg_parser.add_argument('--temporary-pca-dimensions', type=int, default=50)
    arg_parser.add_argument('--output-image', type=str, required=True)

    args = arg_parser.parse_args()
    objects = np.loadtxt(args.objects)
    labels = np.loadtxt(args.labels)

    reduced_objects = np.real(reduce_dimensions_pca(objects, args.temporary_pca_dimensions))
    mapped_2d_objects = t_sne(reduced_objects, perplexity=args.perplexity)
    visualize_clusters(mapped_2d_objects, labels, args.output_image)


if __name__ == '__main__':
    _main()
