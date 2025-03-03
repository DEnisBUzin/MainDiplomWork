from django.db import models
from products.models import Product
from django.contrib.auth.models import User


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Добавляем связь с пользователем
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True,)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'В ожидании'),
            ('processing', 'В обработке'),
            ('shipped', 'Отправлен'),
            ('delivered', 'Доставлен'),
            ('canceled', 'Отменён')
        ],
        default='pending'
    )

    def __str__(self):
        return f"Заказ {self.id} - {self.user.username}"
