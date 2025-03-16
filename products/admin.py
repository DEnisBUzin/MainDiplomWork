from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import render, redirect
from django.utils.html import format_html

from .models import Product, Category
from .forms import ProductImportForm
from .utils import import_products_from_csv


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock', 'stock_status', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'category__name')
    autocomplete_fields = ('category',)
    ordering = ('-created_at',)
    list_editable = ('price', 'stock')
    change_list_template = "admin/products/product_changelist.html"  # Подключаем кастомный шаблон

    def get_urls(self):
        """Добавляем кастомный URL для импорта товаров."""
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name='product_import_csv')
        ]
        return custom_urls + urls

    def import_csv(self, request):
        """Обработчик импорта товаров из CSV."""
        if request.method == 'POST':
            print("📩 Запрос получен!")  # Лог в консоли

            form = ProductImportForm(request.POST, request.FILES)
            if form.is_valid():
                print("✅ Форма валидна!")  # Проверяем, валидна ли форма

                file = request.FILES['file']
                print(f"📂 Загружен файл: {file.name}")

                try:
                    message = import_products_from_csv(file)
                    self.message_user(request, message, messages.SUCCESS)
                except Exception as e:
                    print(f"❌ Ошибка: {e}")
                    self.message_user(request, str(e), messages.ERROR)

                return redirect("..")

            else:
                print("❌ Форма не валидна!")
                self.message_user(request, "Ошибка валидации", messages.ERROR)

        form = ProductImportForm()
        context = {'form': form, 'title': 'Импорт товаров'}
        return render(request, 'admin/import_form.html', context)

    def stock_status(self, obj):
        """Цветовая индикация остатка товаров."""
        color = "green" if obj.stock > 10 else "orange" if obj.stock > 0 else "red"
        return format_html(f'<span style="color: {color}; font-weight: bold;">{obj.stock}</span>')

    stock_status.short_description = "Остаток"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
