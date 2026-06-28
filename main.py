from src.classes import Product, Category, Smartphone, LawnGrass, Order
from src.utils import load_categories_from_json
from src.iterators import CategoryIterator


def main():
    """Основная функция для демонстрации работы классов"""

    print("=== Демонстрация работы классов ===")
    print("\nПри создании объектов миксин будет выводить информацию:")
    print("-" * 50)

    try:
        # Создаем обычные продукты
        product1 = Product("Смартфон", "Современный смартфон", 25000.50, 50)
        product2 = Product("Наушники", "Беспроводные наушники", 3500.00, 100)
        product3 = Product("Чехол", "Защитный чехол", 500.00, 200)

        print("-" * 50)

        # Создаем смартфоны
        smartphone1 = Smartphone(
            "iPhone 15 Pro", "Флагманский смартфон Apple", 99999.99, 10,
            "A17 Pro", "iPhone 15 Pro", 256, "Титан"
        )
        smartphone2 = Smartphone(
            "Samsung Galaxy S23 Ultra", "Флагманский смартфон Samsung", 89999.99, 8,
            "Snapdragon 8 Gen 2", "S23 Ultra", 512, "Черный"
        )

        print("-" * 50)

        # Создаем газонную траву
        grass1 = LawnGrass(
            "Газонная трава", "Смесь для солнечного газона", 1500.00, 50,
            "Россия", "7-14 дней", "Зеленый"
        )
        grass2 = LawnGrass(
            "Теневой газон", "Смесь для тенистого газона", 1800.00, 30,
            "Германия", "10-20 дней", "Темно-зеленый"
        )

        print("-" * 50)

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

        # Демонстрация средней цены
        print("\n=== Средняя цена товаров в категориях ===")
        print(f"Электроника: {electronics.average_price():.2f} руб.")
        print(f"Смартфоны: {smartphones.average_price():.2f} руб.")
        print(f"Садоводство: {garden.average_price():.2f} руб.")

        # Демонстрация обработки исключений
        print("\n=== Обработка исключений ===")
        try:
            print("Попытка создать товар с нулевым количеством:")
            product_zero = Product("Несуществующий товар", "Описание", 100, 0)
        except ValueError as e:
            print(f"Ошибка: {e}")

        try:
            print("\nПопытка создать смартфон с нулевым количеством:")
            smartphone_zero = Smartphone(
                "iPhone", "Флагман", 99999.99, 0,
                "A17 Pro", "15 Pro", 256, "Титан"
            )
        except ValueError as e:
            print(f"Ошибка: {e}")

        # Демонстрация заказа (дополнительное задание)
        print("\n=== Демонстрация заказа ===")
        try:
            order = Order(smartphone1, 2)
            print(f"{order}")

            # Попытка создать заказ с нулевым количеством
            print("\nПопытка создать заказ с нулевым количеством:")
            order_zero = Order(smartphone1, 0)
        except ValueError as e:
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

    except ValueError as e:
        print(f"\nОшибка при создании продукта: {e}")
    except Exception as e:
        print(f"\nНеожиданная ошибка: {e}")


if __name__ == "__main__":
    main()
