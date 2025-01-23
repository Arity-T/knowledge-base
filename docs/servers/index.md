# Servers

## Первое подключение

Подключаемся к серверу к `root` по паролю, который должен выдываться вместе с VDS.
```sh
ssh root@<IPv4>
```

Создаём пользователя с правом использовать `sudo`.
```sh
adduser <user>
sudo adduser <username> sudo

su - <user>
mkdir .ssh
# cat ~/.ssh/id_rsa.pub
echo "<your-id-rsa.pub>" >> .ssh/authorized_keys
```

Придумываем имя новому серверу.
```sh
sudo nano /etc/hostname
sudo nano /etc/hosts
sudo systemctl restart systemd-hostnamed
```

На своей машине добавляем сервер в конфиг SSH.

```sh
code ~/.ssh/config
```

```
Host <hostname>
    HostName <IPv4>
    User <user>
```
