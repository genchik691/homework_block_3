import pytest
from abc import ABC
from src.classes import Product, Category, Smartphone, LawnGrass, Order, BaseProduct


@pytest.fixture
def sample_product():
    return Product("Ноутбук", "Мощный игровой ноутбук", 75000.99, 10)


@pytest.fixture
def sample_smartphone():
    return Smartphone(
        "iPhone 15", "Флагманский смартфон", 99999.99, 5,
        "A17 Pro", "iPhone 15 Pro", 256, "Титан"
    )


@pytest.fixture
def sample_lawn_grass():
    return LawnGrass(
        "Газонная трава", "Смесь для газона", 1500.00, 20,
        "Россия", "7-14 дней", "Зеленый"
    )


@pytest.fixture
def sample_category():
    product1 = Product("Мышь", "Беспроводная мышь", 1500.50, 25)
    product2 = Product("Клавиатура", "Механическая клавиатура", 3500.00, 15)
    return Category("Электроника", "Различные электронные устройства", [product1, product2])


class TestBaseProduct:
    def test_base_product_is_abstract(self):
        assert isinstance(BaseProduct, type)
        assert hasattr(BaseProduct, '__abstractmethods__')
        assert BaseProduct.__abstractmethods__ is not None

    def test_product_inherits_from_base_product(self):
        assert issubclass(Product, BaseProduct)

    def test_smartphone_inherits_from_base_product(self):
        assert issubclass(Smartphone, BaseProduct)

    def test_lawn_grass_inherits_from_base_product(self):
        assert issubclass(LawnGrass, BaseProduct)


class TestLoggingMixin:
    """Тесты для LoggingMixin"""

    def test_logging_mixin_output(self, capsys):
        """Тест что миксин выводит информацию о создании объекта"""
        product = Product("Тест", "Описание", 100, 10)
        captured = capsys.readouterr()
        expected = "Product('Тест', 'Описание', 100, 10)\n"
        assert captured.out == expected

    def test_logging_mixin_smartphone_output(self, capsys):
        """Тест что миксин работает для Smartphone"""
        smartphone = Smartphone(
            "iPhone", "Флагман", 99999.99, 5,
            "A17 Pro", "iPhone 15 Pro", 256, "Титан"
        )
        captured = capsys.readouterr()
        expected = ("Smartphone('iPhone', 'Флагман', 99999.99, 5, 'A17 Pro', "
                    "'iPhone 15 Pro', 256, 'Титан')\n")
        assert captured.out == expected

    def test_logging_mixin_lawn_grass_output(self, capsys):
        """Тест что миксин работает для LawnGrass"""
        grass = LawnGrass(
            "Газон", "Описание", 1500.00, 20,
            "Россия", "7-14 дней", "Зеленый"
        )
        captured = capsys.readouterr()
        expected = ("LawnGrass('Газон', 'Описание', 1500.0, 20, 'Россия', "
                    "'7-14 дней', 'Зеленый')\n")
        assert captured.out == expected

    def test_multiple_objects_logging(self, capsys):
        """Тест логирования нескольких объектов"""
        Product("Товар 1", "Описание 1", 100, 10)
        Product("Товар 2", "Описание 2", 200, 20)

        captured = capsys.readouterr()
        assert "Product('Товар 1', 'Описание 1', 100, 10)" in captured.out
        assert "Product('Товар 2', 'Описание 2', 200, 20)" in captured.out

class TestProduct:
    def test_product_initialization(self, sample_product):
        assert sample_product.name == "Ноутбук"
        assert sample_product.description == "Мощный игровой ноутбук"
        assert sample_product.price == 75000.99
        assert sample_product.quantity == 10

    def test_product_price_setter_invalid(self, sample_product, capsys):
        sample_product.price = -100
        captured = capsys.readouterr()
        assert "Цена не может быть отрицательной или нулевой" in captured.out
        # Цена не должна измениться
        assert sample_product.price == 75000.99

        sample_product.price = 0
        captured = capsys.readouterr()
        assert "Цена не может быть отрицательной или нулевой" in captured.out
        assert sample_product.price == 75000.99

    def test_product_private_attribute(self, sample_product):
        with pytest.raises(AttributeError):
            _ = sample_product.__price

    def test_product_str(self, sample_product):
        expected = "Ноутбук, 75000.99 руб. Остаток: 10 шт."
        assert str(sample_product) == expected

    def test_product_repr(self, sample_product):
        expected = "Product('Ноутбук', 'Мощный игровой ноутбук', 75000.99, 10)"
        assert repr(sample_product) == expected

    def test_product_add_method_same_class(self):
        p1 = Product("A", "Desc", 100, 10)
        p2 = Product("B", "Desc", 200, 2)
        result = p1 + p2
        assert result == (100 * 10) + (200 * 2)

    def test_product_add_method_invalid_type(self):
        p = Product("Товар", "Описание", 100, 10)
        with pytest.raises(TypeError, match="Нельзя сложить Product и int"):
            _ = p + 5


class TestSmartphone:
    def test_smartphone_initialization(self, sample_smartphone):
        assert sample_smartphone.name == "iPhone 15"
        assert sample_smartphone.efficiency == "A17 Pro"
        assert sample_smartphone.model == "iPhone 15 Pro"
        assert sample_smartphone.memory == 256
        assert sample_smartphone.color == "Титан"

    def test_smartphone_repr(self, sample_smartphone):
        expected = ("Smartphone('iPhone 15', 'Флагманский смартфон', 99999.99, 5, "
                    "'A17 Pro', 'iPhone 15 Pro', 256, 'Титан')")
        assert repr(sample_smartphone) == expected


class TestLawnGrass:
    def test_lawn_grass_initialization(self, sample_lawn_grass):
        assert sample_lawn_grass.name == "Газонная трава"
        assert sample_lawn_grass.country == "Россия"
        assert sample_lawn_grass.germination_period == "7-14 дней"
        assert sample_lawn_grass.color == "Зеленый"

    def test_lawn_grass_repr(self, sample_lawn_grass):
        expected = ("LawnGrass('Газонная трава', 'Смесь для газона', 1500.0, 20, "
                    "'Россия', '7-14 дней', 'Зеленый')")
        assert repr(sample_lawn_grass) == expected


class TestCategory:
    def test_category_initialization(self, sample_category):
        assert sample_category.name == "Электроника"
        assert len(sample_category.get_products_list()) == 2

    def test_category_str(self, sample_category):
        # В твоем тесте ожидалась сумма 40 шт. Проверим расчёт:
        # Мышь: 25 + Клавиатура: 15 = 40. Совпадает.
        expected = "Электроника, количество продуктов: 40 шт."
        assert str(sample_category) == expected

    def test_add_product_to_category(self):
        initial_count = Category.product_count
        category = Category("Тестовая категория", "Описание")
        product = Product("Новый товар", "Описание", 500, 15)
        category.add_product(product)

        assert len(category.get_products_list()) == 1
        assert Category.product_count == initial_count + 1

    def test_add_product_invalid_type(self):
        category = Category("Тест", "Описание")
        with pytest.raises(TypeError, match="Можно добавлять только объекты Product"):
            category.add_product("это строка, не продукт")


class TestOrder:
    def test_order_initialization(self, sample_product):
        order = Order(sample_product, 3)
        assert order.product == sample_product
        assert order.quantity == 3
        assert order.total_price == 75000.99 * 3

    def test_order_str(self, sample_product):
        order = Order(sample_product, 3)
        expected = f"Заказ: {sample_product.name}, 3 шт., итого: {order.total_price} руб."
        assert str(order) == expected

    def test_order_add(self, sample_product):
        o1 = Order(sample_product, 2)
        o2 = Order(sample_product, 3)
        result = o1 + o2
        expected = (sample_product.price * 2) + (sample_product.price * 3)
        assert result == expected

    def test_order_price_setter_raises_error(self, sample_product):
        order = Order(sample_product, 3)
        with pytest.raises(AttributeError, match="Нельзя изменить цену заказа напрямую"):
            order.price = 1000


class TestProductExceptions:
    """Тесты для исключений в классе Product"""

    def test_product_zero_quantity_raises_error(self):
        """Тест что создание продукта с нулевым количеством вызывает ValueError"""
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            Product("Тестовый товар", "Описание", 100, 0)

    def test_smartphone_zero_quantity_raises_error(self):
        """Тест что создание смартфона с нулевым количеством вызывает ValueError"""
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            Smartphone(
                "iPhone", "Флагман", 99999.99, 0,
                "A17 Pro", "iPhone 15 Pro", 256, "Титан"
            )

    def test_lawn_grass_zero_quantity_raises_error(self):
        """Тест что создание травы с нулевым количеством вызывает ValueError"""
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            LawnGrass(
                "Газон", "Описание", 1500.00, 0,
                "Россия", "7-14 дней", "Зеленый"
            )


class TestCategoryAveragePrice:
    """Тесты для метода average_price в классе Category"""

    def test_average_price_with_products(self):
        """Тест подсчета средней цены с товарами"""
        products = [
            Product("Товар 1", "Описание", 100, 10),
            Product("Товар 2", "Описание", 200, 20),
            Product("Товар 3", "Описание", 300, 30)
        ]
        category = Category("Тест", "Описание", products)

        expected_average = (100 + 200 + 300) / 3
        assert category.average_price() == expected_average

    def test_average_price_with_smartphones(self):
        """Тест подсчета средней цены со смартфонами"""
        products = [
            Smartphone("iPhone", "Флагман", 99999.99, 5, "A17", "15 Pro", 256, "Титан"),
            Smartphone("Samsung", "Флагман", 89999.99, 3, "Exynos", "S23", 512, "Черный")
        ]
        category = Category("Смартфоны", "Описание", products)

        expected_average = (99999.99 + 89999.99) / 2
        assert category.average_price() == expected_average

    def test_average_price_empty_category(self):
        """Тест подсчета средней цены в пустой категории (должен вернуть 0)"""
        category = Category("Пустая категория", "Описание")
        assert category.average_price() == 0.0

    def test_average_price_category_with_one_product(self):
        """Тест подсчета средней цены с одним товаром"""
        product = Product("Товар", "Описание", 150, 5)
        category = Category("Тест", "Описание", [product])

        assert category.average_price() == 150.0

    def test_average_price_after_adding_products(self):
        """Тест подсчета средней цены после добавления товаров"""
        category = Category("Тест", "Описание")

        # Добавляем первый товар
        product1 = Product("Товар 1", "Описание", 100, 10)
        category.add_product(product1)
        assert category.average_price() == 100.0

        # Добавляем второй товар
        product2 = Product("Товар 2", "Описание", 200, 20)
        category.add_product(product2)
        assert category.average_price() == 150.0


class TestOrderExceptions:
    """Тесты для исключений в классе Order (дополнительное задание)"""

    def test_order_zero_quantity_raises_error(self):
        """Тест что создание заказа с нулевым количеством вызывает ValueError"""
        product = Product("Товар", "Описание", 100, 10)
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен в заказ"):
            Order(product, 0)