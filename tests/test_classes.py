import pytest
from src.classes import Product, Category


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
        assert sample_product.price == 75000.99
        assert sample_product.quantity == 10

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

    def test_product_price_zero(self):
        """Тест продукта с нулевой ценой"""
        product = Product("Бесплатный товар", "Акция", 0.0, 100)
        assert product.price == 0.0
        assert product.quantity == 100


class TestCategory:
    """Тесты для класса Category"""

    def test_category_initialization(self, sample_category):
        """Тест корректной инициализации категории"""
        assert sample_category.name == "Электроника"
        assert sample_category.description == "Различные электронные устройства"
        assert len(sample_category.products) == 2
        assert isinstance(sample_category.products[0], Product)

    def test_category_without_products(self):
        """Тест создания категории без товаров"""
        category = Category("Книги", "Художественная литература")
        assert category.name == "Книги"
        assert category.description == "Художественная литература"
        assert category.products == []

    def test_category_count_increment(self):
        """Тест автоматического подсчета количества категорий"""
        initial_count = Category.category_count

        # Создаем новую категорию
        category1 = Category("Категория 1", "Описание 1")
        assert Category.category_count == initial_count + 1

        # Создаем еще одну категорию
        category2 = Category("Категория 2", "Описание 2")
        assert Category.category_count == initial_count + 2

    def test_product_count_calculation(self):
        """Тест корректного подсчета количества товаров"""
        initial_count = Category.product_count

        # Создаем категорию с 3 товарами
        products = [
            Product("Товар 1", "Описание 1", 100, 10),
            Product("Товар 2", "Описание 2", 200, 20),
            Product("Товар 3", "Описание 3", 300, 30)
        ]
        category = Category("Тестовая категория", "Описание", products)

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
        category1 = Category("Категория 1", "Описание 1", cat1_products)

        assert Category.category_count == 1
        assert Category.product_count == 2

        # Создаем вторую категорию с 1 товаром
        cat2_products = [Product("Товар C", "Описание C", 300, 7)]
        category2 = Category("Категория 2", "Описание 2", cat2_products)

        assert Category.category_count == 2
        assert Category.product_count == 3

    def test_add_product_to_category(self):
        """Тест добавления продукта в категорию"""
        initial_count = Category.product_count

        category = Category("Тестовая категория", "Описание")
        product = Product("Новый товар", "Описание", 500, 15)

        # Добавляем продукт
        category.add_product(product)

        assert len(category.products) == 1
        assert Category.product_count == initial_count + 1

        # Добавляем еще один продукт
        product2 = Product("Еще товар", "Описание", 600, 20)
        category.add_product(product2)

        assert len(category.products) == 2
        assert Category.product_count == initial_count + 2