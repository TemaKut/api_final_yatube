from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router_v1 = SimpleRouter()

router_v1.register('posts', views.PostsViewSet, basename='posts')
router_v1.register(r'^posts/(?P<post_id>\d+)/comments',
                   views.CommentsViewSet, basename='comments')
router_v1.register('groups', views.GroupViewSet, basename='groups')
router_v1.register('follow', views.FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router_v1.urls)),
]
