from typing import Any, Dict, List, Optional


class Product:
    """Класс для представления продукта"""

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
        self._price = price  # Приватный атрибут цены
        self.quantity = quantity  # Обычный атрибут, не приватный

    @property
    def price(self) -> float:
        """Геттер для цены"""
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """
        Сеттер для цены с проверкой

        Args:
            value: Новая цена
        """
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self._price = value

    @classmethod
    def new_product(cls, product_data: Dict[str, Any]) -> 'Product':
        """
        Класс-метод для создания продукта из словаря

        Args:
            product_data: Словарь с данными продукта

        Returns:
            Экземпляр класса Product
        """
        return cls(
            name=product_data.get('name', ''),
            description=product_data.get('description', ''),
            price=float(product_data.get('price', 0)),
            quantity=int(product_data.get('quantity', 0))
        )

    def __str__(self) -> str:
        return f"{self.name}, {self._price} руб. Остаток: {self.quantity} шт."

    def __repr__(self) -> str:
        return f"Product('{self.name}', '{self.description}', {self._price}, {self.quantity})"


class Category:
    """Класс для представления категории товаров"""

    # Атрибуты класса для подсчета количества категорий и товаров
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
        self._products = products if products is not None else []

        # Автоматическое обновление атрибутов класса
        Category.category_count += 1
        Category.product_count += len(self._products)

    @property
    def products(self) -> str:
        """
        Геттер для получения списка товаров в виде строки

        Returns:
            Строка со всеми продуктами в формате "Название продукта, X руб. Остаток: X шт.\n"
        """
        if not self._products:
            return ""

        result = ""
        for product in self._products:
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result

    def add_product(self, product: Product) -> None:
        """
        Добавление продукта в категорию

        Args:
            product: Объект продукта для добавления
        """
        self._products.append(product)
        Category.product_count += 1

    def __str__(self) -> str:
        return f"{self.name}: {len(self._products)} товаров"

    def __repr__(self) -> str:
        return f"Category('{self.name}', '{self.description}', {self._products})"
