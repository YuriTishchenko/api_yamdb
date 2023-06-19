from rest_framework import permissions

from reviews.constants import ADMIN, MODERATOR


class IsUserOrModeratorOrReadOnly(permissions.BasePermission):
    """
    Для пользователя, модератора, администратора
    и суперпользователя или чтение
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_superuser
            or request.user.role == MODERATOR
            or request.user.role == ADMIN
        )


class IsUserOrAdminOrReadOnly(permissions.BasePermission):
    """
    Для пользователя, администратора
    и суперпользователя или чтение
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_superuser
            or request.user.role == ADMIN
        )


class IsAdmin(permissions.BasePermission):
    """только для админа и суперюзера"""

    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or request.user.role == ADMIN
        )
