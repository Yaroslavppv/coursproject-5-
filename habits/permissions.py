from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnlyPublic(BasePermission):
    """
    Разрешает доступ автору привычки для любых операций (CRUD).
    Если привычка отмечена как публичная, остальные пользователи могут её только просматривать.
    """

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True

        if obj.is_public and request.method in SAFE_METHODS:
            return True

        return False
