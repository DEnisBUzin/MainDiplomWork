from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView
from .models import Order
from .serializers import OrderSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .permissions import IsOwnerOrReadOnly


class OrderDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)  # Только заказы текущего пользователя


class OrderListCreateView(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)  # Показываем только заказы текущего пользователя

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Автоматически назначаем пользователя

