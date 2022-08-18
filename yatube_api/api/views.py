from rest_framework import viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from django.shortcuts import get_object_or_404

from posts.models import Post, Comment, Group, Follow
from .serializers import (PostSerializer, CommentSerializer,
                          GroupSerializer, FollowSerializer)
from .permissions import (IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly, NotFollowSelf)


class PostsViewSet(viewsets.ModelViewSet):
    """ Вью сет для публикаций. """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """ Добавляем автодобавление пользователя в авторы. """
        if serializer.is_valid():
            serializer.save(author=self.request.user)


class CommentsViewSet(viewsets.ModelViewSet):
    """ Вьюсет для комментариев к конкретному посту. """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return Comment.objects.filter(post=post)

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
    permission_classes = []


class FollowViewSet(viewsets.ViewSet):
    """ Вьюсет подписок. """
    permission_classes = (NotFollowSelf, IsAuthenticated)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=user',)

    def list(self, request):
        queryset = Follow.objects.all()
        serializer = FollowSerializer(queryset, many=True)

        return Response(serializer.data)

    def create(self, request):
        serializer = FollowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                user=self.request.user,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
