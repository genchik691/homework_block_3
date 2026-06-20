from typing import Iterator
from src.classes import Product, Category


class CategoryIterator:
    """
    Итератор для перебора товаров в категории

    Позволяет использовать цикл for для перебора всех продуктов в категории
    """

    def __init__(self, category: Category):
        """
        Инициализация итератора

        Args:
            category: Объект категории для итерации
        """
        self.category = category
        self.index = 0

    def __iter__(self) -> 'CategoryIterator':
        """Возвращает сам итератор"""
        return self

    def __next__(self) -> Product:
        """
        Возвращает следующий продукт из категории

        Returns:
            Следующий продукт

        Raises:
            StopIteration: Когда все продукты перебраны
        """
        products = self.category.get_products_list()
        if self.index >= len(products):
            raise StopIteration

        product = products[self.index]
        self.index += 1
        return product