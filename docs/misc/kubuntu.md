# Kubuntu

## Внешний вид KDE Plasma

Настройки актуальны для KDE plasma 6.4.5.

```sh
plasmashell --version
```

Во все пункты настроек можно перейти с помощью KRunner (`alt + space`).

Прозрачность для Application Launcher и Context Menu - `Application Style -> Breeze -> Configure Style... (иконка карандаша) -> Transparancy (~60%)`, `Desktop Effects -> Blur (поставить галочку) -> Configure... (иконка шестерёнки) -> Blur strength ~30% Noise strength = 0`, `ПКМ по панели задач -> Show Panel Configuration -> Opacity -> Translucent`.


Эффекты при переносе окон - `Desktop Effects -> Wobbly Windows`.


Кнопки в верхней панели окон - `Window Decorations -> More Actions (три точки) -> Configure Titlebar Buttons`.

Запускать чистую рабочую сессию без перезапуска незакрытых приложений - `Desktop Session -> Start with an empty session`.

Убрать индикатор проигрывания звука у приложений в панели задач - `ПКМ по панели задач -> Icons-Only Task Manager Settings -> Appearance -> General -> Show an indicator when a task is playing audio`.

Убрать уведомления о переключении раскладки в центре экрана - `Keyboard -> Configure Switching... -> Show ODS popup on layout change`.

Убрать звуки при изменении громкости - `Sound -> Configure Volume controls... -> Play audio feedback for changes to`.

### Системный шрифт

Скачиваем шрифт, например, [Inter](https://fonts.google.com/specimen/Inter), устанавливаем, затем в найстройках `Fonts -> везде, кроме Fixed Width, меняем на Inter`.

### Системные иконки

Скачиваем архив с набором иконок, например, [Tela](https://store.kde.org/p/1279924/), затем в настройках `Icons -> Install from file -> Выбираем скачанный архив`. Теперь в этом же разделе настроект можно выбрать набор иконок Tela.

### Быстрое переключение между тёмной и светлой темой

Чтобы создавать свои темы, нужно установить пакет `plasma-sdk`.

```sh
sudo apt install plasma-sdk
```

Настраиваем тёмную или светлую тему, затем открываем `Plasma Global Theme Explorer -> New Theme... -> во всех полях указываем MyDark или MyLight`. Повторяем для обеих тем. Теперь переключаться между ними можно с помощью команды.

```sh
plasma-apply-lookandfeel -a MyDark
plasma-apply-lookandfeel -a MyLight
```

Можно настроить сочетание клавиш для быстрого переключения между темами. Для этого нужно создать простой скрипт.

=== "Терминал"

    ```sh
    nano ~/kde-scripts/toggle-theme.sh
    chmod +x ~/kde-scripts/toggle-theme.sh
    ```

=== "toggle-theme.sh"

    ```sh
    #!/bin/bash

    CURRENT=$(grep '^LookAndFeelPackage=' ~/.config/kdeglobals | cut -d= -f2)

    if [[ "$CURRENT" == "MyDark" ]]; then
        plasma-apply-lookandfeel -a MyLight
        notify-send "Theme switched" "☀ Light mode enabled"
    else
        plasma-apply-lookandfeel -a MyDark
        notify-send "Theme switched" "🌙 Dark mode enabled"
    fi
    ```

Затем назначить сочетание клавиш для его исполнения в `Shortcuts -> Add New -> Command or Script...` и указать путь к скрипту и сочетание клавиш, например, `meta (win) + alt + t`.

### Настройки Dolphin

В Dolphin можно добавить кнопку "Вверх", `ПКМ по панельке с кнопками -> Configure Toolbars... -> перенести действие Up в правую панель`.

Добавить панель с показом свободного дискового пространства в правом нижнем углу можно через `Application Menu (иконка бургер) -> Settings -> Configure Dolphin -> Status & Location Bars -> Status Bar` поставить галочку `Full Width`. Тут же можно поставить галочку в `Location Bar -> Show full path inside location bar`.

В Dolphin можно переопределять сочетания клавиш для любых действий через меню `Settings -> Configure Keyboard Shortcuts...`. Например, можно переопределить создание папок на `Shift + a`, а создание файлов на `a`.

В контекстное меню Dolphin (открывается при нажатии ПКМ)  можно добавлять новые пункты. Например, `Open With Cursor` для открытия папок в Cursor IDE. Для этого [нужно создать `.desktop` файл в `~/.local/share/kio/servicemenus/`](https://develop.kde.org/docs/apps/dolphin/service-menus/).

=== "Терминал"

    ```sh
    nano ~/.local/share/kio/servicemenus/open-in-cursor.desktop

    chmod +x ~/.local/share/kio/servicemenus/open-in-cursor.desktop
    ```

=== "open-in-cursor.desktop"

    ```ini
    [Desktop Entry]
    Type=Service
    MimeType=inode/directory;
    Actions=OpenInCursor;

    [Desktop Action OpenInCursor]
    Name=Open in Cursor
    Icon=cursor
    Exec=cursor "%f"
    ```

Открывать архивы как папки - `Application Menu (иконка бургер) -> Settings -> Configure Dolphin -> View -> General -> Open archives as folder`.

### Настройки Konsole

Прозрачный фон терминала - `Application Menu (иконка бургер) -> Settings -> Edit current profile -> Appearance -> Edit -> ставим галочку на Blur Background и меняем Background Color Transparancy (~7%)`.

Перед установкой какого-нибудь Oh My Zsh нужно установить шрифты для терминала - `Application Menu (иконка бургер) -> Settings -> Edit current profile -> Appearance -> Choose Font`. Шрифты предварительно нужно скачать и установить.

Можно переопределить `ctrl + v` для вставки текста в терминал - `Application Menu (иконка бургер) -> Settings -> Configure Keyboard Shortcuts...`. Там можно добавить альтернативное сочетание клавиш для действия `paste`.

В настройках VS Code тоже можно переопределить `ctrl + v` для вставки текста в терминал.

```json
[
    {
        "key": "ctrl+v",
        "command": "workbench.action.terminal.paste",
        "when": "terminalFocus"
    }
]
```

### Дополнительные действия при нажатии ПКМ на иконки в панели задач

Например, можно добавить кнопку для быстрого открытия проекта в VS Code или Cursor.

=== "Терминал"

    ```sh
    cp /usr/share/applications/cursor.desktop ~/.local/share/applications/
    nano ~/.local/share/applications/cursor.desktop
    ```

=== "Пример cursor.desktop"

    Действие нужно добавить в поле `Actions`, а затем описать его в отдельной секции.

    ```ini
    [Desktop Entry]
    Name=Cursor
    Comment=The AI Code Editor.
    GenericName=Text Editor
    Exec=/usr/share/cursor/cursor %F
    Icon=co.anysphere.cursor
    Type=Application
    StartupNotify=false
    StartupWMClass=Cursor
    Categories=TextEditor;Development;IDE;
    MimeType=application/x-cursor-workspace;
    Actions=knowledge-base;new-empty-window;edit-actions
    Keywords=cursor;

    [Desktop Action new-empty-window]
    Name=New Empty Window
    Name[ru]=Новое пустое окно
    Exec=/usr/share/cursor/cursor --new-window %F
    Icon=co.anysphere.cursor

    [Desktop Action knowledge-base]
    Name=Open knowledge-base
    Exec=cursor --new-window ~/Main/knowledge-base
    Icon=folder

    [Desktop Action edit-actions]
    Name=Edit Task Manager Actions
    Exec=cursor ~/.local/share/applications/cursor.desktop
    Icon=edit
    ```


## Настройка Oh My Zsh

Установить Zsh и сделать его shell по умолчанию.

```sh
sudo apt install zsh
chsh -s $(which zsh)
```

В настройках терминала нужно выбрать Zsh как основной shell. Также установить любой [Nerd Font](https://www.nerdfonts.com/) (например, Mononoki Nerd Font).

```sh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

Одна из самых популярных тем для Zsh - [powerlevel10k](https://github.com/romkatv/powerlevel10k). После [установки](https://github.com/romkatv/powerlevel10k?tab=readme-ov-file#oh-my-zsh) нужно выполнить команду для интерактивной настройки.

```sh
p10k configure
```

В VS Code также нужно установить Zsh как основной shell и задать правильные шрифты.

```json
{
    "terminal.integrated.defaultProfile.linux": "zsh",
    "terminal.integrated.profiles.linux": {
      "zsh": {
        "path": "/bin/zsh"
      }
    },
    "terminal.integrated.fontFamily": "Mononoki Nerd Font Mono",
    "terminal.integrated.fontSize": 15
}
```

В Oh My Zsh можно установливать плагины на любой вкус и цвет, например: [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting/blob/master/INSTALL.md), [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions).

## Горячие клавиши на русской раскладке в VS Code

Без этой настройки на русской раскладке могут не работать некоторые горячие клавиши в VS Code.

```json
{
    "keyboard.dispatch": "keyCode"
}
```


## Автоматическая отчистка старых файлов в Downloads

=== "Терминал"

    ```sh
    sudo nano /etc/tmpfiles.d/downloads.conf

    # Можно сразу применить и удалить старые файлы
    sudo systemd-tmpfiles --clean
    ```

=== "downloads.conf"

    ```ini
    # Type Path               Mode UID GID Age Argument
    d /home/USERNAME/Downloads 0755 USER USER 7d
    ```

## Настройка zram

[zram-tools](https://packages.debian.org/sid/zram-tools) позволяет оптимизировать использование памяти, сжимая редко используемые данные в RAM.

```sh
sudo apt install zram-tools
reboot

# Проверить, что swap работает
swapon --show
```

По умолчанию под swap выделяется 50% памяти, можно изменить:

```sh
sudo nano /etc/default/zramswap
sudo systemctl restart zramswap
sudo systemctl status zramswap
```

Также при использовании zram рекомендуют уменьшать swappiness. Этот параметр говорит системе, насколько часто ей стоит использовать swap файл.

```sh
echo "vm.swappiness=10" | sudo tee /etc/sysctl.d/99-swappiness.conf
sudo sysctl -p /etc/sysctl.d/99-swappiness.conf

# Проверка
cat /proc/sys/vm/swappiness
```