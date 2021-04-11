# Укладка ациклических неориентированных графов (DAG)

Реализованы два алгоритма укладки:

- Алгоритм Коффмана-Грэхэма (используется, если явно указать значение максимальную ширину слоя параметром `max-width`
  при запуске скрипта)
- Алгоритм минимизации числа dummy-вершин (используется в противном случае)

## Запуск примеров

```console
$ ./main.py -i examples/1.graphml -o examples/1_coffman.png --max-width=3
$ ./main.py -i examples/1.graphml -o examples/1_min_dummy.png
$ ./main.py -i examples/2.graphml -o examples/2_coffman.png --max-width=3
$ ./main.py -i examples/2.graphml -o examples/2_min_dummy.png
```

или

```
$ ./run_examples.sh
```

## Параметры запуска

```console
$ ./main.py --help
```