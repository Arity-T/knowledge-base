# Начальная настройка сервера

## Первое подключение
Подключаемся к серверу к `root` по паролю, который должен выдываться вместе с VDS.
```sh
ssh root@<IPv4>
```

Уже в терминале сервера выполняем.
```sh { .code-wrap }
# Создаём пользователя и наделяем его правом использовать `sudo`.
adduser <user>
adduser <username> sudo

su - <user>

# Все файлы, созданные пользователем, по умолчанию будут иметь права 600, а директории - 700.
echo 'umask 0077' >> .bashrc
source ~/.bashrc

# Добавляем свой публичный SSH ключ (cat ~/.ssh/id_rsa.pub), чтобы подключаться к пользователю по SSH напрямую.
mkdir .ssh
echo "<your-id-rsa.pub>" >> .ssh/authorized_keys
# Актуально, только если настройку umask не добавлять в .bashrc
# chmod 700 ~/.ssh
# chmod 600 ~/.ssh/authorized_keys
```

Теперь можно попробовать подключиться к серверу по SSH-ключу.
```sh
ssh <user>@<IPv4>
```

Желательно обновить все пакеты.
```sh
sudo apt update
sudo apt upgrade
```

Можно придумать серверу имя, оно будет отображаться в терминале после `<user>@`.
```sh
sudo nano /etc/hostname
sudo nano /etc/hosts
sudo systemctl restart systemd-hostnamed
```


## Настройка конфига SSH
Открываем конфиг SSH.
```sh
sudo nano /etc/ssh/sshd_config
```

 - `Port <ssh-port>` - можно поменять со стандртного 22 на какой-нибудь другой. Лучше больше 10000, чтобы уменьшить вероятность конфликтов с другим ПО.
 - `PermitRootLogin no` - запрещаем авторизацию по SSH под `root`.
 - `PasswordAuthentication no` - запрещаем авторизацию по SSH по паролю.

??? question "А что будет, если потерять SSH-ключ?"

    Обычно хостинг предоставляет доступ к `VNC` или другие методы подключения к серверу, которые не требуют подключения по SSH. Однако в таком случае будет необходим доступ к личному кабинету хостинга.


На своей машине добавляем сервер в конфиг SSH.

```sh
# На Windows надо будет нажать на Tab, чтобы раскрыть `~`.
# code - VS Code
code ~/.ssh/config 
```

```
Host <host>
    HostName <IPv4>
    User <user>
    Port <ssh-port>
```

Можно проверить, что подключение проходит без ошибок
```sh
ssh <host>
```

## Настройка фаерволла c UFW


```sh
# Установка UFW
sudo apt update
sudo apt install ufw

# Открываем порт, используемый для SSH (по умолчанию 22)
sudo ufw allow <ssh-port>/tcp

# Закрываем все входные
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Включаем фаерволл
sudo ufw enable

# Показать состояние ufw и активные правила
sudo ufw status verbose
```

??? tip "Дополнительные команды `ufw`"

    ```sh
    # Отключить фаерволл
    sudo ufw disable

    # Удалить правило (применятся настройки по умолчанию)
    sudo ufw delete allow <port>/<protocol> # удалить разрешение
    sudo ufw delete deny <port>/<protocol> # удалить запрет

    # Сброс всех правил
    sudo ufw reset

    # Вывести логи ufw
    sudo tail -f -n 100 /var/log/ufw.log

    # Изменить уровень логирования
    sudo ufw logging <low/medium/high>

    # Разрешить доступ ко всем портам с определённого IP-адреса
    sudo ufw allow from <IPv4>
    
    # Разрешить доступ к порту с определённого IP-адреса
    sudo ufw allow from <IPv4> to any port <port>
    ```
