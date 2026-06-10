# homework_block_3
# E-commerce Core

## Описание

Базовая реализация классов для e-commerce системы, включающая работу с категориями и продуктами.

# Структура проекта

```
homework_block_3/
├── src/
│   ├── __init__.py
│   ├── classes.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_classes.py
├── data/
│   └── products.json
├── main.py
├── pyproject.toml
├── README.md
└── .flake8
└── .gitignore
```
## Функциональность

- Класс `Product` для представления товаров с атрибутами: название, описание, цена, количество
- Класс `Category` для управления категориями товаров
- Автоматический подсчет количества категорий и товаров через атрибуты класса
- Загрузка данных из JSON файлов
- Полное покрытие тестами (>75%)

## Установка и запуск

```bash
# Клонирование репозитория
git clone <repository-url>

# Установка зависимостей через poetry
poetry install

# Запуск тестов
poetry run pytest

# Запуск основного скрипта
poetry run python main.py
Покрытие тестами
Для просмотра отчета о покрытии выполните:

bash
poetry run pytest --cov=src --cov-report=html
```