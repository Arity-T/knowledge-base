# Termux

[Termux](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://termux.dev/en/&ved=2ahUKEwiwtP-i8-6KAxUmCRAIHdzFLIMQFnoECBcQAQ&usg=AOvVaw3QQbzyEPPj93rvMGGQkfpC) - бесплатный эмулятор терминала Linux для Android.

## Установка

Скачать последнюю версию можно с [GitHub](https://github.com/termux/termux-app/releases). Впрочем версия с [Play Market](https://play.google.com/store/apps/details?id=com.termux) тоже работает исправно.

После установки нужно открыть приложение и выполнить команду для получения [доступа к файлам устройства](https://android.stackexchange.com/a/185949).
```sh
termux-setup-storage
```
В появившемся окне настроек нужно будет предоставить приложению Termux доступ ко всем файлам устройства.

После этого файлы устройства будут доступны по пути `~/storage/shared`. Проверить, что доступ к файлам получен, а заодно перейти в эту папку можно с помощью команд:

```sh
cd ~/storage/shared
ls
```

!!! tip

    Команда `termux-setup-storage` однократно создаёт символические ссылки на все папки, расположенные в `/storage/emulated/0`, и помещает их в `~/storage/shared`. Это означает, что если в корневом каталоге `/storage/emulated/0` будут созданы новые папки, для доступа к ним потребуется повторно выполнить команду `termux-setup-storage`.

Также стоит обновить все пакеты перед началом работы.

```sh
pkg upgrade
```

!!! info

    `pkg` это просто удобная обёртка над `apt`, который тоже доступен в Termux. Команда `pkg upgrade` эквивалентна `apt update && apt upgrade`.

## Установка и настройка Git

Как и любые другие пакеты, `Git` устанавливается с помощью команды `pkg`.

```sh
pkg install git
```

Дальше базовая настройка имени пользователя и почты

```sh
git config --global user.name "name"
```
```sh
git config --global user.email "email"
```

Нужно отключить проверку прав на файлы в репозиториях. Это [особенность](https://stackoverflow.com/a/77628879) работы с `Git` через `Termux`.

```sh
git config --global safe.directory '*'
```

Также можно установить `OpenSSH` и сгенерировать SSH ключ.

```sh
pkg install openssh
ssh-keygen
cat ~/.ssh/id_ed25519.pub
```

Осталось разве что настроить [алиасы](../git/aliases.md) и можно полноценно использовать `Git` на телефоне!