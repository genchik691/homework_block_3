from typing import List, Optional, Type


class Product:
    """Базовый класс для представления продукта"""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        """
        Инициализация продукта

        Args:
            name: Название продукта
            description: Описание продукта
            price: Цена продукта
            quantity: Количество в наличии
        """
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Геттер для цены"""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для цены с проверкой"""
        if new_price <= 0:
            print("Цена не может быть отрицательной или нулевой")
        else:
            self.__price = new_price

    @classmethod
    def new_product(cls, product_data: dict) -> 'Product':
        """Класс-метод для создания продукта из словаря"""
        return cls(
            name=product_data.get('name', ''),
            description=product_data.get('description', ''),
            price=float(product_data.get('price', 0)),
            quantity=int(product_data.get('quantity', 0))
        )

    def __str__(self) -> str:
        """
        Строковое представление продукта

        Returns:
            Строка в формате: "Название продукта, X руб. Остаток: X шт."
        """
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __repr__(self) -> str:
        return f"Product('{self.name}', '{self.description}', {self.__price}, {self.quantity})"

    def __add__(self, other: 'Product') -> float:
        """
        Сложение продуктов (общая стоимость товаров на складе)

        Args:
            other: Другой продукт для сложения

        Returns:
            Сумма произведений цены на количество для двух продуктов

        Raises:
            TypeError: Если типы продуктов не совпадают
        """
        if not isinstance(other, Product):
            raise TypeError(f"Нельзя сложить Product и {type(other).__name__}")

        # Проверяем, что объекты одного класса
        if type(self) is not type(other):
            raise TypeError(f"Нельзя сложить товары разных классов: {type(self).__name__} и {type(other).__name__}")

        return (self.price * self.quantity) + (other.price * other.quantity)


class Smartphone(Product):
    """Класс для представления смартфона"""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: str, model: str, memory: int, color: str):
        """
        Инициализация смартфона

        Args:
            name: Название смартфона
            description: Описание смартфона
            price: Цена смартфона
            quantity: Количество в наличии
            efficiency: Производительность
            model: Модель смартфона
            memory: Объем встроенной памяти (ГБ)
            color: Цвет смартфона
        """
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __repr__(self) -> str:
        return (f"Smartphone('{self.name}', '{self.description}', {self.price}, {self.quantity}, "
                f"'{self.efficiency}', '{self.model}', {self.memory}, '{self.color}')")


class LawnGrass(Product):
    """Класс для представления газонной травы"""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: str, color: str):
        """
        Инициализация газонной травы

        Args:
            name: Название травы
            description: Описание травы
            price: Цена травы
            quantity: Количество в наличии
            country: Страна-производитель
            germination_period: Срок прорастания
            color: Цвет травы
        """
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __repr__(self) -> str:
        return (f"LawnGrass('{self.name}', '{self.description}', {self.price}, {self.quantity}, "
                f"'{self.country}', '{self.germination_period}', '{self.color}')")


class Category:
    """Класс для представления категории товаров"""

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: Optional[List[Product]] = None):
        """
        Инициализация категории

        Args:
            name: Название категории
            description: Описание категории
            products: Список товаров в категории
        """
        self.name = name
        self.description = description
        self.__products = products if products is not None else []

        Category.category_count += 1
        Category.product_count += len(self.__products)

    @property
    def products(self) -> str:
        """
        Геттер для списка товаров

        Returns:
            Строка с информацией о товарах, каждый с новой строки
        """
        if not self.__products:
            return ""

        return "\n".join(str(product) for product in self.__products)

    @property
    def total_quantity(self) -> int:
        """
        Общее количество товаров в категории

        Returns:
            Сумма quantity всех продуктов в категории
        """
        return sum(product.quantity for product in self.__products)

    def add_product(self, product: Product) -> None:
        """
        Добавление продукта в категорию

        Args:
            product: Объект продукта для добавления

        Raises:
            TypeError: Если добавляемый объект не является продуктом или его наследником
        """
        # Проверяем, что объект является продуктом или его наследником
        if not isinstance(product, Product):
            raise TypeError(
                f"Можно добавлять только объекты Product или его наследников. Получен: {type(product).__name__}")

        self.__products.append(product)
        Category.product_count += 1

    def get_products_list(self) -> List[Product]:
        """Возвращает список продуктов (для тестирования)"""
        return self.__products

    def __str__(self) -> str:
        """
        Строковое представление категории

        Returns:
            Строка в формате: "Название категории, количество продуктов: X шт."
        """
        return f"{self.name}, количество продуктов: {self.total_quantity} шт."

    def __repr__(self) -> str:
        return f"Category('{self.name}', '{self.description}', {self.__products})"
