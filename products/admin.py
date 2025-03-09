from django.contrib import admin
from django.utils.html import format_html

from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock', 'stock_status', 'category', 'created_at')  # Добавил stock
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'category__name')
    autocomplete_fields = ('category',)
    ordering = ('-created_at',)
    list_editable = ('price', 'stock')  # Теперь stock есть в list_display

    def stock_status(self, obj):
        """Цветовая индикация остатка товаров."""
        color = "green" if obj.stock > 10 else "orange" if obj.stock > 0 else "red"
        return format_html(f'<span style="color: {color}; font-weight: bold;">{obj.stock}</span>')

    stock_status.short_description = "Остаток"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
