from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from .utils import send_invoice_to_admin, send_order_confirmation


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('canceled', 'Отменён'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Заказ {self.id} - {self.user.username}"

    def save(self, *args, **kwargs):
        is_new = self._state.adding  # Проверяем, создаётся ли новый заказ
        super().save(*args, **kwargs)

        if is_new:
            send_invoice_to_admin(self)  # Отправляем накладную админу
            send_order_confirmation(self)  # Отправляем подтверждение клиенту
