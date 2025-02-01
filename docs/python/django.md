## Отслеживание SQL запросов

```python
from django.db import connection, reset_queries

# Сбрасываем счетчик запросов
reset_queries()

# Код, который работает с БД

# Теперь выводим все запросы, которые были зафиксированы
for query in connection.queries:
	print(query)
```
