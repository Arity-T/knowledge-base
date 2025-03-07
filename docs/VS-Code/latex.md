# LaTeX в VS Code

## Подготовка

Вся работа с LaTeX в VS Code завязана на расширении [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop). Вот [документация](https://github.com/James-Yu/LaTeX-Workshop/wiki/Install) по установке. Вкратце:

1. Устанавливаем [Perl](https://strawberryperl.com/)
2. Устанавливаем [MikTeX](https://miktex.org/)
3. Устанавливаем [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop)

После установки можно открыть любой `.tex` файл и попробовать скомпилировать его (`ctrl + alt + b`), а затем открыть предпросмотр (`ctrl + alt + v`). При сохранении файл будет автоматически компилироваться, а предпросмотр обновляться.

## Сниппеты

### Создание
В LaTeX очень много повторяющихся конструкций, грех не использовать сниппеты. Нажимаем `ctrl + shift + p` (или `f1`), ищем пункт `Snippets: Configure Snippets`, затем ищем `latex`. Автоматически будет создан файл `latex.json`, в который можно добавлять сниппеты.

### Использование

Примеры [сниппетов](attachments/latex.json), которые я использую.

- `\img` - для вставки картинок.
- `\lst` или `\listing` - для вставки листингов.
- `\tablex` и `\table` - для вставки таблиц.
- `\pdf` - для вставки PDF файлов.

## Примечание

- Работать с текстом в VS Code намного удобнее, в первую очередь за счёт [горячих клавиш](hotkeys.md). В особенности полезно сочетание `alt + z`, с помощью которого включается автоматический перенос строк.
- При написании отчётов, которые обычно обрастают множеством правок, полезно использовать `Git`. `MikTex` создаёт много временных файлов, которые в `Git` добавлять не нужно, поэтому ниже представлена заготовка для `.gitignore`.
```sh title=".gitignore"
# Игнорировать всё,
**/*
# кроме
!.gitignore
!report.tex
!img
!img/*
```