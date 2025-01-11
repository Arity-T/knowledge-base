# Алиасы команд в Git

## Полезные ссылки
- [Раздел](https://githowto.com/ru/aliases) в GitHowTo

## Мои алиасы
Просто выполнить в терминале:
```sh
git config --global alias.co checkout
git config --global alias.ci commit
git config --global alias.cim "commit -m"
git config --global alias.st status
git config --global alias.br branch
git config --global alias.hist "log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short"
git config --global alias.histt "log --pretty=format:'%h %cd | %s%d [%an]' --graph --date=iso"
git config --global alias.ad "add -A"
```

Пример использования:
```sh
git st # git status
git co main # git checkout main
git cim "Some changes" # git commit -m
```
## Создание алиасов
```sh
git config --global alias.<alias> <command>
```

## Вывести список алиасов
```sh
git config --global --get-regexp alias
```

## Удаление алиасов
[Вопрос](https://stackoverflow.com/a/48110875/17341937) на StatckOverflow 
```sh
git config --global --unset-all alias.your-alias
```