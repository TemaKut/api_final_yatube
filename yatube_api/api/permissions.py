from rest_framework import permissions
from rest_framework import serializers


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """ Тольк авторизованный пользователь может иметь доступ
    к незащищённым методам, остальные только читают. """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        else:
            if request.method in permissions.SAFE_METHODS:
                return True
            else:
                return False


class IsAuthorOrReadOnly(permissions.BasePermission):
    """ Только автор поста может менять данные. """

    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            if request.user == obj.author:
                return True
            else:
                return False
        else:
            return True


class NotFollowSelf(permissions.BasePermission):
    """ Запрещаем подписку на самого себя """

    def has_permission(self, request, view):
        if request.method == 'POST':
            if request.user.username == request.data.get('following'):
                raise serializers.ValidationError(
                    'Нельзя подписываться на себя')
            return True
        else:
            return True
