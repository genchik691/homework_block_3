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

    def test_product_add_method(self):
        """Тест магического метода __add__"""
        product1 = Product("Товар A", "Описание", 100, 10)
        product2 = Product("Товар B", "Описание", 200, 2)

        result = product1 + product2
        expected = (100 * 10) + (200 * 2)  # 1000 + 400 = 1400
        assert result == expected

    def test_product_add_method_with_zero_quantity(self):
        """Тест сложения с нулевым количеством"""
        product1 = Product("Товар A", "Описание", 100, 10)
        product2 = Product("Товар B", "Описание", 200, 0)

        result = product1 + product2
        expected = (100 * 10) + (200 * 0)  # 1000
        assert result == expected

    def test_product_add_method_same_product(self):
        """Тест сложения продукта с самим собой"""
        product = Product("Товар", "Описание", 150, 5)
        result = product + product
        expected = (150 * 5) + (150 * 5)  # 1500
        assert result == expected

    def test_product_add_method_invalid_type(self):
        """Тест сложения с неверным типом"""
        product = Product("Товар", "Описание", 100, 10)
        with pytest.raises(TypeError, match="Нельзя сложить Product и int"):
            _ = product + 5


class TestCategory:
    """Тесты для класса Category"""

    def test_category_initialization(self, sample_category):
        """Тест корректной инициализации категории"""
        assert sample_category.name == "Электроника"
        assert sample_category.description == "Различные электронные устройства"
        assert len(sample_category.get_products_list()) == 2
        assert isinstance(sample_category.get_products_list()[0], Product)

    def test_category_without_products(self):
        """Тест создания категории без товаров"""
        category = Category("Книги", "Художественная литература")
        assert category.name == "Книги"
        assert category.description == "Художественная литература"
        assert category.get_products_list() == []

    def test_products_getter_format(self):
        """Тест геттера для продуктов с использованием __str__"""
        product1 = Product("Смартфон", "Описание", 25000.50, 50)
        product2 = Product("Наушники", "Описание", 3500.00, 100)
        category = Category("Электроника", "Описание", [product1, product2])

        result = category.products
        expected = "Смартфон, 25000.5 руб. Остаток: 50 шт.\nНаушники, 3500.0 руб. Остаток: 100 шт."
        assert result == expected

    def test_products_getter_empty(self):
        """Тест геттера для пустой категории"""
        category = Category("Пустая категория", "Нет товаров")
        assert category.products == ""

    def test_category_string_representation(self, sample_category):
        """Тест __str__ категории"""
        # total_quantity = 25 + 15 = 40
        expected = "Электроника, количество продуктов: 40 шт."
        assert str(sample_category) == expected

    def test_category_string_representation_empty(self):
        """Тест __str__ пустой категории"""
        category = Category("Книги", "Художественная литература")
        expected = "Книги, количество продуктов: 0 шт."
        assert str(category) == expected

    def test_category_total_quantity_property(self):
        """Тест свойства total_quantity"""
        products = [
            Product("Товар 1", "Описание", 100, 10),
            Product("Товар 2", "Описание", 200, 20),
            Product("Товар 3", "Описание", 300, 30)
        ]
        category = Category("Тест", "Описание", products)
        assert category.total_quantity == 60  # 10 + 20 + 30

    def test_category_total_quantity_empty(self):
        """Тест total_quantity для пустой категории"""
        category = Category("Пустая", "Описание")
        assert category.total_quantity == 0

    def test_category_repr(self, sample_category):
        """Тест __repr__ категории"""
        assert "Category('Электроника', 'Различные электронные устройства'" in repr(sample_category)

    def test_category_count_increment(self):
        """Тест автоматического подсчета количества категорий"""
        initial_count = Category.category_count

        Category("Категория 1", "Описание 1")
        assert Category.category_count == initial_count + 1

        Category("Категория 2", "Описание 2")
        assert Category.category_count == initial_count + 2

    def test_product_count_calculation(self):
        """Тест корректного подсчета количества товаров"""
        initial_count = Category.product_count

        products = [
            Product("Товар 1", "Описание 1", 100, 10),
            Product("Товар 2", "Описание 2", 200, 20),
            Product("Товар 3", "Описание 3", 300, 30)
        ]
        Category("Тестовая категория", "Описание", products)

        assert Category.product_count == initial_count + 3

    def test_multiple_categories_product_count(self):
        """Тест подсчета товаров при создании нескольких категорий"""
        Category.category_count = 0
        Category.product_count = 0

        cat1_products = [
            Product("Товар A", "Описание A", 100, 5),
            Product("Товар B", "Описание B", 200, 3)
        ]
        Category("Категория 1", "Описание 1", cat1_products)

        assert Category.category_count == 1
        assert Category.product_count == 2

        cat2_products = [Product("Товар C", "Описание C", 300, 7)]
        Category("Категория 2", "Описание 2", cat2_products)

        assert Category.category_count == 2
        assert Category.product_count == 3

    def test_add_product_to_category(self):
        """Тест добавления продукта в категорию"""
        initial_count = Category.product_count

        category = Category("Тестовая категория", "Описание")
        product = Product("Новый товар", "Описание", 500, 15)

        category.add_product(product)

        assert len(category.get_products_list()) == 1
        assert Category.product_count == initial_count + 1

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
