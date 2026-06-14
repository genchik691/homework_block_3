import json
from typing import Any, Dict, List

from src.classes import Category, Product


def load_categories_from_json(file_path: str) -> List[Category]:
    """
    Загрузка категорий и товаров из JSON файла

    Args:
        file_path: Путь к JSON файлу

    Returns:
        Список объектов Category
    """
    categories = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for category_data in data:
            products = []

            # Создаем продукты для категории
            for product_data in category_data.get('products', []):
                product = Product.new_product(product_data)
                products.append(product)

            # Создаем категорию с продуктами
            category = Category(
                name=category_data.get('name', ''),
                description=category_data.get('description', ''),
                products=products
            )
            categories.append(category)

    except FileNotFoundError:
        print(f"Файл {file_path} не найден")
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON в файле {file_path}")

    return categories


def check_and_merge_product(products_list: List[Product], new_product_data: Dict[str, Any]) -> Product:
    """
    Проверяет наличие товара с таким же именем и при необходимости объединяет

    Args:
        products_list: Список существующих продуктов
        new_product_data: Данные нового продукта

    Returns:
        Продукт (существующий обновленный или новый)
    """
    new_name = new_product_data.get('name', '')

    # Ищем продукт с таким же названием
    for existing_product in products_list:
        if existing_product.name == new_name:
            # Обновляем количество
            existing_product.quantity += int(new_product_data.get('quantity', 0))

            # Выбираем максимальную цену
            new_price = float(new_product_data.get('price', 0))
            if new_price > existing_product.price:
                existing_product.price = new_price

            return existing_product

    # Если не нашли, создаем новый продукт
    return Product.new_product(new_product_data)
