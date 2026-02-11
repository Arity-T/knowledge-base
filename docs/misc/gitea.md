# Gitea

Шпаргалки актуальны для Gitea 1.24.

## Установка с Docker

Эта заметка лишь дополнение к [документации](https://docs.gitea.com/installation/install-with-docker#basics).

=== "Терминал"

    ```sh
    # Создаём служебного пользователя
    sudo useradd --create-home --shell /bin/bash --system gitea

    # Даём пользователю права использовать Docker
    # Строго говоря это необязательно для разворачивания Gitea, 
    # но скорее всего и ранеры будут запускаться от этого пользователя,
    # так что ему в любом случае потребуются права на Docker
    sudo usermod -aG docker gitea

    # Переключаемся на пользователя gitea
    sudo su - gitea

    # Узнаём его uid и gid
    id

    # Создаём docker-compose.yml по примеру
    # Указываем переменные USER, USER_UID и USER_GID и порты
    nano docker-compose.yml

    # Создаём директорию для данных Gitea из-под пользователя gitea,
    # иначе Docker сам создаст её из-под root
    # см. секцию "volumes" в docker-compose.yml
    mkdir data

    # Запускаем Gitea
    docker compose up -d
    ```

=== "docker-compose.yml"

    ```yaml
    networks:
      gitea:
        external: false

    services:
      server:
        image: docker.gitea.com/gitea:1.24.6
        container_name: gitea
        environment:
          - USER=<user>
          - USER_UID=<uid>
          - USER_GID=<gid>
        restart: always
        networks:
          - gitea
        volumes:
          - ./data:/data
          - /etc/timezone:/etc/timezone:ro
          - /etc/localtime:/etc/localtime:ro
        ports:
          - "28500:3000"
          - "28522:22"
    ```

Теперь можно перейти по адресу `http://<IPv4>:28500` и завершить установку Gitea.

Подключиться к контейнеру можно командой.

```sh
docker exec --user gitea -it gitea bash

# Уже внутри контейнера можно запускать бинарник gitea
/usr/local/bin/gitea help
```

## Создание бэкапа

Ссылка на [документацию](https://docs.gitea.com/administration/backup-and-restore).

### Gitea установлена из бинарника

```sh
# gitea - это пользователь под которым запущен Gitea, часто это просто git
sudo su - gitea

mkdir gitea-backup
cd gitea-backup

# Нужно указать актуальный путь к конфигу
/usr/local/bin/gitea dump -c /etc/gitea/app.ini

# Если планируется восстановление с другой базой данных,
# то нужно указать параметр --database <sqlite3|mysql|postgres>
/usr/local/bin/gitea dump --database sqlite3 -c /etc/gitea/app.ini
```

### Gitea установлена с Docker

!!! info "Есть вариант проще"

    Если Gitea запускается через Docker Compose, как показано в инструкции [выше](#установка-с-docker) и в качестве базы данных используется SQLite, то для создания полного бэкапа достаточно сохранить папку `data`. Её же достаточно перенести на другую машину при переезде.

    ```sh
    # Предварительно нужно остановить Gitea
    sudo su - gitea
    docker compose stop
    exit

    mkdir gitea-backup
    cd gitea-backup

    # Запускать надо с root правами, потому что некоторые файлы
    # внутри волюма создаются из-под root
    sudo tar -czf gitea-backup.tar.gz -C /home/gitea data
    sudo chown $USER:$USER gitea-backup.tar.gz

    # Опционально: можно зашифровать бэкап хотя бы просто паролем
    gpg -c gitea-backup.tar.gz
    rm gitea-backup.tar.gz

    # Команда для расшифровки
    # gpg -d gitea-backup.tar.gz.gpg > gitea-backup.tar.gz

    # Перезапускаем Gitea
    sudo su - gitea
    docker compose up -d
    ```

Предполагается, что Gitea развёрнута с помощью Docker Compose как описано в инструкции [выше](#установка-с-docker).

Подключаемся к контейнеру.

```sh
docker exec --user gitea -it gitea bash
```

Внутри контейнера выполняем.

```sh
# Бэкап нужно создать в директории /data, потому что она прокинута на хост
cd /data

# (Опционально) Создаём директорию для бэкапов
mkdir backups
cd backups

# Нужно указать актуальный путь к конфигу
/usr/local/bin/gitea dump -c /data/gitea/conf/app.ini

# Если планируется восстановление с другой базой данных,
# то нужно указать параметр --database <sqlite3|mysql|postgres>
/usr/local/bin/gitea dump --database sqlite3 -c /data/gitea/conf/app.ini
```

То же самое в одну команду.

```sh
docker exec -u gitea -w /data gitea /usr/local/bin/gitea dump -c /data/gitea/conf/app.ini
```

### Перенос бэкапа на другую машину

Перенести бэкап на другую машину можно, например, так:

```sh
# Запускаем HTTP сервер (с scp загрузка больших файлов займёт много времени)
python3 -m http.server 8080

# На другой машине скачиваем бэкап
curl -O http://<IP>:8080/gitea-dump-1760203345.zip
```


## Восстановление из бэкапа в Docker

!!! info "Есть вариант проще"

    Если в качестве бэкапа Gitea была сохранена папка `data`. То для восстановления Gitea на другой машине достаточно просто пройти по инструкции [установки Gitea с Docker](#установка-с-docker), но перед запуском просто скопировать папку `data` по пути, указанном в `docker-compose.yml`.


Предполагается, что Gitea разворачивается из [бэкапа](#создание-бэкапа) с помощью Docker Compose как описано в инструкции [выше](#установка-с-docker). В [документации](https://docs.gitea.com/1.24/administration/backup-and-restore#using-docker-restore) есть соответствующая инструкция, однако она не полная и содержит ошибки.

```sh
# Если создавали пользователя по инструкции выше, 
# то команды выполняем от него
sudo su - gitea

# Распаковываем бэкап
unzip -q gitea-dump-*.zip -d dump

# Создаём директорию для данных Gitea
mkdir data

# Копируем данные
cp -r dump/data/ data/gitea/

# Копируем репозитории
mkdir data/git/
cp -r dump/repos/ data/git/repositories/

# Копируем SSH ключи, если есть
mkdir data/ssh
cp -r dump/ssh/ data/ssh/

# Копируем кастомные стили и шаблоны
# Актуально, если $GITEA_CUSTOM не совпадала с data/gitea
# cp -r dump/custom/. data/gitea/

# Если Gitea в Docker будет работать с SQLite, 
# то восстановить базу данных можно так.
# sqlite3 data/gitea/gitea.db < dump/gitea-db.sql
# Если файл data/gitea/gitea.db уже есть, то и восстанавливать ничего не нужно
# Команды для других баз данныех есть в документации

# Копируем конфиг, если изначально он был в другом месте
# mkdir data/gitea/conf
# cp dump/app.ini data/gitea/conf/app.ini
```

Если до этого Gitea была запущена не через Docker, то нужно отредактировать конфиг.

=== "Терминал"

    ```sh
    vim data/gitea/conf/app.ini
    ```

=== "`app.ini` для Docker"

    Это не полноценный конфиг, а лишь часть настроек для запуска Gitea Docker.
    Подразумевается, что конфиг был перенесён из бэкапа.

    `SSH_PORT` нужно указать тот же, что и в `docker-compose.yml`.

    ```ini
    RUN_USER = gitea
    WORK_PATH = /data/gitea

    [server]
    LOCAL_ROOT_URL   = http://localhost:3000
    APP_DATA_PATH    = /data/gitea
    DOMAIN           = localhost
    SSH_DOMAIN       = localhost
    HTTP_PORT        = 3000
    SSH_PORT         = 28522

    [repository]
    ROOT = /data/git/repositories

    [database]
    PATH    = /data/gitea/gitea.db
    DB_TYPE = sqlite3
    HOST    = localhost:3306
    NAME    = gitea
    USER    = root
    PASSWD  =
    LOG_SQL = false

    [lfs]
    PATH = /data/git/lfs

    [log]
    ROOT_PATH = /data/gitea/log
    ```

Запускаем Gitea, скорее всего она начнёт падать с ошибкой `permission denied`, а Docker будет пытаться её перезапустить. При первом запуске Gitea создаёт директории для ssh ключей, но по какой-то причине они создаются из-под `root`, а не из-под пользователя `gitea`.

```sh
# Специально без -d, ждём когда в логах повалятся ошибки и нажимаем Ctrl+C
docker compose up
```

Теперь нужно из-под `root` или с помощью `sudo` указать нужные права.

```sh
# Выходим из пользователя gitea (Ctrl + D или exit)
# и выполняем команду с root правами
sudo chown -R gitea:gitea ~gitea/data
```

Снова запускаем Gitea.

```sh
sudo su - gitea
docker compose up -d
```

Если всё работает корректно, то файлы бэкапа можно удалить.

```sh
rm -rf dump gitea-dump-*.zip
```


## Кастомизация Gitea

Во всех командах подразумевается, что Gitea [установлена из бинарника](https://docs.gitea.com/installation/install-from-binary) и [запускается как `systemd` сервис](https://docs.gitea.com/installation/linux-service).

В документации есть страница, посвящённая [кастомизации Gitea](https://docs.gitea.com/administration/customizing-gitea).


### Свой `css`

Добавляем ссылку на свой файл со стилями.

=== "Терминал"

    ```sh
    # Путь по умолчанию
    export GITEA_CUSTOM=/var/lib/gitea/custom
    
    sudo -u git mkdir -p $GITEA_CUSTOM/templates/custom
    sudo -u git nano $GITEA_CUSTOM/templates/custom/header.tmpl
    ```

=== "header.tmpl"

    ```html
    <link rel="stylesheet" href="/assets/css/custom.css">
    ```

Создаём файл со стилями.

=== "Терминал"

    ```sh
    sudo -u git mkdir -p $GITEA_CUSTOM/public/assets/css
    sudo -u git nano $GITEA_CUSTOM/public/assets/css/custom.css
    ```

=== "Пример custom.css"

    ```css
    /* Стили для git.tishenko.dev */
    * {
        transition: all 0.125s;
    }

    /* Список переменных и их значения по умолчанию
     *
     * Для светлой темы
     * https://github.com/go-gitea/gitea/blob/main/web_src/css/themes/theme-gitea-light.css
     *
     * Для тёмной темы
     * https://github.com/go-gitea/gitea/blob/main/web_src/css/themes/theme-gitea-dark.css
     */

    /* Переопределения переменных для светлой и тёмной темы одновременно */
    :root {
        /* Основной цвет */
        --color-primary: #6674c4;
        --color-primary-contrast: #ffffff;

        /* https://maketintsandshades.com/#4051B5 */
        --color-primary-dark-1: #7985cb;
        --color-primary-dark-2: #8c97d3;
        --color-primary-dark-3: #a0a8da;
        --color-primary-dark-4: #b3b9e1;
        --color-primary-dark-5: #c6cbe9;
        --color-primary-dark-6: #d9dcf0;
        --color-primary-dark-7: #eceef8;

        --color-primary-light-1: #5362bc;
        --color-primary-light-2: #4051b5;
        --color-primary-light-3: #3a49a3;
        --color-primary-light-4: #334191;
        --color-primary-light-5: #2d397f;
        --color-primary-light-6: #26316d;
        --color-primary-light-7: #20295b;

        --color-primary-alpha-10: #6674c419;
        --color-primary-alpha-20: #6674c433;
        --color-primary-alpha-30: #6674c44b;
        --color-primary-alpha-40: #6674c466;
        --color-primary-alpha-50: #6674c480;
        --color-primary-alpha-60: #6674c499;
        --color-primary-alpha-70: #6674c4b3;
        --color-primary-alpha-80: #6674c4cc;
        --color-primary-alpha-90: #6674c4e1;
    }

    /* Переопределения переменных для светлой темы */
    @media (prefers-color-scheme: light) {
        :root {}

        #navbar-logo {
            padding: 5px !important;
            background: #14151A;
        }

        #navbar-logo img {
            width: 27px !important;
            height: 27px !important;
        }

        #navbar-logo:hover {
            background: #14151A !important;
        }
    }

    /* Переопределения переменных для тёмной темы */
    @media (prefers-color-scheme: dark) {
        :root {
            /* Шапка */
            --color-nav-bg: #14151A;
            --color-secondary-nav-bg: #14151A;
            --color-nav-text: #BEC1C6;
            --color-nav-hover-bg: #272A35;

            /* Тёмно-серый фон основной */
            --color-body: #1E2129;

            --color-input-background: #14151A;
            --color-menu: #14151A;
            --color-card: #14151A;
            --color-button: #14151A;
        }
    }
    ```

Перезапускаем Gitea.
```sh
sudo systemctl restart gitea
```

После изменения стилей, страницу в браузере нужно обновить с помощью `ctrl + f5`. 

### Настройка `app.ini`

Перечень всех возможных настроек представлен в [документации](https://docs.gitea.com/administration/config-cheat-sheet).

=== "Терминал"
    ```sh
    sudo nano /etc/gitea/app.ini
    ```

=== "Пример параметров app.ini"
    ```ini
    [server]
    LANDING_PAGE = explore

    [other]
    SHOW_FOOTER_VERSION = false
    SHOW_FOOTER_TEMPLATE_LOAD_TIME = false
    SHOW_FOOTER_POWERED_BY = false
    ENABLE_FEED = false

    [i18n]
    LANGS = en-US,ru-RU
    NAMES = English,Русский

    [repository]
    DISABLE_STARS = true

    [cron]
    ENABLED = true

    [ui.meta]
    AUTHOR = Artem Tishenko: Personal Git Repository Hub
    DESCRIPTION = A personal hub for managing Git repositories by Artem Tishenko.
    KEYWORDS = Artem Tishenko, Artyom Tishchenko, Git, self-hosted, personal projects, repositories, Gitea
    ```

Перезапускаем Gitea.
```sh
sudo systemctl restart gitea
```

### Изменение шаблонов страниц

Ищем шаблон для нужной версии в [репозитории Gitea](https://github.com/go-gitea/gitea/tree/main/templates), загружаем с помощью `wget` по такому же пути в `$GITEA_CUSTOM/templates` и редактируем.

Так, например, можно убрать пункт "Помощь" с ссылкой на `https://docs.gitea.com` из основного меню.

```sh
# Путь по умолчанию
export GITEA_CUSTOM=/var/lib/gitea/custom

# gitea --version
export GITEA_VERSION=v1.22.3 

sudo -u git mkdir -p $GITEA_CUSTOM/templates/base
wget -P $GITEA_CUSTOM/templates/base https://raw.githubusercontent.com/go-gitea/gitea/refs/tags/$GITEA_VERSION/templates/base/head_navbar.tmpl 
sudo -u git nano $GITEA_CUSTOM/templates/base/head_navbar.tmpl
```

Перезапускаем Gitea.
```sh
sudo systemctl restart gitea
```