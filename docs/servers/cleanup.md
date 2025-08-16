# Очистка места на сервере

## Полезные команды

```sh
# Проверить место во всех разделах
df -h

# Размер файла/папки
du -sh <path>

# Показать самые большие директории в корне
sudo du -h -d1 / | sort -hr

# В домашнем каталоге
du -h -d1 ~ | sort -hr

# Показать файлы больше 100MB
find . -type f -size +100M -exec ls -lh {} \; | awk '{print $5, $9}' | sort -hr
```

## Логи `journalctl`

```sh
# Посмотреть сколько занимают логи журнала
sudo journalctl --disk-usage

# Оставить только 100MB самых актуальных логов
sudo journalctl --rotate
sudo journalctl --vacuum-size=100M

# Можно задать параметры SystemMaxUse и RuntimeMaxUse
# Вместо MB надо использовать M
sudo nano /etc/systemd/journald.conf

# Применить изменения в конфиге
sudo systemctl restart systemd-journald
```

## Другие логи

```sh
# Посмотреть сколько места занимают логи
sudo du -h -d1 /var/log | sort -hr

# Очищать файлы с логами лучше командой, чтобы процессы могли
# дальше писать логи в этим файлы
sudo truncate -s 0
```

## Кэш пакетов

```sh
sudo apt-get clean
sudo apt-get autoremove --purge
```

## Docker

```sh
# Посмотреть сколько место занимает докер
docker system df
# Показать детализацию по образам, контейнерам, волюмам
docker system df -v

# Удалить все нетегированные образы, остановленные контейнеры,
# неиспользуемые сети, кэш сборки
docker system prune

# Очистит также все образы, с которыми не связан ни один контейнер
docker system prune -a

# Удалить волюмы, с которыми не связан ни один контейнер
docker volume prune
```