from src.classes import Product, Category, Smartphone, LawnGrass
from src.utils import load_categories_from_json
from src.iterators import CategoryIterator


def main():
    """Основная функция для демонстрации работы классов"""

    print("=== Демонстрация работы классов ===")

    # Создаем обычные продукты
    product1 = Product("Смартфон", "Современный смартфон", 25000.50, 50)
    product2 = Product("Наушники", "Беспроводные наушники", 3500.00, 100)
    product3 = Product("Чехол", "Защитный чехол", 500.00, 200)

    # Создаем смартфоны
    smartphone1 = Smartphone(
        "iPhone 15 Pro", "Флагманский смартфон Apple", 99999.99, 10,
        "A17 Pro", "iPhone 15 Pro", 256, "Титан"
    )
    smartphone2 = Smartphone(
        "Samsung Galaxy S23 Ultra", "Флагманский смартфон Samsung", 89999.99, 8,
        "Snapdragon 8 Gen 2", "S23 Ultra", 512, "Черный"
    )

    # Создаем газонную траву
    grass1 = LawnGrass(
        "Газонная трава", "Смесь для солнечного газона", 1500.00, 50,
        "Россия", "7-14 дней", "Зеленый"
    )
    grass2 = LawnGrass(
        "Теневой газон", "Смесь для тенистого газона", 1800.00, 30,
        "Германия", "10-20 дней", "Темно-зеленый"
    )

    # Создаем категории
    electronics = Category("Электроника", "Различные электронные устройства", [product1, product2])
    smartphones = Category("Смартфоны", "Флагманские смартфоны", [smartphone1, smartphone2])
    garden = Category("Садоводство", "Товары для сада", [grass1, grass2])

    print(f"\nВсего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")

    print("\nИнформация о категориях:")
    print(f"- {electronics}")
    print(f"- {smartphones}")
    print(f"- {garden}")

    # Демонстрация __str__ продуктов
    print("\nИнформация о продуктах:")
    print(f"- {product1}")
    print(f"- {smartphone1}")
    print(f"- {grass1}")

    # Демонстрация __add__
    print("\nДемонстрация сложения продуктов:")
    try:
        total_cost = smartphone1 + smartphone2
        print(f"{smartphone1.name} + {smartphone2.name} = {total_cost} руб.")
    except TypeError as e:
        print(f"Ошибка: {e}")

    try:
        total_cost = grass1 + grass2
        print(f"{grass1.name} + {grass2.name} = {total_cost} руб.")
    except TypeError as e:
        print(f"Ошибка: {e}")

    # Демонстрация ошибки при сложении разных классов
    print("\nПопытка сложить смартфон и траву:")
    try:
        result = smartphone1 + grass1
        print(f"Результат: {result}")
    except TypeError as e:
        print(f"Ошибка: {e}")

    # Демонстрация добавления продуктов в категорию
    print("\nДобавление продуктов в категорию:")
    try:
        electronics.add_product(smartphone1)
        print(f"Смартфон успешно добавлен в категорию 'Электроника'")
    except TypeError as e:
        print(f"Ошибка: {e}")

    try:
        electronics.add_product("не продукт")
        print("Строка добавлена в категорию")
    except TypeError as e:
        print(f"Ошибка: {e}")

    # Демонстрация итератора
    print("\n=== Итерация по товарам категории 'Смартфоны' ===")
    iterator = CategoryIterator(smartphones)
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

