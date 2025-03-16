import csv
from .models import Product, Category

def import_products_from_csv(file):
    """Функция импорта товаров из CSV."""
    decoded_file = file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded_file)
    created_count = 0

    for row in reader:
        category, _ = Category.objects.get_or_create(name=row['category'])
        Product.objects.create(
            name=row['name'],
            description=row['description'],
            price=row['price'],
            category=category
        )
        created_count += 1

    return f"Импортировано {created_count} товаров"
