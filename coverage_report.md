# Отчет о покрытии тестами

## Общая информация
- **Дата:** 26.06.2026
- **Инструмент:** pytest-cov 7.1.0
- **Общее покрытие:** 90%

## Детальный отчет

### Покрытие модулей

| Модуль | Строки | Покрыто | Пропущено | Покрытие |
|--------|--------|---------|-----------|----------|
| src/__init__.py | 0 | 0 | 0 | 100% |
| src/classes.py | 137 | 119 | 18 | 87% |
| src/iterators.py | 15 | 15 | 0 | 100% |
| src/utils.py | 20 | 20 | 0 | 100% |
| **Итого** | **172** | **154** | **18** | **90%** |

### Покрытие классов

#### Product (87%)
- `__init__` - 100% (включая проверку исключений)
- `price` (property) - 100%
- `price.setter` - 100%
- `new_product` - 100%
- `__str__` - 100%
- `__repr__` - 100%
- `__add__` - 100%

#### Smartphone (100%)
- `__init__` - 100%
- `__repr__` - 100%

#### LawnGrass (100%)
- `__init__` - 100%
- `__repr__` - 100%

#### Category (100%)
- `__init__` - 100%
- `products` (property) - 100%
- `total_quantity` (property) - 100%
- `average_price` - 100%
- `add_product` - 100%
- `get_products_list` - 100%
- `__str__` - 100%
- `__repr__` - 100%

#### LoggingMixin (100%)
- `__init__` - 100%
- `__repr__` - 100%

#### BaseProduct (100%)
- Все абстрактные методы - 100%

#### Order (100%)
- `__init__` - 100%
- `total_price` - 100%
- `price` - 100%
- `price.setter` - 100%
- `__str__` - 100%
- `__add__` - 100%

#### Utils (100%)
- `load_categories_from_json` - 100% (включая обработку ошибок)

### Результаты тестов
- **Всего тестов:** 47
- **Пройдено:** 47 (100%)
- **Провалено:** 0 (0%)
- **Покрытие:** 90%

### Команды для запуска

```bash
# Запуск тестов с отчетом
poetry run pytest --cov=src --cov-report=term

# Запуск с HTML отчетом
poetry run pytest --cov=src --cov-report=html

# Открыть HTML отчет
start htmlcov/index.html  # Windows
open htmlcov/index.html   # macOS/Linux