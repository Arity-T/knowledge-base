# Заметка о Powershell

## Установка Powershell

По умолчанию в Windows установлен устаревший Windows PowerShell с кучей багов и отсутствующей поддержкой базовых операторов (`&&`, `|`, `||`). Установить новый Powershell можно по [инструкции в репозитории](https://github.com/PowerShell/PowerShell?tab=readme-ov-file#get-powershell).

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

## Обновление PSReadLine

На старых версиях PSReadLine, который используется под капотом PowerShell, возникают различные баги: [иногда не печатаются заглавные буквы](https://github.com/PowerShell/PowerShell/issues/10794#issuecomment-542319327), [не работает `Ctrl + C` при запуске с русской раскладкой](https://github.com/PowerShell/PSReadLine/issues/1393#issuecomment-2065423282). Так что стоит сразу его обновить.

Закрыть открытые PowerShell, в том числе внутри VS Code или других IDE. Запустить `cmd` от имени администратора и выполнить:

```cmd
"C:\Program Files\PowerShell\7\pwsh.exe" -noprofile -command "Install-Module PSReadLine -Force -SkipPublisherCheck -AllowPrerelease"
```

Баг с `Ctrl + C` исправлен частично. Если открыть PowerShell с русской раскладкой, то вместо `Ctrl + C` всё равно будет появляться буква `с`, но теперь достаточно переключить раскладку на английскую и всё заработает.

## Мой PowerShell profile

Открыть файл настроек PowerShell:
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
 
# Удобный поиск по истории команд с помощью стрелочек
Set-PSReadlineKeyHandler -Key UpArrow -Function HistorySearchBackward
Set-PSReadlineKeyHandler -Key DownArrow -Function HistorySearchForward
```


## Выполнение сценариев отключено в этой системе
```powershell
Set-ExecutionPolicy RemoteSigned
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
