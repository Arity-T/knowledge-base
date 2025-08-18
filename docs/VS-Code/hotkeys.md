# Горячие клавиши VS Code

Горячие клавиши можно посмотреть и настроить в разделе `Kyeboard Shortcuts`. Открыть его можно сочетанием клавиш `ctrl + k ctrl + s`, либо через панель команд - `F1` или `ctrl + shift + p` и ввести `Keyboard Shortcuts`.

****

![Сочетания клавиш VS Code](attachments/vscode-keyboard-shortcuts.png)
/// caption
Зелёным отмечены самые часто используемые комбинации, синим - более редкие, но тоже полезные. [PDF](attachments/vscode-keyboard-shortcuts.pdf){ target="_blank"}. [Source](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-windows.pdf){ target="_blank"}.
///

!!! tip

    `ctrl + shift + p` - главное сочетание клавиш, которое стоит запомнить.

    `alt + 1/2/3/...` - переключение между открытыми вкладками в порядке их расположения.

    Удалить множественные курсоры можно с помощью `Esc`.

    Если с помощью `ctrl + d` выделили лишнее, то сочетанием `ctrl + u` можно убрать последнее выделение.

    `ctrl + alt + ←/→` - перенести файл в левую/правую группу вкладок.

    `alt + z` - крайне полезно при работе с Latex, Markdown и другими "широкими" файлами.

    `ctrl + j` - скрыть/показать нижнюю панель (терминал, логи и т.д.).

    `alt + shift + r` - показать файл, выбранный в левой панели с файлами, в проводнике.

    `ctrl + shift + .` - breadcrumbs

## Кастомные сочетания клавиш

Сочетания клавиш для быстрого создания папок и файлов через проводник внутри VS Code.

- `a` - создать файл.
- `shift + a` - создать папку.

Быстрый переход к определению и типу функции, метода, переменной, etc. В дополнение к `F12`. Удобно использовать вместе с `alt + ←/→`.

- `alt + d` - перейти к определению.
- `alt + t` - перейти к определению типа.

Обычно я отключаю `explorer.autoReveal` в настройках, чтобы боковая панель с проводником не изменялась, когда я переключаюсь по файлам. Если мне всё-таки требуется выделить открытый файл в `Explorer View`, то я использую дополнительное сочетание клавиш.

- `alt + shift + r` - показать открытый файл в `Explorer View`.

```json
[
    {
        "key": "a",
        "command": "explorer.newFile",
        "when": "filesExplorerFocus && !inputFocus"
    },
    {
        "key": "shift+a",
        "command": "explorer.newFolder",
        "when": "filesExplorerFocus && !inputFocus"
    },
    {
        "key": "alt+d",
        "command": "editor.action.revealDefinition",
        "when": "editorHasDefinitionProvider && editorTextFocus"
    },
    {
        "key": "alt+t",
        "command": "editor.action.goToTypeDefinition",
        "when": "editorTextFocus"
    },
    {
        "key": "shift+alt+r",
        "command": "workbench.files.action.showActiveFileInExplorer",
        "when": "editorTextFocus"
    }
]
```