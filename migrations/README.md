# Database Migrations

Эта папка содержит миграции базы данных для проекта.

## Структура

- `versions/` - папка с файлами миграций (версии схемы БД)

## Использование Alembic

Для работы с миграциями используется [Alembic](https://alembic.sqlalchemy.org/).

### Инициализация (если еще не инициализировано)

```bash
alembic init migrations
```

### Создание новой миграции

```bash
alembic revision --autogenerate -m "Описание изменений"
```

### Применение миграций

```bash
alembic upgrade head
```

### Откат миграции

```bash
alembic downgrade -1
```

### Просмотр текущей версии

```bash
alembic current
```

### Просмотр истории миграций

```bash
alembic history
```

