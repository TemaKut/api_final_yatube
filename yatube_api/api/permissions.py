from rest_framework import permissions


class IsAuthenticatedAndIsAuthorOrReadOnly(permissions.BasePermission):
    """
    Тольк авторизованный пользователь может иметь доступ
    к незащищённым методам, остальные только читают.
    Только автор поста может менять данные.
    """

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            or request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):

        return (
            request.user == obj.author
            or request.method in permissions.SAFE_METHODS
        )
