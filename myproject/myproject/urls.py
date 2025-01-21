from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from insta.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('posts/', PostViewSet.as_view({'get': 'list', 'post': 'create'}), name='post_list_create'),
    path('users/<str:username>/follow/', UserViewSet.as_view({'post': 'follow'}), name='user_follow'),
    path('users/<str:username>/unfollow/', UserViewSet.as_view({'post': 'unfollow'}), name='user_unfollow'),
    path('users/<str:username>/followers/', UserViewSet.as_view({'get': 'followers'}), name='user_followers'),
    path('users/<str:username>/following/', UserViewSet.as_view({'get': 'following'}), name='user_following'),
    path('users/actions/', UserViewSet.as_view({'get': 'actions'}), name='user_actions'),
]
