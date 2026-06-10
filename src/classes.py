from typing import List, Optional


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
        self.price = price
        self.quantity = quantity

    def __str__(self) -> str:
        return f"{self.name} - {self.price} руб."

    def __repr__(self) -> str:
        return f"Product('{self.name}', '{self.description}', {self.price}, {self.quantity})"


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
        self.products = products if products is not None else []

        # Автоматическое обновление атрибутов класса
        Category.category_count += 1

        # Подсчет общего количества товаров (уникальных продуктов)
        # Каждый продукт считается один раз, независимо от его количества в наличии
        Category.product_count += len(self.products)

    def add_product(self, product: Product) -> None:
        """
        Добавление продукта в категорию

        Args:
            product: Объект продукта для добавления
        """
        self.products.append(product)
        Category.product_count += 1

    def __str__(self) -> str:
        return f"{self.name}: {len(self.products)} товаров"

    def __repr__(self) -> str:
        return f"Category('{self.name}', '{self.description}', {self.products})"
