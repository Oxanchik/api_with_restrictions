from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db import models

from .models import Advertisement
from .serializers import AdvertisementSerializer
from .filters import AdvertisementFilter
from .permissions import IsOwnerOrReadOnly


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = AdvertisementFilter
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']  # Сортировка по умолчанию: сначала новые


    def get_permissions(self):
        """Получение прав для действий."""

        # Для создания, обновления и удаления -> требуется авторизация
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]

        # Для обновления и удаления -> также проверяются права
        if self.action in ["update", "partial_update", "destroy"]:
            permission_classes.append(IsOwnerOrReadOnly)

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Фильтрация набора запросов:
        - Удаленные записи видны только их создателю
        - Анонимные пользователи видят только записи в состояниях OPEN и CLOSED

        """
        queryset = super().get_queryset()

        # Если пользователь авторизован
        if self.request.user.is_authenticated:
            # Просмотр черновиков: только для создателей
            return queryset.filter(
                models.Q(creator=self.request.user) |
                ~models.Q(status='DRAFT')
            )

        # Анонимные пользователи: не видят черновиков
        return queryset.exclude(status='DRAFT')