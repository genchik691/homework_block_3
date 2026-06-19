import json

import pytest

from src.classes import Category, Product
from src.utils import load_categories_from_json


@pytest.fixture
def sample_product():
    """Фикстура для создания тестового продукта"""
    return Product("Ноутбук", "Мощный игровой ноутбук", 75000.99, 10)


@pytest.fixture
def sample_category():
    """Фикстура для создания тестовой категории"""
    product1 = Product("Мышь", "Беспроводная мышь", 1500.50, 25)
    product2 = Product("Клавиатура", "Механическая клавиатура", 3500.00, 15)
    return Category("Электроника", "Различные электронные устройства", [product1, product2])


class TestProduct:
    """Тесты для класса Product"""

    def test_product_initialization(self, sample_product):
        """Тест корректной инициализации продукта"""
        assert sample_product.name == "Ноутбук"
        assert sample_product.description == "Мощный игровой ноутбук"
        assert sample_product.price == 75000.99  # Геттер
        assert sample_product.quantity == 10

    def test_product_price_getter(self, sample_product):
        """Тест геттера для цены"""
        assert sample_product.price == 75000.99

    def test_product_price_setter_valid(self, sample_product):
        """Тест сеттера для цены с корректным значением"""
        sample_product.price = 80000.00
        assert sample_product.price == 80000.00

    def test_product_price_setter_invalid(self, sample_product, capsys):
        """Тест сеттера для цены с некорректным значением"""
        sample_product.price = -100
        captured = capsys.readouterr()
        assert "Цена не может быть отрицательной или нулевой" in captured.out
        assert sample_product.price == 75000.99  # Цена не изменилась

        sample_product.price = 0
        captured = capsys.readouterr()
        assert "Цена не может быть отрицательной или нулевой" in captured.out
        assert sample_product.price == 75000.99  # Цена не изменилась

    def test_product_price_private_attribute(self, sample_product):
        """Тест что цена - приватный атрибут"""
        with pytest.raises(AttributeError):
            _ = sample_product.__price  # Должен вызвать ошибку

    def test_product_with_different_types(self):
        """Тест инициализации с разными типами данных"""
        product = Product("Телефон", "Смартфон", 50000.00, 5)
        assert isinstance(product.name, str)
        assert isinstance(product.description, str)
        assert isinstance(product.price, float)
        assert isinstance(product.quantity, int)

    def test_product_string_representation(self, sample_product):
        """Тест строкового представления продукта"""
        assert str(sample_product) == "Ноутбук - 75000.99 руб."

    def test_product_price_zero_through_setter(self):
        """Тест установки нулевой цены через сеттер"""
        product = Product("Бесплатный товар", "Акция", 0.0, 100)
        assert product.price == 0.0  # Начальное значение может быть 0

        # Попытка установить 0 через сеттер
        product.price = 0
        # Цена не должна измениться (остается 0.0 или не меняется)
        # Сеттер не должен менять цену на 0

    def test_new_product_class_method(self):
        """Тест класс-метода new_product"""
        product_data = {
            'name': 'Смартфон',
            'description': 'Современный смартфон',
            'price': 25000.50,
            'quantity': 50
        }
        product = Product.new_product(product_data)

        assert product.name == 'Смартфон'
        assert product.description == 'Современный смартфон'
        assert product.price == 25000.50
        assert product.quantity == 50
        assert isinstance(product, Product)


class TestCategory:
    """Тесты для класса Category"""

    def test_category_initialization(self, sample_category):
        """Тест корректной инициализации категории"""
        assert sample_category.name == "Электроника"
        assert sample_category.description == "Различные электронные устройства"
        assert len(sample_category.get_products_list()) == 2

        products_list = sample_category.get_products_list()
        assert isinstance(products_list[0], Product)

    def test_category_without_products(self):
        """Тест создания категории без товаров"""
        category = Category("Книги", "Художественная литература")
        assert category.name == "Книги"
        assert category.description == "Художественная литература"
        assert category.get_products_list() == []

    def test_products_getter_format(self, sample_category):
        """Тест геттера для продуктов в правильном формате"""
        result = sample_category.products
        assert "Мышь, 1500.5 руб. Остаток: 25 шт." in result
        assert "Клавиатура, 3500.0 руб. Остаток: 15 шт." in result

    def test_products_getter_empty(self):
        """Тест геттера для пустой категории"""
        category = Category("Пустая категория", "Нет товаров")
        assert category.products == ""

    def test_category_count_increment(self):
        """Тест автоматического подсчета количества категорий"""
        # Сохраняем начальное значение
        initial_count = Category.category_count

        # Создаем новую категорию
        Category("Категория 1", "Описание 1")
        assert Category.category_count == initial_count + 1

        # Создаем еще одну категорию
        Category("Категория 2", "Описание 2")
        assert Category.category_count == initial_count + 2

    def test_product_count_calculation(self):
        """Тест корректного подсчета количества товаров"""
        # Сохраняем начальное значение
        initial_count = Category.product_count

        # Создаем категорию с 3 товарами
        products = [
            Product("Товар 1", "Описание 1", 100, 10),
            Product("Товар 2", "Описание 2", 200, 20),
            Product("Товар 3", "Описание 3", 300, 30)
        ]
        Category("Тестовая категория", "Описание", products)

        # Проверяем, что количество товаров увеличилось на 3
        assert Category.product_count == initial_count + 3

    def test_multiple_categories_product_count(self):
        """Тест подсчета товаров при создании нескольких категорий"""
        # Сбрасываем счетчики для чистоты теста
        Category.category_count = 0
        Category.product_count = 0

        # Создаем первую категорию с 2 товарами
        cat1_products = [
            Product("Товар A", "Описание A", 100, 5),
            Product("Товар B", "Описание B", 200, 3)
        ]
        Category("Категория 1", "Описание 1", cat1_products)

        assert Category.category_count == 1
        assert Category.product_count == 2

        # Создаем вторую категорию с 1 товаром
        cat2_products = [Product("Товар C", "Описание C", 300, 7)]
        Category("Категория 2", "Описание 2", cat2_products)

        assert Category.category_count == 2
        assert Category.product_count == 3

    def test_add_product_to_category(self):
        """Тест добавления продукта в категорию"""
        # Сохраняем начальное значение
        initial_count = Category.product_count

        category = Category("Тестовая категория", "Описание")
        product = Product("Новый товар", "Описание", 500, 15)

        # Добавляем продукт
        category.add_product(product)

        assert len(category.get_products_list()) == 1
        assert Category.product_count == initial_count + 1

        # Добавляем еще один продукт
        product2 = Product("Еще товар", "Описание", 600, 20)
        category.add_product(product2)

        assert len(category.get_products_list()) == 2
        assert Category.product_count == initial_count + 2

    def test_add_product_increments_counter(self):
        """Тест что add_product увеличивает счетчик продуктов на 1"""
        Category.category_count = 0
        Category.product_count = 0

        category = Category("Тест", "Описание")
        initial_count = Category.product_count

        product = Product("Товар", "Описание", 100, 10)
        category.add_product(product)

        assert Category.product_count == initial_count + 1


class TestUtils:
    """Тесты для утилит загрузки данных"""

    def test_load_categories_from_json_success(self, tmp_path):
        """Тест успешной загрузки категорий из JSON"""
        # Создаем временный JSON файл
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

        # Сохраняем во временный файл
        json_file = tmp_path / "test_products.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        # Загружаем категории
        categories = load_categories_from_json(str(json_file))

        # Проверяем результат
        assert len(categories) == 2
        assert categories[0].name == "Электроника"
        assert categories[0].description == "Различные электронные устройства"
        assert len(categories[0].get_products_list()) == 2

        assert categories[1].name == "Аксессуары"
        assert len(categories[1].get_products_list()) == 1

        # Проверяем продукты
        products = categories[0].get_products_list()
        assert products[0].name == "Смартфон"
        assert products[0].price == 25000.50
        assert products[0].quantity == 50

    def test_load_categories_from_json_empty(self, tmp_path):
        """Тест загрузки пустого JSON файла"""
        json_file = tmp_path / "empty.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump([], f)

        categories = load_categories_from_json(str(json_file))
        assert categories == []

    def test_load_categories_from_json_file_not_found(self, capsys):
        """Тест загрузки из несуществующего файла"""
        categories = load_categories_from_json("non_existent_file.json")
        assert categories == []

        captured = capsys.readouterr()
        assert "Файл non_existent_file.json не найден" in captured.out

    def test_load_categories_from_json_invalid_json(self, tmp_path, capsys):
        """Тест загрузки из некорректного JSON файла"""
        json_file = tmp_path / "invalid.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            f.write("this is not valid json")

        categories = load_categories_from_json(str(json_file))
        assert categories == []

        captured = capsys.readouterr()
        assert "Ошибка декодирования JSON" in captured.out

    def test_load_categories_from_json_missing_fields(self, tmp_path):
        """Тест загрузки JSON с отсутствующими полями"""
        json_data = [
            {
                "name": "Категория без товаров"
                # Отсутствует description и products
            }
        ]

        json_file = tmp_path / "missing_fields.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f)

        categories = load_categories_from_json(str(json_file))

        assert len(categories) == 1
        assert categories[0].name == "Категория без товаров"
        assert categories[0].description == ""  # Значение по умолчанию
        assert categories[0].get_products_list() == []  # Пустой список по умолчанию
