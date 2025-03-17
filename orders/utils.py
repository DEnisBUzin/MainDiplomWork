from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from email.header import Header

def send_invoice_to_admin(order):
    """Отправка накладной администратору."""
    admin_email = "buzin.den@bk.ru"
    subject_admin = Header(f"Новый заказ #{order.id} от {order.user.username}", "utf-8").encode()

    message = render_to_string("emails/admin_invoice.html", {"order": order})

    send_mail(
        subject_admin,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [admin_email],
        fail_silently=False,
    )

    return print("Сообщение отправлено администратору!")

def send_order_confirmation(order):
    """Отправка подтверждения заказа клиенту."""
    subject_client = Header(f"Подтверждение заказа #{order.id}", "utf-8").encode()
    message = render_to_string("emails/order_confirmation.html", {"order": order})

    send_mail(
        subject_client,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.user.email],
        fail_silently=False,
    )

    return print("Сообщение отправлено клиенту!")
