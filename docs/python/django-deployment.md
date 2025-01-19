Предполагается, что на сервере установлена `Ubuntu`.

## Подготовка

В этом разделе общая последовательность действий для запуска `Django` приложения на сервере. Многое в нём зависит от конкретного проекта, поэтому команды и их последовательность может быть совсем другой. Главное, что в результате папка с приложением должна оказаться на сервере, а также должно быть создано виртуальное окружение `Python` (не обязательно через `venv`) со всеми зависимостями проекта.

### Установка Python

```sh
# Для начала обновим установленные пакеты
sudo apt update
sudo apt upgrade

# Не забудьте указать нужную версию python
sudo apt install python3.10 python3.10-venv -y
```

Python может сходу не установиться и из-за следующей ошибки.
```
E: Unable to locate package python3.10
E: Couldn't find any package by glob 'python3.10'
E: Unable to locate package python3.10-venv
E: Couldn't find any package by glob 'python3.10-venv'
```

Нужно просто добавить репозиторий со списками пакетов Python.
```sh
sudo add-apt-repository ppa:deadsnakes/ppa   
sudo apt update 
# и снова пробуем установить python
```

### Клонируем проект

На сервере создаём SSH ключ и копируем его в раздел `Deploy keys` (в случае `GitHub`) в настройках репозитория. Если проект публичный, то ключ создавать не обязательно.
```sh
ssh-keygen
cat ~/.ssh/id_rsa.pub
```

А затем клонируем репозиторий.
```sh
git clone <repo-url.git>
```

Если вдруг `Git` не установлен.

```sh
sudo apt install git
```

### Готовим Django к запуску

Предварительно нужно добавить домен или IP-адрес сервера в `ALLOWED_HOSTS` в `settings.py`. Также стоит посмотреть на [deployment checklist](https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/), который предоставляет документация `Django`.

Настраиваем виртуальное окружение.

```sh
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Создаём миграции и суперпользователя. Команды отличаются в зависимости от проекта.

```sh
python manage.py makemigrations <app_name>
python manage.py migrate
python manage.py createsuperuser
```


## Gunicorn

### Установка
```sh { .annotate }
# В виртуальном окружении проекта выполнить
pip install gunicorn

# Можно перейти по адресу сервера в браузере на порт 8000 и убедиться,
# что всё работает (ну почти, статики тут не будет)
# Не на всех VDS может быть открыт 8000 порт, в таком случае просто 
# смотрим на отсутствие ошибок
gunicorn --bind 0.0.0.0:8000 django-app-name.wsgi # (1)!
```

1. Не забудьте заменить `django-app-name.wsgi` на реальный путь к `wsgi.py` файлу проекта. 

### UNIX-сокет
Создаём UNIX-сокет в `systemd` для локального обмена данными между `Gunicorn`, в котором развёрнут `Django`, и `nginx`. 

```sh
sudo nano /etc/systemd/system/gunicorn.socket
```

```ini
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

!!! tip "UNIX-сокет можно назвать как угодно"

    Это особенно полезно, когда на одной машине с помощью `Gunicorn` нужно развёрнуть сразу несколько приложений. Кстати, имя сокета (`gunicorn.sock`) не обязательно должно совпадать с названием файла конфигурации сокета для `systemd` (`gunicorn.socket`). При этом в командах по типу `systemctl status` нужно будет использовать имя конфигурационного файла.

### Сервис в systemd

Создаём сервис в `systemd`, чтобы `Gunicorn` мог работать как фоновый процесс и запускался вместе с системой.

```sh
sudo nano /etc/systemd/system/gunicorn.service
```

В секции `Service` нужно указать актуального пользователя и путь до проекта, а также путь до `wsgi.py` внутри проекта.

```ini
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=user
Group=user
WorkingDirectory=/home/user/project-folder
ExecStart=/home/user/project-folder/venv/bin/gunicorn \
          --access-logfile - \
          --workers 1 \
          --bind unix:/run/gunicorn.sock \
          django-app-name.wsgi:application

[Install]
WantedBy=multi-user.target
```

Теперь можно запустить сокет и добавить его в автозапуск. `systemd` автоматически запустит сервис `Gunicorn`, когда на сокет придёт первый запрос.

```sh
# Предварительно перезагружаем systemd
sudo systemctl daemon-reload

sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```


## Nginx

### Установка

После установки `nginx` должен запуститься автоматически, чтобы проверить можно перейти по адресу сервера в браузере.

```sh
sudo apt install nginx
```

### Собираем статику

Собираем статику (стили, скрипты, картинки) и переносим в `/var/www/` - именно этот каталог обычно используется для её хранения. Если поместить статику в другое место, то могут возникнуть проблемы с доступами. `nginx` просто не сможет работать с нашими файлами, если у него не будет прав на чтение файлов статики и прав на исполнение всех директорий в путях к этим файлам. В конфиге `/etc/nginx/nginx.conf` можно узнать от имени какого пользователя `nginx` обрабатывает запросы.

```bash
# Команда собирает всю статику Django в папку, которая
# указана в settings.py (см. STATIC_ROOT)
python manage.py collectstatic

# Переносим статику из staticfiles (см. STATIC_ROOT) в /var/www/
# Вместо static может потребоваться указать другую папку (см. STATIC_URL)
sudo mkdir /var/www/django-project
sudo cp -r staticfiles /var/www/django-project/static
```

### Конфиг nginx

Теперь можно настроить `nginx`.
```bash
# Вместо my-site можно указать название проекта
sudo nano /etc/nginx/sites-available/my-site
```

Минимальный конфиг.
```nginx
server {
    listen 80;
    server_name your_domain_or_ip;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /var/www/django-project;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

Добавляем конфиг в активные конфиги, с которыми сейчас работает nginx.

```sh
sudo ln -s /etc/nginx/sites-available/my-site /etc/nginx/sites-enabled
```

Проверка корректности конфигов.

```sh
sudo nginx -t
```

Если всё в порядке, перезапускаем `nginx`.

```sh
sudo systemctl restart nginx
```


## Если что-то идёт не так...

### Логи NGINX
```bash
# Информация обо всех запросах
sudo tail -f /var/log/nginx/access.log

# Информация обо всех ошибках и предупреждениях
sudo tail -f /var/log/nginx/error.log

# Проверка корректности конфигов
sudo nginx -t

# Очистка логов без необходимости перезапуска NGINX
sudo truncate -s 0 /var/log/nginx/access.log
sudo truncate -s 0 /var/log/nginx/error.log
```

### Логи Gunicorn
```bash
sudo journalctl -u gunicorn.service -f
sudo journalctl -u gunicorn.socket -f
```

## Полезные ссылки
 - [How to deploy Django](https://docs.djangoproject.com/en/5.1/howto/deployment/)
 - [Deployment checklist](https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/)