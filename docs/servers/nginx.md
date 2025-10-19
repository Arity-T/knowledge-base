## Добавление сайта

Создаём конфиг.

=== "Терминал"

    ```sh
    sudo nano /etc/nginx/sites-available/new-site.conf
    ```

=== "Статический сайт"

    ```nginx
    server {
        server_name example.com www.example.com;
        listen 80;

        root /var/www/new-site;
        index index.html;

        location / {
            try_files $uri $uri/ =404;
        }
    }
    ```

=== "Веб-приложение"

    ```nginx
    server {
        server_name giga-chill.ru www.giga-chill.ru;
        listen 80;

        # Все запросы к /api/* перенаправляются на бэкенд
        location /api/ {
            proxy_pass http://127.0.0.1:8081/;
            include proxy_params;
        }

        # Спецификация API в формате OpenAPI
        location = /api/openapi.yml {
            alias /var/www/giga-chill/openapi.yml;
            types { text/yaml yml yaml; }
            charset utf-8;
            charset_types text/yaml application/yaml text/x-yaml application/x-yaml;
        }

        # Документация API в Swagger UI
        location = /api/swagger { return 301 /api/swagger/; }
        location /api/swagger/ {
            proxy_pass http://127.0.0.1:1240/;
            include proxy_params;
        }

        # Документация API в Redocly
        location = /api/redoc { return 301 /api/redoc/; }
        location /api/redoc/ {
            alias /var/www/giga-chill/redoc/;
            index index.html;
        }

        # Все остальные запросы направляются на фронтенд
        location / {
            proxy_pass http://127.0.0.1:3000;
            include proxy_params;
        }
    }
    ```

Активируем конфиг.

```sh
sudo ln -s /etc/nginx/sites-available/new-site.conf /etc/nginx/sites-enabled/
sudo systemctl reload nginx.service
```

Конфиг можно проверить на наличие синтаксических ошибок.

```sh
sudo nginx -t
```

??? question "`open() "/etc/nginx/proxy_params" failed (2: No such file or directory)`"

    Обычно файл `/etc/nginx/proxy_params` создаётся автоматически при установке Nginx, однако его несложно добавить самостоятельно, если по каким-то причинам он не был создан или был удалён.

    === "Терминал"

        ```sh
        sudo nano /etc/nginx/proxy_params
        ```

    === "proxy_params"

        ```nginx
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        ```

## Просмотр логов

По умолчанию логи находятся в `access.log` и `error.log` файлах.

```sh
sudo tail -n 20 /var/log/nginx/access.log
sudo tail -n 20 /var/log/nginx/error.log
```

## SSL-сертификат с certbot

!!! tip "Актуальная версия Python"

    Обычно системный `Python` достаточно старый. Для установки `certbot` может потребоваться более новая версия. Минимальные требования можно узнать на [pypi](https://pypi.org/project/certbot/).

    ```sh
    sudo apt update
    sudo add-apt-repository ppa:deadsnakes/ppa

    # Вместо 3.1x нужно указать актуальную версию Python
    sudo apt install python3.1x python3.1x-venv 
    ```

    Теперь вместо `python3` можно использовать `python3.1x`.

SSL-сертификат получается и устанавливается с помощью [certbot](https://github.com/certbot/certbot). На их сайте есть подробная пошаговая [инструкция](https://certbot.eff.org/instructions?ws=nginx&os=pip) о том, как правильно его установить, получить сертификаты и включить их автообновление.

??? note "Установка вкратце"

    ```sh { .code-wrap }
    # Установили certbot в venv
    # Вместо 3.1x нужно указать актуальную версию Python
    sudo python3.x -m venv /opt/certbot/
    sudo /opt/certbot/bin/pip install --upgrade pip
    sudo /opt/certbot/bin/pip install certbot certbot-nginx

    # Добавили в PATH
    sudo ln -s /opt/certbot/bin/certbot /usr/bin/certbot

    # Автообновление сертификатов
    echo "0 0,12 * * * root /opt/certbot/bin/python -c 'import random; import time; time.sleep(random.random() * 3600)' && sudo certbot renew -q" | sudo tee -a /etc/crontab > /dev/null
    ```
??? tip "Отключение UFW"

    Может потребоваться временно отключить UFW.

    ```sh
    sudo ufw disable

    # Получаем сертификат

    sudo ufw enable
    ```

    Либо насовсем открыть порт 80, тогда и `renew` точно будет работать.

    ```sh
    sudo ufw allow 80/tcp
    ```

Несколько полезных команд.

```sh
# Получить сертификат для определённого домена. Предварительно нужно 
# настроить конфиг nginx для этого домена.
sudo certbot --nginx -d example.com -d www.example.com

# Список сертификатов со сроками их жизни
sudo certbot certificates

# Удалить сертификат (команда предложит выбор)
sudo certbot delete
```