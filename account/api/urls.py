from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

user_router = DefaultRouter()
user_router.register('users', views.UserViewSet, basename='user')

user_profile = DefaultRouter()
user_profile.register('', views.UserProfileViewSet, basename='user_update')

urlpatterns = [
    path('sign-up/', views.SignUpView.as_view(), name='sign_up'),
    path('email-verify/', views.VerifyEmail.as_view(), name='email_verify'),
    path('update-password/', views.UpdatePassword.as_view(), name='update_pass'),
    path('sign-out/', views.sign_out, name='sign_out'),
    path('', include(user_router.urls)),
    path('', include(user_profile.urls)),
]
