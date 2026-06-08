import json
from typing import List
from src.classes import Product, Category


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
                product = Product(
                    name=product_data.get('name', ''),
                    description=product_data.get('description', ''),
                    price=float(product_data.get('price', 0)),
                    quantity=int(product_data.get('quantity', 0))
                )
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