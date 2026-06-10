from src.classes import Product, Category
from src.utils import load_categories_from_json


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

    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")

    print("\nИнформация о категориях:")
    print(f"- {electronics}")
    print(f"- {accessories}")

    # Демонстрация загрузки из JSON
    print("\n=== Загрузка данных из JSON ===")
    categories = load_categories_from_json('data/products.json')
    print(f"Загружено категорий: {len(categories)}")

    for category in categories:
        print(f"- {category}")


if __name__ == "__main__":
    main()
