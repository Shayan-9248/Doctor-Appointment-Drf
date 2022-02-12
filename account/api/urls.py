from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

user_router = DefaultRouter()
user_router.register('', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(user_router.urls)),
]
