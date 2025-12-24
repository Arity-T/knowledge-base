# LaTeX

## LaTeX в VS Code

### Подготовка

Вся работа с LaTeX в VS Code завязана на расширении [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop). Вот [документация](https://github.com/James-Yu/LaTeX-Workshop/wiki/Install) по установке. Вкратце:

1. Устанавливаем [Perl](https://strawberryperl.com/)
2. Устанавливаем [MikTeX](https://miktex.org/)
3. Устанавливаем [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop)

После установки можно открыть любой `.tex` файл и попробовать скомпилировать его (`ctrl + alt + b`), а затем открыть предпросмотр (`ctrl + alt + v`). При сохранении файл будет автоматически компилироваться, а предпросмотр обновляться.

### Сниппеты

#### Создание
В LaTeX очень много повторяющихся конструкций, грех не использовать сниппеты. Нажимаем `ctrl + shift + p` (или `f1`), ищем пункт `Snippets: Configure Snippets`, затем ищем `latex`. Автоматически будет создан файл `latex.json`, в который можно добавлять сниппеты.

#### Использование

Примеры [сниппетов](attachments/latex.json), которые я использую.

- `\img` - для вставки картинок.
- `\lst` или `\listing` - для вставки листингов.
- `\tablex` и `\table` - для вставки таблиц.
- `\pdf` - для вставки PDF файлов.

### Примечание

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

## Цитирование по ГОСТу с Biblatex-GOST

Пакет [Biblatex-GOST](https://ctan.org/pkg/biblatex-gost) автоматически формирует список литературы по ГОСТу и при этом, позволяет использовать привычное для LaTeX цитирование с помощью команды `\cite`. У пакета есть [документация](https://mirror.macomnet.net/pub/CTAN/macros/latex/contrib/biblatex-contrib/biblatex-gost/doc/biblatex-gost.pdf) и [GitHub репозиторий](https://github.com/odomanov/biblatex-gost/). MikTex автоматически установит пакет при первом использовании.

=== "LaTeX"

    ```latex
    \documentclass[a4paper,12pt]{article}

    \usepackage[T2A]{fontenc}
    \usepackage[utf8]{inputenc}
    \usepackage[russian]{babel}

    % Рекомендуется для biblatex (кавычки/локализация цитат и т.п.)
    \usepackage{csquotes}

    % ГОСТ-стили для biblatex
    \usepackage[
      backend=biber,
      bibstyle=gost-numeric, % ссылки вида: [1]
      citestyle=gost-numeric,
      sorting=none % порядок в списке = по первому цитированию
    ]{biblatex}

    % Все источники хранятся в отдельном файле
    \addbibresource{refs.bib}

    \begin{document}

    Цитируем как обычно, например: \cite{whisper}.

    Также при цитировании можно указывать страницу 
    или раздел, например: \cite[с. 10]{whisper}.

    Сайты и статьи в интернете можно цитировать так: \cite{overleaf}.

    % Выводим список литературы
    \printbibliography

    \end{document}
    ```

=== "refs.bib"

    Код `bibtex` обычно генерируется автоматически на сайтах с научными статьями. Например, на Arxiv по нажатию кнопки `Export BibTeX Citation`, на ScienceDirect - `Cite -> Export citation to BibTeX`.

    ```bibtex
    @misc{whisper,
      title={Robust Speech Recognition via Large-Scale Weak Supervision}, 
      author={Alec Radford and Jong Wook Kim and Tao Xu and 
        Greg Brockman and Christine McLeavey and Ilya Sutskever},
      year={2022},
      eprint={2212.04356},
      archivePrefix={arXiv},
      primaryClass={eess.AS},
      url={https://arxiv.org/abs/2212.04356}, 
    }
    @online{overleaf,
      title   = {Bibliography management with biblatex},
      author  = {{Overleaf}},
      url     = {https://www.overleaf.com/learn/latex/Bibliography_management_with_biblatex},
      urldate = {2025-12-24},
    }
    ```