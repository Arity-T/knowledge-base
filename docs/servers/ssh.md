# Заметка по SSH

## SSH-agent

### Установка на Windows

`ssh-agent` является частью OpenSSH. Начиная с Windows 10, OpenSSH устанавливается вместе с системой, однако службу `ssh-agent` надо включить вручную. Для этого нужно запустить `Powershell` от имени администратора и выполнить несколько команд.

```powershell
Set-Service -Name ssh-agent -StartupType Automatic
Start-Service ssh-agent
```

Проверить состояние `ssh-agent` можно с помощью команды.

```powershell
Get-Service -Name ssh-agent | select -property status,name,starttype
```

На Windows `git` по умолчанию использует свою службу `ssh` вместо системной, поэтому `ssh-agent` не будет с ним работать и пароли всё равно придётся вводить вручную. Однако можно настроить `git` так, чтобы он использовал системный `ssh`.

```powershell
git config --global core.sshCommand "C:/Windows/System32/OpenSSH/ssh.exe"
```

### Установка на Linux

На Linux `ssh-agent` как правило уже установлен и активирован из коробки. При перезагрузке системы нужно будет добавлять ключи заново. Можно настроить `ssh` так, чтобы ключи добавлялись автоматически, тогда пароль от каждого ключа будет запрашиваться только один раз.

=== "Терминал"

    ```sh
    nano ~/.ssh/config
    ```

=== "~/.ssh/config"

    ```ini
    Host *
        AddKeysToAgent yes
    ```

### Использование

!!! warning "Security warning"

    На Windows доступ к ключам сохраняется даже после перезагрузки системы.

```sh
# Добавляет ключи из ~/.ssh/
ssh-add
# Можно указать путь
ssh-add path/to/id_rsa
# Список добавленных ключей
ssh-add -l
# Удалить все ключи из памяти агента
ssh-add -D
```

Иногда нужно, чтобы при подключении на сервер, были доступны приватные ключи из локального `ssh-agent`. Для этого можно использовать команду `ssh -A`.

```sh
ssh -A user@server
```

Либо указать `ForwardAgent yes` в конфиге `ssh`.