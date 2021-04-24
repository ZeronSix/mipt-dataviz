# Расположение меток/подписей (Label placement)
Задача решена в постановке без ограничений на число вариантов расположения каждой метки. В качестве солвера используется `python-sat`.

Если указанное расположение недостижимо, программа уведомляет пользователя, выдавая ошибку.

## Запуск примеров
Replit: кнопка `Run`

```console
./main.py -i examples/1.txt -o examples/1.png --width=80 --height=80
./main.py -i examples/2.txt -o examples/2.png --width=80 --height=80
./main.py -i examples/3.txt -o examples/3.png --width=80 --height=80
./main.py -i examples/4.txt -o examples/4.png --width=80 --height=80
```

или

```
$ ./run_examples.sh
```

## Параметры запуска

```console
$ ./main.py --help
```
Через параметры `width` и `height` можно задавать требуемые размеры холста.