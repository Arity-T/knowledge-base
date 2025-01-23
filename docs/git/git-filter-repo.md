# git-filter-repo

С помощью [git-filter-repo](https://github.com/newren/git-filter-repo/) можно переписать историю репозитория.

## Установка

Глобально или в `virtualenv`

```sh
pip install git-filter-repo
```

## Замена метаданных коммитов

`git-filter-repo` позволяет создать скрипт на `Python`, который будет вызван для всех коммитов репозитория. Доступ к данным коммита, с возможностю их редактирования, предоставляется через объект `commit`. Таким образом можно описать любую логику изменения метаданных коммитов на обычном `Python`.

Ниже представлен пример изменения метаданных коммита по его хэшу. Узнать хэш коммита можно с помощью, например, `git log`.

=== "Command"

    ```sh
    git filter-repo --force --commit-callback "callback.py"
    ```

=== "callback.py"

    ```python
    """Файл создан для использования с git-filter-repo.

    Пример команды:
    git filter-repo --force --commit-callback "callback.py"
    """

    from datetime import datetime, timedelta, timezone


    def git_timestamp(date_str: str, tz_offset: int = 3) -> bytes:
        """
        Преобразует строку с датой в формат временной метки для git-filter-repo.

        Args:
            date_str (str): Дата в формате "DD.MM.YYYY HH:MM:SS".
            tz_offset (int, optional): Сдвиг временной зоны относительно UTC.
                По умолчанию 3 (московское время).

        Returns:
            bytes: Байтовая строка с временной меткой и сдвигом временной зоны
                в формате `b"{timestamp} {timezone_offset}"`.
        """
        tz = timezone(timedelta(hours=tz_offset))
        dt = datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S").replace(tzinfo=tz)

        timestamp = int(dt.timestamp())
        timezone_offset = f"{tz_offset:+03d}00"

        return f"{timestamp} {timezone_offset}".encode("utf-8")


    # Обязательно нужно указывать полный хэш коммита
    if commit.original_id == b"72f6afa37aac4cdbf8d37f22470b77c221a8fce0":
        # Сообщение коммита
        commit.message = "Новое сообщение коммита!".encode("utf-8")

        new_name = "Иван Иванов".encode("utf-8")
        new_email = "ivan-ivanov@mail.com".encode("utf-8")
        new_date = git_timestamp("01.01.2000 10:00:00")

        # Автор изменений
        commit.author_name = new_name
        commit.author_email = new_email

        # Автор коммита
        commit.committer_name = new_name
        commit.committer_email = new_email

        # Дата изменений и дата коммита
        commit.author_date = new_date
        commit.committer_date = new_date
    ```

## Полезные ссылки

 - [git-filter-repo](https://github.com/newren/git-filter-repo/?tab=readme-ov-file#simple-example-with-comparisons) on GitHub
 - [usage examples](https://www.mankier.com/1/git-filter-repo)