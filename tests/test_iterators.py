import pytest
from src.classes import Product, Category
from src.iterators import CategoryIterator


class TestCategoryIterator:
    """Тесты для итератора категории"""

    def test_iterator_initialization(self):
        """Тест инициализации итератора"""
        category = Category("Тест", "Описание")
        iterator = CategoryIterator(category)
        assert iterator.category == category
        assert iterator.index == 0

    def test_iterator_iter_method(self):
        """Тест метода __iter__"""
        category = Category("Тест", "Описание")
        iterator = CategoryIterator(category)
        assert iter(iterator) == iterator

    def test_iterator_next(self):
        """Тест метода __next__"""
        products = [
            Product("Товар 1", "Описание", 100, 10),
            Product("Товар 2", "Описание", 200, 20)
        ]
        category = Category("Тест", "Описание", products)
        iterator = CategoryIterator(category)

        assert next(iterator) == products[0]
        assert next(iterator) == products[1]

        with pytest.raises(StopIteration):
            next(iterator)

    def test_iterator_for_loop(self):
        """Тест использования итератора в цикле for"""
        products = [
            Product("Товар 1", "Описание", 100, 10),
            Product("Товар 2", "Описание", 200, 20),
            Product("Товар 3", "Описание", 300, 30)
        ]
        category = Category("Тест", "Описание", products)

        iterated_products = []
        for product in CategoryIterator(category):
            iterated_products.append(product)

        assert len(iterated_products) == 3
        assert iterated_products == products

    def test_iterator_empty_category(self):
        """Тест итератора для пустой категории"""
        category = Category("Пустая", "Описание")
        iterator = CategoryIterator(category)

        with pytest.raises(StopIteration):
            next(iterator)

        # Цикл for не должен выполниться
        count = 0
        for _ in CategoryIterator(category):
            count += 1
        assert count == 0