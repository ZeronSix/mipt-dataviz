#!/usr/bin/env bash

./main.py -i examples/1.graphml -o examples/1_coffman.png --max-width=3
./main.py -i examples/1.graphml -o examples/1_min_dummy.png
./main.py -i examples/2.graphml -o examples/2_coffman.png --max-width=3
./main.py -i examples/2.graphml -o examples/2_min_dummy.png
