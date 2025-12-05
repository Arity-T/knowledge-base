# Начальная настройка сервера

## Первое подключение
Подключаемся к серверу к `root` по паролю, который должен выдаваться вместе с VDS.
```sh
ssh root@<IPv4>
```

Уже в терминале сервера выполняем.
```sh { .code-wrap }
# Создаём пользователя и наделяем правом использовать `sudo`.
adduser <user>
adduser <user> sudo

# Переключаемся на нового пользователя
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

Желательно обновить все пакеты и перезагрузить сервер.
```sh
sudo apt update
sudo apt upgrade
sudo reboot
```

Можно придумать серверу имя, оно будет отображаться в терминале после `<user>@`.
```sh
sudo nano /etc/hostname
sudo systemctl restart systemd-hostnamed

# В hosts тоже иногда есть строчка вида
# 127.0.1.1 <hostname>
sudo nano /etc/hosts
```


## Настройка конфига SSH
Открываем конфиг SSH.
```sh
sudo nano /etc/ssh/sshd_config
```

 - `Port <ssh-port>` - можно поменять со стандартного 22 на какой-нибудь другой. Лучше больше 10000, чтобы уменьшить вероятность конфликтов с другим ПО.
 - `PermitRootLogin no` - запрещаем авторизацию по SSH под `root`.
 - `PasswordAuthentication no` - запрещаем авторизацию по SSH по паролю.

После внесения изменений в конфиг, необходимо перезагрузить `sshd`.
```sh
# На некоторых системах ssh вместо sshd
sudo systemctl reload sshd

# Иногда дополнительно нужно выполнить
systemctl daemon-reload
systemctl restart ssh.socket
```

??? question "А что будет, если потерять SSH-ключ?"

    Хостинг предоставляет доступ к `VNC` или другие методы подключения к серверу, которые не требуют подключения по SSH. Однако в таком случае будет необходим доступ к личному кабинету хостинга.


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

Можно проверить, что подключение проходит без ошибок.
```sh
# Если конфиг настроен
ssh <host>
```
```sh
# Без конфига
ssh <user>@<IPv4> -p <ssh-port>
```

## Создание SWAP-файла

Лучше пожертвовать пару гигабайт от объёма диска сервера на SWAP-файл, чтобы уменьшить вероятность того, что в один прекрасный момент сервер крашнется из-за нехватки памяти.

```sh
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
sudo swapon --show

# Чтобы swap-файл подключался при перезагрузке сервера
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

Чтобы удалить SWAP-файл, нужно выполнить следующие команды.

```sh
sudo swapoff /swapfile

# Удаляем строку со swap-файлом
sudo nano /etc/fstab
```

## Настройка фаерволла c UFW


```sh
# Установка UFW
sudo apt update
sudo apt install ufw -y

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

    # Удалить правило (будут применены настройки по умолчанию)
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

    Некоторые приложения, например `OpenSSH` или `Nginx`, добавляют пресеты с правилами для `ufw`, которые точно так же можно разрешать и запрещать.

    ```sh
    # Вывести список пресетов
    sudo ufw app list

    # Открыть все соединения, которые нужны Nginx
    sudo ufw allow "Nginx Full"

    # Удалить правило для пресета
    sudo ufw delete allow "Nginx Full"
    ```

## Настройка Fail2Ban

[Fail2Ban](https://github.com/fail2ban/fail2ban) - базовая защита сервера от brute-force атак.

```sh
sudo apt update
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
```

Теперь нужно [правильно настроить Fail2Ban](https://github.com/fail2ban/fail2ban/wiki/Proper-fail2ban-configuration).

```sh
# Создаём файл с пользовательскими настройками
sudo nano /etc/fail2ban/jail.local
```

Настройка защиты SSH сервера.
```ini
[sshd]
# Единственный обязательный параметр
enabled = true

# Можно не указывать, если используется стандартный порт
port = <ssh-port>

# Пример настроек. Эти параметры можно не указывать, тогда будут использованы
# значения по умолчанию.
# Если в течении 24 часов
findtime = 86400
# произведено 3 неудачных попытки логина,
maxretry = 3
# то банить IP навсегда.
bantime = -1
```

!!! tip "Более строгий конфиг для `fail2ban`"

    Если на сервере настроена авторизация по ключу, можно смело использовать такой конфиг. 
    
    При авторизации по ключу, бан возможен только в случае указания неправильного имени пользователя, что исключено при использовании корректно настроенного SSH-конфига. В случае случайного бана всегда можно зайти на сервер через личный кабинет хостинга.

    ```ini
    [sshd]
    enabled = true
    port = <ssh-port>
    # Если произведена хотя бы одна неудачная попытка логина,
    maxretry = 1
    # то банить IP навсегда.
    bantime = -1
    ```


```sh
# Применяем настройки
sudo fail2ban-client reload
```

После установки и первоначальной настройки `fail2ban` лучше перезагрузить сервер, иначе `fail2ban` может не заработать.
```sh
sudo reboot
```

??? tip "Дополнительные команды `fail2ban`"

    ```sh
    # Вывести список активных jail's
    sudo fail2ban-client status

    # Вывести информацию по конкретному jail, в т. ч. список заблокированных IP
    sudo fail2ban-client status <jail-name>

    # Разблокировать IP
    sudo fail2ban-client set <jail-name> unbanip <IP>
    
    # Вывести логи fail2ban
    sudo tail -f -n 100 /var/log/fail2ban.log
    ```

## Дополнительно

```sh
# Вывести записи о неудачных попытках входа в систему
sudo lastb | head -n 20

# Очистить записи о неудачных попытках входа в систему
sudo truncate -s 0 /var/log/btmp

# Показывает, кто в системе прямо сейчас
sudo w

# Логи попыток входа
sudo grep "Accepted password" /var/log/auth.log | tail -n 20
sudo grep "Failed password" /var/log/auth.log | tail -n 20
sudo grep "Invalid user" /var/log/auth.log | tail -n 20

# Очистить логи с попытками входа
sudo truncate -s 0 /var/log/auth.log
```

## Полезные ссылки
 - [Initial Server Setup with Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-20-04)
 - [UFW Essentials: Common Firewall Rules and Commands](https://www.digitalocean.com/community/tutorials/ufw-essentials-common-firewall-rules-and-commands)
 - [VPS cheatsheet](https://habr.com/ru/articles/756804/)
 - [Fail2Ban](https://github.com/fail2ban/fail2ban)