from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_invoice_to_admin(order):
    """Отправка накладной администратору."""
    admin_email = "buzin.den@bk.ru"
    subject = f"Новый заказ #{order.id} от {order.user.username}"

    message = render_to_string("emails/admin_invoice.html", {"order": order})

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [admin_email],
        fail_silently=False,
    )

    return print("Сообщение отправлено администратору!")

def send_order_confirmation(order):
    """Отправка подтверждения заказа клиенту."""
    subject = f"Подтверждение заказа #{order.id}"
    message = render_to_string("emails/order_confirmation.html", {"order": order})

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.user.email],
        fail_silently=False,
    )

    return print("Сообщение отправлено клиенту!")
