

## SSL-сертификат с certbot

!!! tip "Актуальная версия Python"

    Обычно системый `Python` достаточно старый. Для установки `certbot` может потребоваться более новая версия. Минимальные требования можно узнать на [pypi](https://pypi.org/project/certbot/).

    ```sh
    sudo apt update
    sudo add-apt-repository ppa:deadsnakes/ppa

    # Вместо 3.1x нужно указать актуальную версию Python
    sudo apt install python3.1x python3.1x-venv 
    ```

    Теперь вместо `python3` можно использовать `python3.1x`.

SSL-сертификат получается и устанавливается с помощью [certbot](https://github.com/certbot/certbot). На их сайте есть подробная пошаговая [инструкция](https://certbot.eff.org/instructions?ws=nginx&os=pip) о том, как правильно его установить, получить сертификаты и включить их автообновление.

??? note "Установка вкратце"

    ```sh { .code-wrap }
    # Установили certbot в venv
    # Вместо 3.1x нужно указать актуальную версию Python
    sudo python3.x -m venv /opt/certbot/
    sudo /opt/certbot/bin/pip install --upgrade pip
    sudo /opt/certbot/bin/pip install certbot certbot-nginx

    # Добавили в PATH
    sudo ln -s /opt/certbot/bin/certbot /usr/bin/certbot

    # Автообновление сертификатов
    echo "0 0,12 * * * root /opt/certbot/bin/python -c 'import random; import time; time.sleep(random.random() * 3600)' && sudo certbot renew -q" | sudo tee -a /etc/crontab > /dev/null
    ```


Несколько полезных команд.

```sh
# Получить сертификат для определённого домена. Предварительно нужно 
# настроить конфиг nginx для этого домена.
sudo certbot --nginx -d example.com -d www.example.com

# Список сертификатов со сроками их жизни
sudo certbot certificates

# Удалить сертификат (команда предложит выбор)
sudo certbot delete
```