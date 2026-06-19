from src.classes import Product, Category
from src.utils import load_categories_from_json
from src.iterators import CategoryIterator


def main():
    """Основная функция для демонстрации работы классов"""

    print("=== Демонстрация работы классов ===")

    # Создаем продукты
    product1 = Product("Смартфон", "Современный смартфон", 25000.50, 50)
    product2 = Product("Наушники", "Беспроводные наушники", 3500.00, 100)
    product3 = Product("Чехол", "Защитный чехол", 500.00, 200)

    # Создаем категории
    electronics = Category("Электроника", "Различные электронные устройства", [product1, product2])
    accessories = Category("Аксессуары", "Аксессуары для устройств", [product3])

    print(f"\nВсего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")

    print("\nИнформация о категориях:")
    print(f"- {electronics}")
    print(f"- {accessories}")

    # Демонстрация __str__ продуктов
    print("\nИнформация о продуктах:")
    print(f"- {product1}")
    print(f"- {product2}")
    print(f"- {product3}")

    # Демонстрация __add__
    print("\nДемонстрация сложения продуктов:")
    total_cost = product1 + product2
    print(f"{product1.name} + {product2.name} = {total_cost} руб.")

    # Демонстрация геттера products
    print("\nТовары в категории 'Электроника':")
    print(electronics.products)

    # Демонстрация итератора (дополнительное задание)
    print("\n=== Итерация по товарам категории 'Электроника' ===")
    iterator = CategoryIterator(electronics)
    for product in iterator:
        print(f"- {product}")

    # Загрузка из JSON
    print("\n=== Загрузка данных из JSON ===")
    categories = load_categories_from_json('data/products.json')
    print(f"Загружено категорий: {len(categories)}")
    for category in categories:
        print(f"- {category}")


if __name__ == "__main__":
    main()
