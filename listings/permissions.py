from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Разрешение, позволяющее редактировать/удалять объявление только его владельцу."""

    def has_object_permission(self, request, view, obj):
        # Безопасные методы (GET, HEAD, OPTIONS) доступны всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Только создатель объявления может изменять/удалять
        return obj.creator == request.user