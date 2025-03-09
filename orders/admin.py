from django.contrib import admin
from django.utils.html import format_html
from .models import Order
from products.models import Product


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'total_price', 'status_colored', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'product__name')
    autocomplete_fields = ('user', 'product')  # Автозаполнение полей
    ordering = ('-created_at',)

    def total_price(self, obj):
        """Метод для отображения общей стоимости заказа."""
        return f"{obj.product.price * obj.quantity:.2f} ₽"

    total_price.short_description = "Сумма заказа"

    def status_colored(self, obj):
        """Цветовая индикация статусов заказов."""
        colors = {
            "pending": "gray",
            "processing": "blue",
            "shipped": "orange",
            "delivered": "green",
            "canceled": "red",
        }
        color = colors.get(obj.status, "black")
        return format_html(f'<span style="color: {color}; font-weight: bold;">{obj.get_status_display()}</span>')

    status_colored.short_description = "Статус"

