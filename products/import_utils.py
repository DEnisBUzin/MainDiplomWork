import csv
from io import TextIOWrapper
from django.core.exceptions import ValidationError
from .models import Product, Category


def import_products_from_csv(file):
    """Импортируем товары из CSV-файла"""
    try:
        decoded_file = TextIOWrapper(file, encoding='utf-8')
        reader = csv.reader(decoded_file)
        next(reader)  # Пропускаем заголовки

        created_count = 0
        for row in reader:
            if len(row) < 5:
                continue  # Пропускаем строки с недостаточным числом данных

            name, description, price, stock, category_name = row

            # Проверяем существование категории, если нет — создаем
            category, _ = Category.objects.get_or_create(name=category_name.strip())

            # Создаем или обновляем товар
            product, created = Product.objects.update_or_create(
                name=name.strip(),
                defaults={
                    'description': description.strip(),
                    'price': float(price),
                    'stock': int(stock),
                    'category': category,
                }
            )
            if created:
                created_count += 1

        return f'Импорт завершен. Добавлено новых товаров: {created_count}'
    except Exception as e:
        raise ValidationError(f'Ошибка при обработке CSV: {str(e)}')
