from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)

from .serializers import (
    UserListSerializer,
    CreateNewUserSerializer,
    UserRetrieveSerializer,
    UserUpdateSerializer
)

User = get_user_model()


class UserViewSet(ModelViewSet):
    def get_permissions(self):
        if self.action == ['list', 'retrieve']:
            permission_classes = (IsAdminUser,)
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        elif self.action == 'retrieve':
            return UserRetrieveSerializer
