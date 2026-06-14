from src.classes import Product, Category
from src.utils import load_categories_from_json, check_and_merge_product


def main():
    """Основная функция для демонстрации работы классов"""

    print("=== Демонстрация работы обновленных классов ===")

    # Создаем продукты через класс-метод
    product1_data = {
        'name': 'Смартфон',
        'description': 'Современный Смартфон',
        'price': 25000.50,
        'quantity': 50
    }
    product1 = Product.new_product(product1_data)
    print(f"Создан продукт: {product1}")

    # Тестируем сеттер цены
    print("\n=== Тестирование сеттера цены ===")
    print(f"Текущая цена: {product1.price}")

   # Пытаемся установить цену меньше нуля
    product1.price = -1000
    print(f"Попытка установить цену -1000 : {product1.price}")

    # Устанавливаем правильную цену
    product1.price = 23000
    print(f"Установлена правильная цена 23000: {product1.price}")

    # Создаем категорию
    print("\n=== Создание категории ===")
    electronics = Category("Электроника", "Различная электроника")
    print(f"Создана категория: {electronics.name}")

    # Добавляем продукт в категорию через метод add_product
    print("\n=== Добавление продукта в категорию ===")
    electronics.add_product(product1)
    print(f"Добавлен продукт: {product1.name}")

    # Создаем еще один продукт
    product2 = Product.new_product({
        'name': 'Наушники',
        'description': 'Беспроводные наушники',
        'price': 3500.00,
        'quantity': 100
    })

    # Добавляем продукт в категорию
    electronics.add_product(product2)
    print(f"Добавлен продукт: {product2.name}")

    # Выводим список товаров через геттер
    print("\n=== Список товаров в категории ===")
    print(electronics.products)

    # Проверяем счетчики
    print(f"\n=== Статистика ===")
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего продуктов: {Category.product_count}")

    # Демонстрация загрузки из JSON (если файл существует)
    print("\n=== Загрузка данных из JSON ===")
    try:
        categories = load_categories_from_json('data/products.json')
        print(f"Загружено категорий: {len(categories)}")
        for category in categories:
            print(f"\nКатегория: {category.name}")
            print(category.products)
    except FileNotFoundError:
        print("Файл data/products.json не найден")


if __name__ == "__main__":
    main()

