
## Запуск Prometheus с помощью systemd

Ссылку на последнюю версию `Prometheus` можно найти на [странице загрузок](https://prometheus.io/download/).

```sh
# Скачиваем и распаковываем релиз
wget <link>
tar xvf prometheus-*.*-amd64.tar.gz
cd prometheus-*.*

# Создаём отдельного пользователя и группу для запуска prometheus
sudo adduser --system --no-create-home --group prometheus

# Конфиг
sudo mkdir /etc/prometheus
sudo cp prometheus.yml /etc/prometheus/
sudo chown -R prometheus:prometheus /etc/prometheus

# Папка для данных
sudo mkdir /var/lib/prometheus
sudo chown -R prometheus:prometheus /var/lib/prometheus

# Бинарники prometheus и promtool
sudo cp prometheus /usr/local/bin/ 
sudo chown prometheus:prometheus /usr/local/bin/prometheus
sudo cp promtool /usr/local/bin/
sudo chown prometheus:prometheus /usr/local/bin/promtool
```

Создаём `systemd` сервис. Список возможных параметров запуска `Prometheus` представлен в [документации](https://prometheus.io/docs/prometheus/latest/command-line/prometheus/). 


=== "Терминал"
    ```sh
    sudo nano /etc/systemd/system/prometheus.service
    ```

=== "prometheus.service"

    ```ini
    [Unit]
    Description=Prometheus Server
    After=network-online.target

    [Service]
    User=prometheus
    Group=prometheus
    Restart=on-failure
    ExecStart=/usr/local/bin/prometheus \
        --config.file=/etc/prometheus/prometheus.yml \
        --storage.tsdb.path=/var/lib/prometheus

    [Install]
    WantedBy=multi-user.target
    ```

Добавляем `Prometheus` в автозагрузку и запускаем. 

```sh
sudo systemctl daemon-reload
sudo systemctl enable prometheus
sudo systemctl start prometheus
sudo systemctl status prometheus
```

При обновлении конфига, нужно будет перезапустить сервис.

```sh
sudo systemctl restart prometheus
```


## Node Exporter

Устанавливаем `Node Exporter` по инструкции из [документации](https://prometheus.io/docs/guides/node-exporter/). Сервис в `systemd` для `Node Exporter` будет создан автоматически.

```sh
sudo systemctl status node_exporter.service
```

[Пример](https://grafana.com/grafana/dashboards/1860-node-exporter-full/) дашборда `Grafana` для `Node Exporter`.