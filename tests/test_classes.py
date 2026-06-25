import pytest
from src.classes import Product, Category, Smartphone, LawnGrass


@pytest.fixture
def sample_product():
    """Фикстура для создания тестового продукта"""
    return Product("Ноутбук", "Мощный игровой ноутбук", 75000.99, 10)


@pytest.fixture
def sample_smartphone():
    """Фикстура для создания тестового смартфона"""
    return Smartphone(
        "iPhone 15", "Флагманский смартфон", 99999.99, 5,
        "A17 Pro", "iPhone 15 Pro", 256, "Титан"
    )


@pytest.fixture
def sample_lawn_grass():
    """Фикстура для создания тестовой травы"""
    return LawnGrass(
        "Газонная трава", "Смесь для газона", 1500.00, 20,
        "Россия", "7-14 дней", "Зеленый"
    )


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
        assert sample_product.price == 75000.99

        sample_product.price = 0
        captured = capsys.readouterr()
        assert "Цена не может быть отрицательной или нулевой" in captured.out
        assert sample_product.price == 75000.99

    def test_product_price_private_attribute(self, sample_product):
        """Тест что цена - приватный атрибут"""
        with pytest.raises(AttributeError):
            _ = sample_product.__price

    def test_product_with_different_types(self):
        """Тест инициализации с разными типами данных"""
        product = Product("Телефон", "Смартфон", 50000.00, 5)
        assert isinstance(product.name, str)
        assert isinstance(product.description, str)
        assert isinstance(product.price, float)
        assert isinstance(product.quantity, int)

    def test_product_string_representation(self, sample_product):
        """Тест __str__ продукта"""
        expected = "Ноутбук, 75000.99 руб. Остаток: 10 шт."
        assert str(sample_product) == expected

    def test_product_string_representation_format(self):
        """Тест формата __str__ продукта"""
        product = Product("Смартфон", "Описание", 25000.50, 50)
        result = str(product)

        assert "Смартфон" in result
        assert "25000.5 руб." in result or "25000.50 руб." in result
        assert "Остаток: 50 шт." in result
        assert ", " in result
        assert ". " in result

    def test_product_repr(self, sample_product):
        """Тест __repr__ продукта"""
        expected = "Product('Ноутбук', 'Мощный игровой ноутбук', 75000.99, 10)"
        assert repr(sample_product) == expected

    def test_product_price_zero_through_setter(self):
        """Тест установки нулевой цены через сеттер"""
        product = Product("Бесплатный товар", "Акция", 0.0, 100)
        assert product.price == 0.0

        product.price = 0

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

    def test_product_add_method_same_class(self):
        """Тест магического метода __add__ с одинаковыми классами"""
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


class TestSmartphone:
    """Тесты для класса Smartphone"""

    def test_smartphone_initialization(self, sample_smartphone):
        """Тест корректной инициализации смартфона"""
        assert sample_smartphone.name == "iPhone 15"
        assert sample_smartphone.description == "Флагманский смартфон"
        assert sample_smartphone.price == 99999.99
        assert sample_smartphone.quantity == 5
        assert sample_smartphone.efficiency == "A17 Pro"
        assert sample_smartphone.model == "iPhone 15 Pro"
        assert sample_smartphone.memory == 256
        assert sample_smartphone.color == "Титан"

    def test_smartphone_inheritance(self, sample_smartphone):
        """Тест что Smartphone наследник Product"""
        assert isinstance(sample_smartphone, Product)
        assert issubclass(Smartphone, Product)

    def test_smartphone_string_representation(self, sample_smartphone):
        """Тест __str__ смартфона"""
        result = str(sample_smartphone)
        assert "iPhone 15" in result
        assert "99999.99 руб." in result
        assert "Остаток: 5 шт." in result

    def test_smartphone_repr(self, sample_smartphone):
        """Тест __repr__ смартфона"""
        expected = "Smartphone('iPhone 15', 'Флагманский смартфон', 99999.99, 5, 'A17 Pro', 'iPhone 15 Pro', 256, 'Титан')"
        assert repr(sample_smartphone) == expected

    def test_smartphone_add_same_class(self, sample_smartphone):
        """Тест сложения двух смартфонов"""
        smartphone2 = Smartphone(
            "Samsung Galaxy", "Флагман", 89999.99, 3,
            "Exynos 2200", "S23 Ultra", 512, "Черный"
        )
        result = sample_smartphone + smartphone2
        expected = (99999.99 * 5) + (89999.99 * 3)
        assert result == expected

    def test_smartphone_add_different_class(self, sample_smartphone, sample_lawn_grass):
        """Тест сложения смартфона и травы (должна быть ошибка)"""
        with pytest.raises(TypeError, match="Нельзя сложить товары разных классов: Smartphone и LawnGrass"):
            _ = sample_smartphone + sample_lawn_grass


class TestLawnGrass:
    """Тесты для класса LawnGrass"""

    def test_lawn_grass_initialization(self, sample_lawn_grass):
        """Тест корректной инициализации травы"""
        assert sample_lawn_grass.name == "Газонная трава"
        assert sample_lawn_grass.description == "Смесь для газона"
        assert sample_lawn_grass.price == 1500.00
        assert sample_lawn_grass.quantity == 20
        assert sample_lawn_grass.country == "Россия"
        assert sample_lawn_grass.germination_period == "7-14 дней"
        assert sample_lawn_grass.color == "Зеленый"

    def test_lawn_grass_inheritance(self, sample_lawn_grass):
        """Тест что LawnGrass наследник Product"""
        assert isinstance(sample_lawn_grass, Product)
        assert issubclass(LawnGrass, Product)

    def test_lawn_grass_string_representation(self, sample_lawn_grass):
        """Тест __str__ травы"""
        result = str(sample_lawn_grass)
        assert "Газонная трава" in result
        assert "1500.0 руб." in result
        assert "Остаток: 20 шт." in result

    def test_lawn_grass_repr(self, sample_lawn_grass):
        """Тест __repr__ травы"""
        expected = "LawnGrass('Газонная трава', 'Смесь для газона', 1500.0, 20, 'Россия', '7-14 дней', 'Зеленый')"
        assert repr(sample_lawn_grass) == expected

    def test_lawn_grass_add_same_class(self, sample_lawn_grass):
        """Тест сложения двух трав"""
        grass2 = LawnGrass(
            "Газон", "Теневой газон", 1800.00, 10,
            "Германия", "10-20 дней", "Темно-зеленый"
        )
        result = sample_lawn_grass + grass2
        expected = (1500.00 * 20) + (1800.00 * 10)
        assert result == expected

    def test_lawn_grass_add_different_class(self, sample_lawn_grass, sample_smartphone):
        """Тест сложения травы и смартфона (должна быть ошибка)"""
        with pytest.raises(TypeError, match="Нельзя сложить товары разных классов: LawnGrass и Smartphone"):
            _ = sample_lawn_grass + sample_smartphone


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
        assert category.total_quantity == 60

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

    def test_add_product_with_smartphone(self):
        """Тест добавления смартфона в категорию"""
        category = Category("Смартфоны", "Категория смартфонов")
        smartphone = Smartphone(
            "iPhone 15", "Флагман", 99999.99, 5,
            "A17 Pro", "iPhone 15 Pro", 256, "Титан"
        )

        category.add_product(smartphone)
        assert len(category.get_products_list()) == 1
        assert isinstance(category.get_products_list()[0], Smartphone)

    def test_add_product_with_lawn_grass(self):
        """Тест добавления травы в категорию"""
        category = Category("Газоны", "Категория газонов")
        grass = LawnGrass(
            "Газонная трава", "Смесь", 1500.00, 20,
            "Россия", "7-14 дней", "Зеленый"
        )

        category.add_product(grass)
        assert len(category.get_products_list()) == 1
        assert isinstance(category.get_products_list()[0], LawnGrass)

    def test_add_product_invalid_type(self):
        """Тест добавления не-продукта в категорию (должна быть ошибка)"""
        category = Category("Тест", "Описание")

        with pytest.raises(TypeError, match="Можно добавлять только объекты Product или его наследников"):
            category.add_product("это строка, не продукт")

        with pytest.raises(TypeError, match="Можно добавлять только объекты Product или его наследников"):
            category.add_product(123)

        with pytest.raises(TypeError, match="Можно добавлять только объекты Product или его наследников"):
            category.add_product(None)

        # Проверяем, что продукты не были добавлены
        assert len(category.get_products_list()) == 0
