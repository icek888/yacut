# YaCut

**YaCut** — это удобный сервис укорачивания ссылок. Его главная задача — сокращать длинные URL-адреса до коротких, удобных для использования, хранения и обмена.

[**Ссылка на репозиторий**](https://github.com/icek888/yacut)

---

## Основные возможности

- Генерация коротких ссылок для длинных URL-адресов.
- Возможность указать пользовательский вариант короткой ссылки (до 16 символов).
- Переадресация на оригинальный адрес по короткой ссылке.
- API для автоматизации создания и получения ссылок.

---

## Установка и запуск проекта

### 1. Клонирование репозитория

```bash
git clone https://github.com/icek888/yacut.git
cd yacut
```

### 2. Создание и активация виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Для Linux/macOS
venv\Scripts\activate     # Для Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Создайте файл `.env` в корне проекта и добавьте туда следующие параметры:

```plaintext
FLASK_APP=yacut
FLASK_ENV=development
DATABASE_URI=sqlite:///yacut.db
```

### 5. Инициализация базы данных

```bash
flask db init
flask db migrate
flask db upgrade
```

### 6. Запуск приложения

```bash
flask run
```

Приложение будет доступно по адресу: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## Работа с API

YaCut предоставляет простой API для создания и получения ссылок.

### 1. Создание короткой ссылки

**Ендпоинт:** `/api/id/`

**Метод:** `POST`

**Тело запроса:**
```json
{
  "original_link": "https://example.com/very/long/url",
  "custom_id": "short123"  // Необязательно
}
```

**Ответ:**
- Успех (201):
  ```json
  {
    "short_link": "http://127.0.0.1:5000/short123",
    "original_link": "https://example.com/very/long/url"
  }
  ```
- Ошибка (400):
  ```json
  {
    "message": "Custom ID already exists."
  }
  ```

### 2. Получение оригинальной ссылки

**Ендпоинт:** `/api/id/<short_id>/`

**Метод:** `GET`

**Ответ:**
- Успех (200):
  ```json
  {
    "original_link": "https://example.com/very/long/url"
  }
  ```
- Ошибка (404):
  ```json
  {
    "message": "Short ID not found."
  }
  ```

---

## Тестирование проекта

Для проверки функциональности проекта выполните команду:

```bash
pytest
```

Тесты находятся в директории `tests/`.

---

## Технологии

- **Python 3.10+**
- **Flask** — легковесный веб-фреймворк.
- **SQLAlchemy** — ORM для работы с базой данных.
- **SQLite** — база данных по умолчанию (на этапе разработки).

---

## Автор

[**Icek888**](https://github.com/icek888)  