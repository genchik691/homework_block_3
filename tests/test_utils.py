import pytest
import json
import tempfile
from pathlib import Path
from src.classes import Product, Category
from src.utils import load_categories_from_json


class TestUtils:
    """Тесты для утилит загрузки данных"""

    def test_load_categories_from_json_success(self):
        """Тест успешной загрузки категорий из JSON"""
        # Создаем временный JSON файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json_data = [
                {
                    "name": "Электроника",
                    "description": "Различные электронные устройства",
                    "products": [
                        {
                            "name": "Смартфон",
                            "description": "Современный смартфон",
                            "price": 25000.50,
                            "quantity": 50
                        },
                        {
                            "name": "Наушники",
                            "description": "Беспроводные наушники",
                            "price": 3500.00,
                            "quantity": 100
                        }
                    ]
                },
                {
                    "name": "Аксессуары",
                    "description": "Аксессуары для устройств",
                    "products": [
                        {
                            "name": "Чехол",
                            "description": "Защитный чехол",
                            "price": 500.00,
                            "quantity": 200
                        }
                    ]
                }
            ]
            json.dump(json_data, f, ensure_ascii=False, indent=2)
            temp_file = f.name

        try:
            # Загружаем категории
            categories = load_categories_from_json(temp_file)

            # Проверяем результат
            assert len(categories) == 2
            assert categories[0].name == "Электроника"
            assert categories[0].description == "Различные электронные устройства"
            assert len(categories[0].get_products_list()) == 2

            assert categories[1].name == "Аксессуары"
            assert categories[1].description == "Аксессуары для устройств"
            assert len(categories[1].get_products_list()) == 1

            # Проверяем продукты
            products = categories[0].get_products_list()
            assert products[0].name == "Смартфон"
            assert products[0].price == 25000.50
            assert products[0].quantity == 50

            assert products[1].name == "Наушники"
            assert products[1].price == 3500.00
            assert products[1].quantity == 100

        finally:
            # Удаляем временный файл
            Path(temp_file).unlink()

    def test_load_categories_from_json_empty(self):
        """Тест загрузки пустого JSON файла"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump([], f)
            temp_file = f.name

        try:
            categories = load_categories_from_json(temp_file)
            assert categories == []
        finally:
            Path(temp_file).unlink()

    def test_load_categories_from_json_file_not_found(self, capsys):
        """Тест загрузки из несуществующего файла"""
        categories = load_categories_from_json("non_existent_file.json")
        assert categories == []

        captured = capsys.readouterr()
        assert "Файл non_existent_file.json не найден" in captured.out

    def test_load_categories_from_json_invalid_json(self, capsys):
        """Тест загрузки из некорректного JSON файла"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            f.write("this is not valid json")
            temp_file = f.name

        try:
            categories = load_categories_from_json(temp_file)
            assert categories == []

            captured = capsys.readouterr()
            assert "Ошибка декодирования JSON" in captured.out
        finally:
            Path(temp_file).unlink()

    def test_load_categories_from_json_missing_fields(self):
        """Тест загрузки JSON с отсутствующими полями"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json_data = [
                {
                    "name": "Категория без товаров"
                    # Отсутствует description и products
                }
            ]
            json.dump(json_data, f)
            temp_file = f.name

        try:
            categories = load_categories_from_json(temp_file)

            assert len(categories) == 1
            assert categories[0].name == "Категория без товаров"
            assert categories[0].description == ""  # Значение по умолчанию
            assert categories[0].get_products_list() == []  # Пустой список по умолчанию
        finally:
            Path(temp_file).unlink()

    def test_load_categories_from_json_with_smartphone(self):
        """Тест загрузки категории со смартфонами"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json_data = [
                {
                    "name": "Смартфоны",
                    "description": "Флагманские смартфоны",
                    "products": [
                        {
                            "name": "iPhone 15",
                            "description": "Флагманский смартфон",
                            "price": 99999.99,
                            "quantity": 10
                        }
                    ]
                }
            ]
            json.dump(json_data, f)
            temp_file = f.name

        try:
            categories = load_categories_from_json(temp_file)
            assert len(categories) == 1
            assert categories[0].name == "Смартфоны"
            assert len(categories[0].get_products_list()) == 1

            product = categories[0].get_products_list()[0]
            assert product.name == "iPhone 15"
            assert product.price == 99999.99
            assert product.quantity == 10
        finally:
            Path(temp_file).unlink()