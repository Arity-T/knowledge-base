# Minecraft Server

[docker-minecraft-server](https://github.com/itzg/docker-minecraft-server) - самый простой и удобный способ запуска своего Minecraft сервера. У проекта есть хорошая [документация](https://docker-minecraft-server.readthedocs.io/en/latest/), но всё же есть некоторые нюансы, которые стоит записать.

## Запуск сервера

1. Устанавливаем [`docker`](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository). Не забываем про [post-install steps](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user).
2. Создаём папку для сервера.
    ```sh
    mkdir minecraft-server
    cd minecraft-server
    ```
3. Создаём файл `docker-compose.yml`.
   
    === "Терминал"
    
        ```sh
        nano docker-compose.yml
        ```

    === "docker-compose.yml"
    
        ```yaml
        # https://docker-minecraft-server.readthedocs.io/en/latest/
        services:
          mc:
            image: itzg/minecraft-server
            tty: true
            stdin_open: true
            ports:
              # Порт 25565 является стандартным, все клиенты по умолчанию 
              # подключаются к нему, если порт не задан явно
              - "25565:25565"
            environment:
              # Полный список переменных можно найти в документации
              # https://docker-minecraft-server.readthedocs.io/en/latest/variables/

              EULA: "TRUE"

              # Не забудьте указать нужную версию Minecraft
              VERSION: 1.19.4

              # Разрешаем подключаться без лицензии Minecraft
              ONLINE_MODE: false

              # Указываем название игрового мира (будет храниться в ./data/<LEVEL>)
              # Чтобы изменить мир, достаточно изменить значение этой переменной
              # и перезапустить контейнер
              LEVEL: MyWorld

              # Описание сервера
              MOTD: |
                Tish's Minecraft Server on %VERSION%

              # Иконка сервера
              # Надо разместить файл icon.png в ./data/
              # ICON: /data/icon.png
              # OVERRIDE_ICON: true

              # Автоотключение пустого сервера
              # ENABLE_AUTOSTOP: TRUE
              # AUTOSTOP_TIMEOUT_EST: 300
              # AUTOSTOP_TIMEOUT_INIT: 600

            volumes:
              - ./data:/data
        ```

4. Запускаем сервер.

    ```sh
    docker compose up -d
    ```

## Остановка сервера

```sh
docker compose stop
```

## Консоль сервера

`ctrl + p ctrl + q` - отключиться от консоли.
Если просто нажать `ctrl + c`, то сервер остановится.

```sh
docker compose attach mc
```

## Домен для сервера

Если порт стандартный (`25565`), то при подключении можно просто указать домен в A-записи которого указан IP-адрес сервера. Однако если порт нестандартный или хочется сделать несколько доменных имён для одного сервера, то можно использовать SRV-записи.

Например, если я создам домен `minecraft.tishenko.dev` и запущу сервер на порте `12345`, то чтобы подключаться к серверу без указания порта, мне нужно будет добавить следующую SRV-запись для `minecraft.tishenko.dev`:

```dns
_minecraft._tcp.minecraft.tishenko.dev.	3600	IN	SRV	0	5	12345	minecraft.tishenko.dev.
```

Обычно ДНС провайдеры предоставляют UI для создания записей, в нём скорее всего будут следующие поля:

- Поддомен: `minecraft`
- Сервис: `minecraft` (SpaceWeb, например, сам подставляет `_`)
- Протокол: `tcp`
- TTL: `3600`
- Приоритет: `0`
- Вес: `5`
- Порт: `12345`
- Целевой домен: `minecraft.tishenko.dev.` (точка в конце обязательна)

Целевой домен не обязательно должен совпадать с поддоменом. Можно сделать подключение к серверу по домену `tishenko.dev` указан следующую SRV-запись для домена `tishenko.dev`:

```dns
_minecraft._tcp.tishenko.dev.	3600	IN	SRV	0	5	12345	minecraft.tishenko.dev.
```

Домен `minecraft.tishenko.dev` в своей A-записи должен указывать на IP-адрес сервера, но при этом совершенно неважно какая A-запись будет у `tishenko.dev`.

DNS-записи распространяются не мгновенно, но обычно это занимает 15-30 минут. Отслеживать распространение записей можно с помощью сайта [DNS Checker](https://dnschecker.org/#SRV/_minecraft._tcp.tishenko.dev).

!!! note "Клиенты Minecraft читают SRV-запись"

    С помощью SRV-записи можно подменять как порт, так и домен сервера. Стандартный клиент Minecraft Java Edition при подключении по домену автоматически ищет SRV-запись _minecraft._tcp.<домен> в DNS. Если такая запись есть, клиент использует указанные в ней порт и хост. С Bedrock Edition могут возникнуть сложности, там не все клиенты читают SRV-запись.


## Автоматическое создание бэкапов

Скрипт ниже автоматически создаёт бэкапы при завершении работы сервера. Особенно удобно сочетать его с настройкой `ENABLE_AUTOSTOP`, тогда при завершении игровой сессии бэкап будет создан автоматически.

=== "Терминал"
    ```sh
    # Создаём скрипт в директории рядом с docker-compose.yml
    nano run-and-backup.sh

    # После создания скрипта надо дать ему права на выполнение
    chmod u+x run-and-backup.sh
    ```

=== "run-and-backup.sh"

    ```bash
    #!/usr/bin/env bash
    set -euo pipefail

    # === настройки ===
    PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    DATA_DIR="${PROJECT_DIR}/data"
    BACKUP_DIR="${PROJECT_DIR}/backups"
    KEEP_BACKUPS=3
    TAR_COMPRESS_FLAGS="-czf"

    mkdir -p "$BACKUP_DIR"

    ts() { date +"%Y-%m-%d_%H-%M-%S"; }

    show_help() {
      cat <<'EOF'
    run-and-backup.sh — запускает Minecraft-сервер через Docker Compose
    и создаёт резервную копию каталога ./data после завершения работы.

    ИСПОЛЬЗОВАНИЕ:
      ./run-and-backup.sh        — запустить сервер в foreground
      ./run-and-backup.sh -d     — запустить в background (логи в run-and-backup.log)
      ./run-and-backup.sh -b     — только сделать бэкап и выйти
      ./run-and-backup.sh -h     — показать эту справку

    ЧТО ДЕЛАЕТ:
      1) docker compose up (следит за завершением контейнера)
      2) по Ctrl+C или штатному выходу — docker compose down
      3) создаёт архив ./backups/mc-data-YYYY-MM-DD_HH-MM-SS.tar.gz
      4) хранит последние KEEP_BACKUPS бэкапов

    КАК ВОССТАНОВИТЬ СЕРВЕР ИЗ БЭКАПА:
      1) Остановите сервер:
           docker compose down
      2) Очистите или перенесите текущие данные:
           mv ./data ./data.old
           mkdir ./data
           ИЛИ
           rm -rf ./data/*
      3) Распакуйте нужный архив в ./data:
           tar -xzf ./backups/mc-data-YYYY-MM-DD_HH-MM-SS.tar.gz -C ./data
      4) Запустите сервер

    ПРИМЕЧАНИЯ:
      • Архив содержит всё из ./data (мир, плагины, конфиги, whitelist, ops и т.д.)
      • Для фонового режима логи скрипта пишутся в ./run-and-backup.log
    EOF
    }

    backup() {
            local stamp archive
            stamp="$(ts)"
            archive="${BACKUP_DIR}/mc-data-${stamp}.tar.gz"

            if [[ ! -d "$DATA_DIR" ]]; then
            echo "[!] Нет каталога DATA_DIR: $DATA_DIR" >&2
            exit 1
            fi

            echo "[*] Бэкап ${DATA_DIR} -> ${archive}"
            tar $TAR_COMPRESS_FLAGS "$archive" -C "$DATA_DIR" .
            echo "[+] Готово: $archive"

            echo "[*] Ротация: оставляю последние ${KEEP_BACKUPS}"
            ls -1t "${BACKUP_DIR}"/mc-data-*.tar.* 2>/dev/null | tail -n +$((KEEP_BACKUPS+1)) | xargs -r rm -f
    }

    graceful_down_and_backup() {
            echo "[*] Останавливаю docker compose (graceful)..."
            docker compose down || true
            backup
    }

    # ---- разбор флагов ----
    bg=false
    do_backup_only=false

    while getopts ":dbh" opt; do
            case "$opt" in
                    d) bg=true ;;
                    b) do_backup_only=true ;;
                    h) show_help; exit 0 ;;
                    \?) echo "Неизвестный флаг: -$OPTARG" >&2; show_help; exit 2 ;;
            esac
    done

    # -b имеет приоритет: просто делаем бэкап и выходим
    if $do_backup_only; then
            backup
            exit 0
    fi

    # запуск в фоне
    if $bg; then
            echo "[*] Запускаю в background (логи: ${PROJECT_DIR}/run-and-backup.log)"
            nohup "$0" >"${PROJECT_DIR}/run-and-backup.log" 2>&1 &
            echo "[✓] PID: $!"
            exit 0
    fi

    # ---- основной режим ----
    trap graceful_down_and_backup INT TERM

    echo "[*] Запускаю docker compose в foreground (Ctrl+C для остановки)..."
    if docker compose up; then
            echo "[*] docker compose завершился сам — делаю бэкап..."
            backup
    else
            echo "[!] docker compose завершился с ошибкой; если это был Ctrl+C, бэкап уже выполнен ловушкой."
    fi

    echo "[✓] Готово."
    ```

Теперь можно запускать сервер командой `./run-and-backup.sh`.

```sh
./run-and-backup.sh -d
```

Вывести справку можно командой.

```sh
./run-and-backup.sh -h
```