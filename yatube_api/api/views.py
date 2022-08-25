from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters, mixins, viewsets
from django.shortcuts import get_object_or_404

from posts.models import Post, Comment, Group, Follow
from .serializers import (PostSerializer, CommentSerializer,
                          GroupSerializer, FollowSerializer)
from .permissions import (
    IsAuthenticatedAndIsAuthorOrReadOnly,
)


class PostsViewSet(viewsets.ModelViewSet):
    """ Вью сет для публикаций. """

    queryset = Post.objects.all().select_related('author', 'group')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedAndIsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """ Добавляем автодобавление пользователя в авторы. """
        if serializer.is_valid():
            serializer.save(author=self.request.user)


class CommentsViewSet(viewsets.ModelViewSet):
    """ Вьюсет для комментариев к конкретному посту. """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedAndIsAuthorOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))

        return Comment.objects.filter(post=post).select_related(
            'post', 'author'
        )

    def perform_create(self, serializer):
        """В момент отправки метода POST
        устанавливаем в качестве автора и поста свои значения."""
        post = get_object_or_404(Post, id=self.kwargs.get("post_id"))
        if serializer.is_valid():
            serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ Вьюсет Групп. Только читаем. """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """ Вьюсет подписок. """
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=following__username']

    def get_queryset(self):

        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """ Добавляем автодобавление пользователя в подписавшегося. """
        if serializer.is_valid():
            serializer.save(user=self.request.user)
