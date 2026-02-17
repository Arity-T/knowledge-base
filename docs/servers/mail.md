# Почта on-premise

Настройка почты на своём сервере со своим доменным именем. В качестве почтового сервера используется [Docker Mailserver](https://github.com/docker-mailserver/docker-mailserver) версии 15.1.0. Вебклиент — [Roundcube Webmail](https://github.com/roundcube/roundcubemail) версии 1.6.11.

## Открытие портов для почты

Многие хостинг провайдеры блокируют исходящие соединения на портах 25, 465 и 587, чтобы предотвратить спам или вредоносные рассылки с их серверов. Можно проверить доступность портов с помощью команды `nc`.

```sh
# Выведет "Connection to smtp.gmail.com 25 port [tcp/*] succeeded!",
# если порт открыт
nc -vz smtp.gmail.com 25
nc -vz smtp.gmail.com 465
nc -vz smtp.gmail.com 587
```

Если порты закрыты, то можно обратиться в поддержку хостинг провайдера с запросом на открытие портов.

??? abstract "Пример обращения в поддержку"

    ```
    Добрый день!

    Прошу разблокировать исходящие соединения на порты 25/tcp, 465/tcp и 587/tcp 
    для моего сервера (<IP-адрес сервера>).
    Сервер используется для личного почтового домена <домен>, не для массовых рассылок.

    Спасибо!
    ```

??? question "Если нельзя открыть исходящие на 25/tcp?"

    Не все хостинги позволяют открывать исходящие соединения на порт 25, даже через поддержку.
    В этом случае можно использовать SMTP Relay, например, [Cloud Postbox](https://yandex.cloud/ru/services/postbox). Инструкция по его настройке приведена [ниже](#smtp-relay).

## Настройка DNS

Настройка DNS на примере домена `tishenko.dev` (почта `@tishenko.dev`). Более подробное описание всех настроек можно прочитать в документации Docker Mailserver: [[1]](https://docker-mailserver.github.io/docker-mailserver/latest/usage/#minimal-dns-setup) и [[2]](https://docker-mailserver.github.io/docker-mailserver/latest/config/best-practices/dkim_dmarc_spf/).

Со стороны DNS провайдера:

1. Добавляем поддомен для почты, например, `mail.tishenko.dev` и `www.mail.tishenko.dev`. В A-записи поддомена указываем IP-адрес сервера.

2. Добавляем MX-запись для основного домена `tishenko.dev`, именно этот домен будет использоваться для отправки и получения почты `@tishenko.dev`. 
   ```dns
   10 mail.tishenko.dev.
   ```
   Обязательно с точкой в конце. Число 10 это приоритет MX-записи, чем меньше число, тем выше приоритет. Приоритет не играет роли, если запись только одна. MX-записи, созданные DNS провайдером, нужно удалить.

3. Добавляем TXT-запись для DMARC. Запись надо создать для домена `_dmarc.tishenko.dev.`.
   ```dns
   v=DMARC1; p=quarantine; sp=quarantine; fo=0; adkim=r; aspf=r; pct=100; rf=afrf; ri=86400; rua=mailto:dmarc.report@tishenko.dev; ruf=mailto:dmarc.report@tishenko.dev
   ```
   DMARC-записи, созданные DNS провайдером, нужно удалить.

4. Добавляем TXT-запись для SPF. Запись надо создать для домена `tishenko.dev.`. 
    ```dns
    v=spf1 mx -all
    ```
    SPF-записи, созданные DNS провайдером, нужно удалить.

5. Для окончательной настройки нужно также добавить TXT-запись для DKIM. Однако это можно сделать только после настройки почтового сервера и создания пары ключей. Подробнее про настройку DKIM написано [ниже](#настройка-dkim).

Со стороны владельца IP-адреса, как правило это VDS провайдер, создаём или редактируем PTR запись для IP-адреса почтового сервера. Указываем в ней почтовый адрес: `mail.tishenko.dev.`.

??? question "Как проверить настройки DNS?"

    Можно использовать [DNS Checker](https://dnschecker.org/) для проверки [A](https://dnschecker.org/#A/mail.tishenko.dev), [MX](https://dnschecker.org/#MX/tishenko.dev), [PTR](https://dnschecker.org/#PTR/146.103.98.219), [DMARC](https://dnschecker.org/#TXT/_dmarc.tishenko.dev) и [SPF](https://dnschecker.org/#TXT/tishenko.dev) записей.

    Либо использовать команду `dig`.

    ```sh
    # Команда должна вывести IP-адрес сервера
    dig @1.1.1.1 +short A mail.tishenko.dev

    # 10 mail.tishenko.dev.
    dig @1.1.1.1 +short MX tishenko.dev

    # mail.tishenko.dev.
    dig @1.1.1.1 +short -x 146.103.98.219

    # Проверить DMARC
    dig @1.1.1.1 +short TXT _dmarc.tishenko.dev

    # Проверить SPF
    dig @1.1.1.1 +short TXT tishenko.dev
    ```

    Обновление DNS происходит не мгновенно, обычно это занимает около 20 минут.

??? abstract "Пример файла зоны"

    В панели управления DNS провайдера можно выгрузить файл зоны и убедиться, что все записи добавились корректно.

    ```dns
    	IN	MX	10	mail.tishenko.dev.
    mail	IN	A	146.103.98.219
    www.mail	IN	A	146.103.98.219
    @	600	IN	TXT	"v=spf1 mx -all"
    _dmarc	600	IN	TXT	"v=DMARC1; p=quarantine; sp=quarantine; fo=0; adkim=r; aspf=r; pct=100; rf=afrf; ri=86400; rua=mailto:dmarc.report@tishenko.dev; ruf=mailto:dmarc.report@tishenko.dev"
    ```

## Docker Mailserver

Docker Mailserver (DMS) имеет отличную [документацию](https://docker-mailserver.github.io/docker-mailserver/latest/usage/). И DNS и почтовый сервер можно настроить просто пройдясь по ней. Эта заметка лишь дополняет документацию.

```sh
# Открываем порты для почты (если используется ufw)
sudo ufw allow 25,143,465,587,993/tcp

# Создаём отдельного пользователя для управления почтой
# Пользователь vmail в контейнере DMS по умолчанию имеет uid 5000,
# поэтому желательно, чтобы и на хосте он имел такой же uid
sudo useradd -u 5000 --create-home --shell /bin/bash vmail
sudo usermod -aG docker vmail

# Переключаемся на пользователя vmail
sudo su - vmail

# Скачиваем compose.yaml и mailserver.env из репозитория DMS
# Версия 15.1.0
DMS_GITHUB_URL="https://raw.githubusercontent.com/docker-mailserver/docker-mailserver/refs/tags/v15.1.0"
wget "${DMS_GITHUB_URL}/compose.yaml"
wget "${DMS_GITHUB_URL}/mailserver.env"
```

Теперь нужно отредактировать `compose.yaml` и `mailserver.env`.

=== "Терминал"

    ```sh
    nano compose.yaml
    ```

=== "compose.yaml"

    В `image` указываем конкретную версию вместо `:latest`. В `hostname` указываем почтовый домен (e. g. mail.tishenko.dev).

    Также прокидываем в контейнер волюм `/etc/letsencrypt` для подключения SSL сертификатов, актуально если на хосте используется letsencrypt.

    ```yaml
    services:
      mailserver:
        image: ghcr.io/docker-mailserver/docker-mailserver:15.1.0
        container_name: mailserver
        # Provide the FQDN of your mail server here (Your DNS MX record should point to this value)
        hostname: mail.tishenko.dev
        env_file: mailserver.env
        # More information about the mail-server ports:
        # https://docker-mailserver.github.io/docker-mailserver/latest/config/security/understanding-the-ports/
        ports:
          - "25:25"    # SMTP  (explicit TLS => STARTTLS, Authentication is DISABLED => use port 465/587 instead)
          - "143:143"  # IMAP4 (explicit TLS => STARTTLS)
          - "465:465"  # ESMTP (implicit TLS)
          - "587:587"  # ESMTP (explicit TLS => STARTTLS)
          - "993:993"  # IMAP4 (implicit TLS)
        volumes:
          - ./docker-data/dms/mail-data/:/var/mail/
          - ./docker-data/dms/mail-state/:/var/mail-state/
          - ./docker-data/dms/mail-logs/:/var/log/mail/
          - ./docker-data/dms/config/:/tmp/docker-mailserver/
          - /etc/localtime:/etc/localtime:ro
          - /etc/letsencrypt:/etc/letsencrypt:ro
        restart: always
        stop_grace_period: 1m
        # Uncomment if using `ENABLE_FAIL2BAN=1`:
        # cap_add:
        #   - NET_ADMIN
        healthcheck:
          test: "ss --listening --ipv4 --tcp | grep --silent ':smtp' || exit 1"
          timeout: 3s
          retries: 0
    ```

=== "mailserver.env"

    В этой заметке DMS настраивается с антиспамом Rspamd. Как отмечено в [документации](https://docker-mailserver.github.io/docker-mailserver/v15.1/config/security/rspamd/), его планируется использовать по умолчанию в будущих версиях DMS. На той же странице документации перечислены legacy проверки, которые нужно отключить. Тут они также продублированы.

    ```sh
    # Указываем тип SSL сертификатов
    SSL_TYPE=letsencrypt

    # Включаем Rspamd
    ENABLE_RSPAMD=1

    # Отключаем legacy проверки, т. к. они уже включены в Rspamd
    ENABLE_OPENDKIM=0
    ENABLE_OPENDMARC=0
    ENABLE_POLICYD_SPF=0
    ENABLE_AMAVIS=0
    RSPAMD_GREYLISTING=1
    ```

```sh
# Создаём директории для волюмов DMS заранее,
# чтобы у них был правильный владелец (vmail)
mkdir -p ./docker-data/dms/{mail-data,mail-state,mail-logs,config}

# Запускаем DMS
docker compose up -d

# В течение двух минут после первого запуска DMS нужно создать хотя бы один
# почтовый адрес, иначе контейнер завершится с ошибкой
# Команда предложит задать пароль для нового почтового аккаунта
docker exec -it mailserver setup email add artem@tishenko.dev

# Обязательно добавляем alias для адреса postmaster
docker exec -it mailserver setup alias add postmaster@tishenko.dev artem@tishenko.dev
```

### Настройка SSL

В документации DMS есть отдельная [страница](https://docker-mailserver.github.io/docker-mailserver/latest/config/security/ssl/) про настройку SSL сертификатов.

Далее подразумевается, что волюм `/etc/letsencrypt` уже прокинут в контейнер, а также в `mailserver.env` указана переменная `SSL_TYPE=letsencrypt`.

Получаем сертификаты. Команды нужно выполнять от пользователя с правом использовать `sudo`. `certbot` можно установить с помощью [pip](https://certbot.eff.org/instructions?ws=other&os=pip).

```sh
# Порт 80 нужен для получения и обновления сертификатов 
sudo ufw allow 80/tcp

# Если на сервере есть nginx или другой веб-сервер, используем соответствующий флаг
sudo certbot certonly --nginx -d mail.tishenko.dev -d www.mail.tishenko.dev

# Если на сервере нет nginx (порт 80 не должен быть занят)
sudo certbot certonly --standalone -d mail.tishenko.dev -d www.mail.tishenko.dev
```


### Настройка DKIM

В документации DMS есть отдельная [страница](https://docker-mailserver.github.io/docker-mailserver/latest/config/best-practices/dkim_dmarc_spf/) про настройку DKIM, DMARC и SPF. Про настройку DMARC и SPF написано [выше](#настройка-dns), а вот для настройки DKIM нужно сначала сгенерировать пару ключей. Публичный ключ как раз и указывается в DKIM.

Команда для генерации ключей. DMS должен быть запущен.

```sh
# Выведет в консоль значение для TXT-записи
# Также её можно узнать в файле
# cat ./docker-data/dms/config/rspamd/dkim/rsa-2048-mail-tishenko.dev.public.dns.txt
docker exec -it mailserver setup config dkim domain tishenko.dev
```

Теперь добавляем TXT запись для DKIM в DNS. Имя записи должно быть `mail._domainkey.tishenko.dev.`. Проверить запись можно с помощью сайта [DNS Checker](https://dnschecker.org/#TXT/mail._domainkey.tishenko.dev) или команды `dig`.

```sh
# Должна вывести "v=DKIM1; k=rsa; p=<публичный ключ>"
dig @1.1.1.1 +short TXT mail._domainkey.tishenko.dev
```

### Проверка

Работоспособность и настройки DMS можно проверить с помощью сайта [Mail-Tester](https://www.mail-tester.com/).

Пример команды для отправки тестового письма.
```sh
docker exec -it mailserver swaks \
  --to <адрес с mail-tester> \
  --from artem@tishenko.dev \
  --server mail.tishenko.dev \
  --port 587 \
  --tls \
  --auth LOGIN \
  --auth-user artem@tishenko.dev \
  --auth-password 'password'
```

Если письмо дойдёт до тестового адреса, то сайт выведет результаты проверки DNS-записей и общую оценку настройки почтового сервера. Если всё сделано правильно, то оценка будет 10/10.

Дополнительно можно проверить настройки почтового сервера с помощью сайта [MX Toolbox](https://mxtoolbox.com/emailhealth).

### Администрирование

Администрировать DMS можно через скрипт `setup` внутри контейнера. Для этого можно подключиться к контейнеру с помощью команды.

```sh
docker exec -it mailserver bash

# Уже внутри контейнера
setup help
```

Если нужно выполнить всего одну команду, то можно не запускать bash.

```sh
docker exec -it mailserver setup help
```


## Roundcube

Roundcube проще всего развернуть с помощью Docker Compose. Актуальную версию образа можно выбрать на [Docker Hub](https://hub.docker.com/r/roundcube/roundcubemail). Там же можно посмотреть список переменных окружения и их значения. Далее подразумевается, что выбран образ `apache-nonroot`, а также что для управления почтой создан отдельный пользователь `vmail` с uid/gid 5000, как показано в инструкции [выше](#docker-mailserver).

=== "Терминал"

    ```sh
    # Переключаемся на пользователя vmail
    sudo su - vmail

    mkdir ./roundcube
    cd ./roundcube

    # Создаём директории для волюмов Roundcube заранее,
    # чтобы у них был правильный владелец (vmail)
    mkdir -p ./roundcube/{app,config,db,tmp}

    nano docker-compose.yml
    ```

=== "Пример docker-compose.yml"

    ```yaml
    services:
      roundcube:
        image: roundcube/roundcubemail:1.6.11-apache-nonroot
        container_name: roundcube
        restart: always
        user: "5000:5000"
        ports:
          - "25025:8000"
        environment:
          # IMAP
          - ROUNDCUBEMAIL_DEFAULT_HOST=ssl://mail.tishenko.dev
          - ROUNDCUBEMAIL_DEFAULT_PORT=993
    
          # SMTP
          - ROUNDCUBEMAIL_SMTP_SERVER=tls://mail.tishenko.dev
          - ROUNDCUBEMAIL_SMTP_PORT=587
          - ROUNDCUBEMAIL_SMTP_USER=%u
          - ROUNDCUBEMAIL_SMTP_PASS=%p
    
          # DB
          - ROUNDCUBEMAIL_DB_TYPE=sqlite
    
          # Misc
          - ROUNDCUBEMAIL_USERNAME_DOMAIN=tishenko.dev
        volumes:
          - ./roundcube/app:/var/www/html
          - ./roundcube/config:/var/roundcube/config
          - ./roundcube/db:/var/roundcube/db
          - ./roundcube/tmp:/tmp/roundcube-temp
    ```

Теперь Roundcube доступен на `http://localhost:25025`, чтобы его можно было использовать извне, нужно настроить nginx или аналогичный веб-сервер.


=== "Терминал"

    ```sh
    sudo nano /etc/nginx/sites-available/mail.conf
    sudo ln -s /etc/nginx/sites-available/mail.conf /etc/nginx/sites-enabled/
    ```

=== "Пример nginx конфига"

    ```nginx
    server {
        listen 80;
        server_name mail.tishenko.dev www.mail.tishenko.dev;
    
        client_max_body_size 25m;
    
        location / {
            proxy_pass http://127.0.0.1:25025;
            include proxy_params;
        }
    }
    ```

Установить SSL сертификат можно с помощью certbot. Причём если сертификат уже был получен на этапе [настройки DMS](#настройка-ssl), то certbot предложит использовать его.

```sh
sudo certbot --nginx -d mail.tishenko.dev -d www.mail.tishenko.dev
```

### Конфиг

Некоторые настройки Roundcube нельзя задать через переменные окружения, они задаются в файле `config.inc.php`. Например, "название продукта", оно отображается в заголовке страницы, на странице входа и в других местах. По умолчанию это `Roundcube Webmail`. Также по умолчанию в Roundcube очень короткое время сессии, всего 10 минут, после которых нужно логиниться заново. Эти параметры можно изменить в `config/config.inc.php`.

=== "Терминал"

    ```sh
    nano roundcube/config/config.inc.php
    ```

=== "config.inc.php"

    ```php
    <?php
    $config['product_name'] = 'Tish\'s Mail';
    $config['session_lifetime'] = 60 * 24;
    ```

После изменения конфига нужно перезапустить Roundcube.

```sh
docker compose restart roundcube
```

### Настройки аккаунта

Настройки, относящиеся к конкретному аккаунту, можно задать через UI. Как минимум стоит установить отображаемое имя, иначе у получателей будет отображаться только адрес электронной почты: `Настройки` -> `Профили` -> `Отображаемое имя`. В разделе с профилями также можно указать подпись для писем.

Roundcube позволяет задать несколько профилей и соответствующих адресов для одного аккаунта и легко переключаться между ними через UI. Для этого в DMS нужно создать алиас для основного адреса, а затем добавить профиль через UI Roundcube в разделе `Настройки` -> `Профили`.

```sh
docker exec -it mailserver setup alias add <алиас> <основной адрес>
```

### Внешний вид

Подразумевается, что прокинут волюм `./roundcube/app:/var/www/html`. Чтобы внешние изменения не терялись при перезапуске контейнера, нужно создать свою тему для Roundcube на основе темы по умолчанию и изменять её.

```sh
# Желательно выполнять команды от пользователя vmail,
# чтобы не было проблем с правами
# Либо подключиться к контейнеру через docker exec -it roundcube bash
# и редактировать темы из контейнера
sudo su - vmail

# Переходим в директорию с docker-compose.yml для Roundcube
cd ./roundcube

# В разделе environment добавляем переменную окружения
# ROUNDCUBEMAIL_SKIN=custom
nano docker-compose.yml

# Копируем тему по умолчанию
# Roundcube должен был быть запущен хотя бы один раз, 
# чтобы тема по умолчанию появилась в волюме
cp -r ./roundcube/app/skins/elastic/ ./roundcube/app/skins/custom/

# Перезапускаем Roundcube
docker compose down
docker compose up -d
```

Теперь любые изменения в теме `custom` будут сохраняться при перезапуске контейнера.

Подробнее про темы Roundcube можно посмотреть в [документации](https://github.com/roundcube/roundcubemail/wiki/Skins).

#### Favicon

Favicon находится в `skins/custom/images/favicon.ico`. Достаточно просто заменить его на свой.

```sh
cp your-favicon.ico ./roundcube/app/skins/custom/images/favicon.ico
```

#### Логотип

Логотип находится в `skins/custom/images/logo.svg`. Достаточно просто заменить его на свой.

```sh
cp your-logo.svg ./roundcube/app/skins/custom/images/logo.svg
```


## Логотип в письмах

Для того чтобы у получателей вместо плейсхолдера рядом с именем отправителя отображался логотип, нужно добавить BIMI TXT-запись в DNS для домена `default._bimi.tishenko.dev.`. Нужно будет настроить Nginx или другой веб-сервер, чтобы логотип был доступен по указанному в BIMI адресу.

```dns
v=BIMI1; l=https://tishenko.dev/logo.svg;
```

Однако в gmail и некоторых других почтовых клиентах он всё равно не будет отображаться, так как они требуют для этого платные VMC сертификаты.

## SMTP Relay

Не всегда есть возможность открыть исходящие соединения на порт 25. Для этого можно использовать SMTP Relay. Это отдельный сервис, у которого есть свои сервера с открытыми почтовыми портами. Бонусом является то, что при использовании подобных сервисов обычно требуется меньше настроек DNS, а также письма с IP адресов таких сервисов практически не попадают в спам. [Yandex Cloud Postbox](https://yandex.cloud/ru/services/postbox) это пример подобного сервиса. Вообще говоря, он предназначен для транзакционных рассылок, то есть сообщений с подтверждением разных действий, но его можно использовать и для отправки писем с личной почты.

1. После регистрации, нужно создать почтовый адрес для отправки писем. При создании нужно указать домен, например, `tishenko.dev` и выбрать простой вариант настройки DKIM.
2. Подтверждаем принадлежность домена. Для этого нужно добавить две CNAME записи в DNS. Для каждого адреса генерируются уникальные ключи, ниже пример для домена `tishenko.dev`.
```dns
egt9mf1fnu9td07bs857-1._domainkey	IN	CNAME	egt9mf1fnu9td07bs857-1.dkim.pstbx.ru.
egt9mf1fnu9td07bs857-2._domainkey	IN	CNAME	egt9mf1fnu9td07bs857-2.dkim.pstbx.ru.
```
Затем нужно подождать пока записи появятся в DNS, затем запустить проверку в Cloud Postbox. Посмотреть процесс распространения записей можно с помощью сайта [DNS Checker](egt9mf1fnu9td07bs857-1._domainkey.tishenko.dev).
3. Добавляем TXT запись для домена `tishenko.dev`.
```dns
v=spf1 include:_spf.yandex.net -all
```

Дальше настраиваем Docker Mailserver для работы с SMTP Relay. [Документация DMS](https://docker-mailserver.github.io/docker-mailserver/latest/config/advanced/mail-forwarding/relay-hosts) по настройке SMTP Relay и [документация Yandex Cloud Postbox](https://yandex.cloud/en/docs/tutorials/serverless/postfix-integration) в помощь. В `mailserver.env` нужно добавить следующие переменные:

```sh
# Отправка всей исходящей почты через Postbox
DEFAULT_RELAY_HOST=[postbox.cloud.yandex.net]:587

# SMTP-учётка Postbox:
RELAY_USER=SMTP_USERNAME
RELAY_PASSWORD=SMTP_PASSWORD
```

Для получения паролей надо создать [сервисный аккаунт](https://yandex.cloud/ru/docs/iam/operations/sa/create), назначить ему роль [`postbox.sender`](https://yandex.cloud/ru/docs/tutorials/serverless/postfix-integration#infrastructure), а затем создать API-ключ с областью действия `yc.postbox.send`. Идентификатор ключа можно использовать как `RELAY_USER`, а сам секретный ключ как `RELAY_PASSWORD`.