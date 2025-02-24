# Разное

## Поиск по истории команд в bash

Включаем поиск по истории команд `bash` по префиксу.

=== "Терминал"

    ```sh
    nano ~/.inputrc
    ```

=== ".inputrc"

    ```sh
    "\e[A": history-search-backward
    "\e[B": history-search-forward
    ```

После обновления `.inputrc` нужно либо начать сеанс заново, либо выполнить команду.

```sh
bind -f ~/.inputrc
```