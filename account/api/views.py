from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet

from .serializers import (
    UserListSerializer,
    CreateNewUserSerializer,
    UserRetrieveSerializer,
    UserUpdateSerializer
)

User = get_user_model()


class UserViewSet(ModelViewSet):
    def get_queryset(self):
        return User.objects.all()
        
    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
