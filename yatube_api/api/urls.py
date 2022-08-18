from django.urls import include, path

from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

router.register('posts', views.PostsViewSet, basename='posts')
router.register(r'^posts/(?P<post_id>\d+)/comments',
                views.CommentsViewSet, basename='comments')
router.register('groups', views.GroupViewSet, basename='groups')
router.register('follow', views.FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(router.urls)),
]
