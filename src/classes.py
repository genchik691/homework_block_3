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
        return f"{self.name} - {self.__price} руб."

    def __repr__(self) -> str:
        return f"Product('{self.name}', '{self.description}', {self.__price}, {self.quantity})"


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
            Строка с информацией о товарах в формате:
            "Название продукта, X руб. Остаток: X шт."
            Каждый товар с новой строки
        """
        if not self.__products:
            return ""

        result = []
        for product in self.__products:
            # Точный формат из задания: "Название продукта, X руб. Остаток: X шт."
            # Важно: пробел после запятой, точка после руб, пробел после точки
            result.append(f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.")

        return "\n".join(result)

    def add_product(self, product: Product) -> None:
        """Добавление продукта в категорию"""
        self.__products.append(product)
        Category.product_count += 1

    def get_products_list(self) -> List[Product]:
        """Возвращает список продуктов (для тестирования)"""
        return self.__products

    def __str__(self) -> str:
        return f"{self.name}: {len(self.__products)} товаров"

    def __repr__(self) -> str:
        return f"Category('{self.name}', '{self.description}', {self.__products})"