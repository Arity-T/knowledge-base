# Разное

## Поиск по истории команд в bash

Включаем поиск по истории команд `bash` по префиксу.

=== "Терминал"

    ```sh
    nano ~/.inputrc
    bind -f ~/.inputrc
    ```

=== ".inputrc"

    ```sh
    "\e[A": history-search-backward
    "\e[B": history-search-forward
    ```