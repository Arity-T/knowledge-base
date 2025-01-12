# Termux

[termux](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://termux.dev/en/&ved=2ahUKEwiwtP-i8-6KAxUmCRAIHdzFLIMQFnoECBcQAQ&usg=AOvVaw3QQbzyEPPj93rvMGGQkfpC) - бесплатный эмулятор терминала Linux для Android.

## Установка

Скачать последнюю версию можно с [GitHub](https://github.com/termux/termux-app/releases). Впрочем версия с [Play Market](https://play.google.com/store/apps/details?id=com.termux) тоже работает исправно.

После установки нужно открыть приложение и выполнить команду для получения доступа к файлам устройства 
```sh
termux-setup-storage
```
В появившемся окне настроек нужно будет предоставить приложению Termux доступ ко всем файлам устройства.

После этого файлы устройства будут доступны по пути `~/storage/shared`.

```sh
cd ~/storage/shared
ls
```
