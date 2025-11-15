# Ellinika Backend

Telegram бот для изучения греческого алфавита.

## Описание

Бот помогает пользователям изучать греческий алфавит, показывая случайные буквы с их названиями, произношением и примерами использования.

## Переменные окружения

Для работы бота необходимо настроить следующие переменные окружения:

### `TELEGRAM_TOKEN` (обязательная)

Токен Telegram бота, полученный от [@BotFather](https://t.me/BotFather).

**Пример:**
```bash
export TELEGRAM_TOKEN="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
```

### Переменные для PostgreSQL 18

Для подключения к базе данных PostgreSQL используются следующие переменные:

- `DB_HOSTNAME` - хост базы данных
- `DB_PORT` - порт базы данных (по умолчанию 5432)
- `DB_DATABASE` - имя базы данных
- `DB_USER` - имя пользователя базы данных
- `DB_PASS` - пароль пользователя базы данных

**Пример:**
```bash
export DB_HOSTNAME="localhost"
export DB_PORT="5432"
export DB_DATABASE="ellinika_db"
export DB_USER="postgres"
export DB_PASS="your_password"
```

## Установка и запуск

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Установите переменные окружения:
```bash
export TELEGRAM_TOKEN="your_token_here"
```

3. Запустите приложение:
```bash
python run.py
```

Или с использованием Gunicorn:
```bash
gunicorn -w 1 app:app
```

## Структура проекта

```
ellinika-backend/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py             # Конфигурация приложения
│   ├── bot/
│   │   ├── data.py           # Данные греческого алфавита
│   │   ├── handlers.py       # Обработчики команд бота
│   │   └── setup.py           # Настройка Telegram бота
│   └── web/
│       └── routes.py         # Flask маршруты (webhook)
├── run.py                    # Точка входа приложения
└── requirements.txt          # Зависимости проекта
```

## Функциональность

- Команда `/start` - приветствие и главное меню
- Команда `/next` - получить случайную букву греческого алфавита
- Кнопки меню:
  - 🔤 Следующая буква - получить новую букву
  - 🏠 В начало - вернуться в главное меню

## Развертывание

Приложение настроено для работы с webhook от Telegram. Убедитесь, что ваш сервер доступен из интернета и правильно настроен webhook URL.

