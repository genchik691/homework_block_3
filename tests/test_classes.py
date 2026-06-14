import pytest

from src.classes import Category, Product


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

    def test_private_price_attribute(self):
        """Тест приватного атрибута цены"""
        product = Product("Телефон", "Смартфон", 50000.00, 5)

        # Проверяем, что атрибут _price существует (он приватный, но доступен)
        # В Python приватные атрибуты доступны, но по соглашению их не используют
        assert hasattr(product, '_price')
        assert product._price == 50000.00

    def test_price_setter_valid(self):
        """Тест сеттера цены с корректным значением"""
        product = Product("Телефон", "Смартфон", 50000.00, 5)
        product.price = 45000.00
        assert product.price == 45000.00

    def test_price_setter_invalid(self, capsys):
        """Тест сеттера цены с некорректным значением"""
        product = Product("Телефон", "Смартфон", 50000.00, 5)
        product.price = -100

        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 50000.00

    def test_price_setter_zero(self, capsys):
        """Тест сеттера цены с нулевым значением"""
        product = Product("Телефон", "Смартфон", 50000.00, 5)
        product.price = 0

        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 50000.00

    def test_new_product_class_method(self):
        """Тест класс-метода new_product"""
        product_data = {
            'name': 'Планшет',
            'description': 'Планшет для работы',
            'price': 30000.00,
            'quantity': 20
        }
        product = Product.new_product(product_data)

        assert product.name == 'Планшет'
        assert product.description == 'Планшет для работы'
        assert product.price == 30000.00
        assert product.quantity == 20
        assert isinstance(product, Product)

    def test_product_string_representation(self, sample_product):
        """Тест строкового представления продукта"""
        expected = "Ноутбук, 75000.99 руб. Остаток: 10 шт."
        assert str(sample_product) == expected


class TestCategory:
    """Тесты для класса Category"""

    def test_private_products_attribute(self, sample_category):
        """Тест приватного атрибута products"""
        # Проверяем, что атрибут _products существует
        assert hasattr(sample_category, '_products')
        assert len(sample_category._products) == 2

    def test_products_getter(self, sample_category):
        """Тест геттера products"""
        products_str = sample_category.products
        assert "Мышь, 1500.5 руб. Остаток: 25 шт." in products_str
        assert "Клавиатура, 3500.0 руб. Остаток: 15 шт." in products_str

    def test_add_product(self):
        """Тест метода add_product"""
        category = Category("Тестовая категория", "Описание")
        product = Product("Товар", "Описание", 100, 10)

        # Проверяем, что изначально товаров нет
        assert category.products == ""

        # Добавляем товар
        category.add_product(product)

        # Проверяем, что товар добавился
        assert "Товар, 100 руб. Остаток: 10 шт." in category.products

    def test_add_product_updates_product_count(self):
        """Тест обновления счетчика продуктов при добавлении"""
        initial_count = Category.product_count

        category = Category("Тестовая категория", "Описание")
        product = Product("Товар", "Описание", 100, 10)

        category.add_product(product)
        assert Category.product_count == initial_count + 1

    def test_category_initialization(self, sample_category):
        """Тест корректной инициализации категории"""
        assert sample_category.name == "Электроника"
        assert sample_category.description == "Различные электронные устройства"

    def test_category_without_products(self):
        """Тест создания категории без товаров"""
        category = Category("Книги", "Художественная литература")
        assert category.name == "Книги"
        assert category.description == "Художественная литература"
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

        products = [
            Product("Товар 1", "Описание 1", 100, 10),
            Product("Товар 2", "Описание 2", 200, 20),
            Product("Товар 3", "Описание 3", 300, 30)
        ]
        Category("Тестовая категория", "Описание", products)

        assert Category.product_count == initial_count + 3

    def test_empty_category_products_getter(self):
        """Тест геттера для пустой категории"""
        category = Category("Пустая", "Описание")
        assert category.products == ""


class TestAdditionalFeatures:
    """Тесты для дополнительных функций"""

    def test_new_product_with_dict(self):
        """Тест создания продукта из словаря"""
        product_data = {
            'name': 'Тестовый товар',
            'description': 'Описание',
            'price': 1000,
            'quantity': 5
        }
        product = Product.new_product(product_data)

        assert product.name == 'Тестовый товар'
        assert product.price == 1000
        assert product.quantity == 5

    def test_merge_duplicate_products(self):
        """Тест объединения дублирующихся продуктов"""
        from src.utils import check_and_merge_product

        existing_products = [
            Product("Смартфон", "Описание", 25000, 50)
        ]

        new_product_data = {
            'name': 'Смартфон',
            'description': 'Обновленный',
            'price': 26000,
            'quantity': 30
        }

        merged = check_and_merge_product(existing_products, new_product_data)

        assert merged.quantity == 80
        assert merged.price == 26000


class TestUtilsCoverage:
    """Тесты для повышения покрытия utils.py"""

    def test_load_categories_file_not_found(self, capsys):
        """Тест: файл не найден"""
        from src.utils import load_categories_from_json

        result = load_categories_from_json("non_existent_file.json")
        captured = capsys.readouterr()

        assert result == []
        assert "Файл non_existent_file.json не найден" in captured.out

    def test_load_categories_invalid_json(self, tmp_path, capsys):
        """Тест: некорректный JSON"""
        from src.utils import load_categories_from_json

        # Создаем временный файл с некорректным JSON
        invalid_file = tmp_path / "invalid.json"
        invalid_file.write_text("{invalid json}")

        result = load_categories_from_json(str(invalid_file))
        captured = capsys.readouterr()

        assert result == []
        assert "Ошибка декодирования JSON" in captured.out

    def test_load_categories_empty_array(self, tmp_path):
        """Тест: пустой массив в JSON"""
        from src.utils import load_categories_from_json

        empty_file = tmp_path / "empty.json"
        empty_file.write_text("[]")

        result = load_categories_from_json(str(empty_file))

        assert result == []

    def test_check_and_merge_no_duplicate(self):
        """Тест: нет дубликата"""
        from src.utils import check_and_merge_product

        existing = [Product("Товар1", "Описание", 100, 10)]
        new_data = {
            'name': 'Товар2',
            'description': 'Новый товар',
            'price': 200,
            'quantity': 5
        }

        result = check_and_merge_product(existing, new_data)

        assert result.name == 'Товар2'
        assert result.price == 200
        assert result.quantity == 5

    def test_check_and_merge_with_lower_price(self):
        """Тест: дубликат с меньшей ценой"""
        from src.utils import check_and_merge_product

        existing = [Product("Смартфон", "Описание", 25000, 50)]
        new_data = {
            'name': 'Смартфон',
            'description': 'Обновленный',
            'price': 24000,
            'quantity': 30
        }

        result = check_and_merge_product(existing, new_data)

        assert result.quantity == 80
        assert result.price == 25000  # Оставляем максимальную цену
