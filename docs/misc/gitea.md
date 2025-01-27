# Кастомизация Gitea

Во всех командах подразумевается, что Gitea [установлена из бинарника](https://docs.gitea.com/installation/install-from-binary) и [запускается как `systemd` сервис](https://docs.gitea.com/installation/linux-service).

В документации есть страница, посвящённая [кастомизации Gitea](https://docs.gitea.com/administration/customizing-gitea).


## Свой `css`

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

## Настройка `app.ini`

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

    [ui.meta]
    AUTHOR = Artem Tishenko: Personal Git Repository Hub
    DESCRIPTION = A personal hub for managing Git repositories by Artem Tishenko.
    KEYWORDS = Artem Tishenko, Artyom Tishchenko, Git, self-hosted, personal projects, repositories, Gitea
    ```

Перезапускаем Gitea.
```sh
sudo systemctl restart gitea
```

## Изменение шаблонов страниц

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