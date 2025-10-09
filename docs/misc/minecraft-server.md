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
