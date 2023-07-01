from rest_framework import permissions


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
            or request.user.is_moderator
            or request.user.is_admin
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
            or request.user.is_admin
        )


class IsAdmin(permissions.BasePermission):
    """только для админа и суперюзера"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.is_admin
            )
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """только админимтратор или суперюзер или чтение"""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.is_admin
                    or request.user.is_superuser)))
