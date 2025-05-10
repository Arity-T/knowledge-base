# Заметка о Powershell

## Установка Powershell

По умолчанию в Windows установлен устаревший Windows PowerShell. Установить новый Powershell можно по [инструкции в репозитории](https://github.com/PowerShell/PowerShell?tab=readme-ov-file#get-powershell).

```powershell
winget search Microsoft.PowerShell
winget install --id Microsoft.PowerShell --source winget
```

Затем стоит [установить PowerShell как профиль по умолчанию](https://stackoverflow.com/a/75891592/17341937).

Чтобы VSCode использовал PowerShell в качестве профиля по умолчанию, нужно добавить в `settings.json` следующий параметр:
```json
{
    "terminal.integrated.defaultProfile.windows": "PowerShell"
}
```


## Мой Powershell profile

Открыть файл настроек Powershell:
```powershell
code $profile # или notepad $profile
```

А вот мои настройки:
```powershell
# Лучше заменить настоящим wget
# https://eternallybored.org/misc/wget/
# Скачать EXE для 64-bit и добавить в папку в PATH
# Удалять алиас нужно только в Windows PowerShell
# remove-item alias:wget

# Заменяем Invoke-WebRequest нормальным curl
# Скачиваем curl for 64-bit тут https://curl.se/windows/
# Из папки bin архива переносим curl.exe в папку в PATH 
# Удалять алиас нужно только в Windows PowerShell
# remove-item alias:curl

# Алиасы
new-alias actvenv venv/Scripts/activate
new-alias grep Select-String
 
function crtvenv {
    virtualenv venv
    actvenv
}

# Аналог команды which в Linux
# https://stackoverflow.com/a/16949127/17341937
function which($name)
{
    Get-Command $name | Select-Object -ExpandProperty Definition
}

# Модуль для автокомплита GIT https://github.com/dahlbyk/posh-git
# Устанавливается одной командой
# PowerShellGet\Install-Module posh-git -Scope CurrentUser -Force
Import-Module posh-git
 
# Модуль для автокомплита Docker https://github.com/matt9ucci/DockerCompletion
# Устанавливается одной командой
# Install-Module DockerCompletion -Scope CurrentUser
Import-Module DockerCompletion
 
# Более удобное автодополнение
Set-PSReadlineKeyHandler -Key Tab -Function MenuComplete
 
# Перемещаться по истории использования команды с помощью стрелочек
Set-PSReadlineKeyHandler -Key UpArrow -Function HistorySearchBackward
Set-PSReadlineKeyHandler -Key DownArrow -Function HistorySearchForward
```


## Выполнение сценариев отключено в этой системе
```powershell
Set-ExecutionPolicy RemoteSigned
```

## Баг с uppercase

В какой-то момент заглавные буквы просто перестают печататься в Powershell, это означает, что нужно обновить `PSReadLine`.

Запустить Powershell от имени администратора и выполнить:
```powershell
Install-Module -Name PowerShellGet -Force
```

Перезапустить от имени администратора и выполнить:
```powershell
Install-Module PSReadLine -AllowPrerelease -Force
```


## Крутой аналог grep - ripgrep

[Скачать](https://github.com/BurntSushi/ripgrep/releases/) релиз для винды и добавить в PATH

```powershell
rg "hello" path/to/dir
```

Аналогично grep можно использовать с другими командами

```powershell
cat README.md | rg hello
```

Можно добавить флаг -i, чтобы ripgrep игнорировал регистр

```powershell
rg -i "hello"
```
