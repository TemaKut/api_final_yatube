from rest_framework import permissions
from rest_framework import serializers


class IsAuthenticatedAndIsAuthorOrReadOnly(permissions.BasePermission):
    """
    Тольк авторизованный пользователь может иметь доступ
    к незащищённым методам, остальные только читают.
    Только автор поста может менять данные.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        else:
            if request.method in permissions.SAFE_METHODS:
                return True
            else:
                return False

    def has_object_permission(self, request, view, obj):

        return (
            request.method not in permissions.SAFE_METHODS
            and request.user == obj.author
            or request.method in permissions.SAFE_METHODS
        )


class NotFollowSelf(permissions.BasePermission):
    """ Запрещаем подписку на самого себя """

    def has_permission(self, request, view):
        if (request.method == 'POST'
                and request.user.username == request.data.get('following')):

            raise serializers.ValidationError(
                'Нельзя подписываться на себя')
        else:
            return True
