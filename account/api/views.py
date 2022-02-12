# Stdlib imports
import jwt

# Core Django imports
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

# 3rd-party imports
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view, 
    renderer_classes, 
    permission_classes,
)
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.renderers import SwaggerUIRenderer, OpenAPIRenderer
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken

# Local imports
from .serializers import (
    UserListSerializer,
    CreateUserSerializer,
    UserRetrieveSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
)
from config.proj import tasks

User = get_user_model()


class UserViewSet(ListModelMixin, 
                  RetrieveModelMixin, 
                  DestroyModelMixin, 
                  UpdateModelMixin, 
                  GenericViewSet):
    def get_permissions(self):
        if self.action == ['list', 'retrieve', 'delete']:
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
    

@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    }), responses={201: 'done'})
@api_view(['POST'])
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
@permission_classes((AllowAny,))
def sign_in_view(request):
    serializer = CreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user_data = serializer.data
    user = User.objects.get(email=user_data['email'])
    user.is_active = False
    user.save()
    token = RefreshToken.for_user(user).access_token
    current_site = get_current_site(request).domain
    relativeLink = reverse('email_verify')
    absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
    email_body = 'Hi '+ user.username + \
        ' Use the link below to verify your email \n' + absurl
    data = {'email_body': email_body, 'to_email': user.email,
            'email_subject': 'Verify your email'}

    tasks.send_email.delay(data)
    return Response(user_data, status=status.HTTP_201_CREATED)


def verify_email(request):
    token = request.GET.get('token')
    try:
        payload = jwt.decode(token, settings.SECRET_KEY)
        user = User.objects.get(id=payload['user_id'])
        if not user.is_active:
            user.is_active = True
            user.save()
        return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
    except jwt.ExpiredSignatureError as identifier:
        return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.exceptions.DecodeError as identifier:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class UpdatePassword(APIView):
    """
    An endpoint for changing password.
    """

    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(("POST",))
def sign_out(request):
    try:
        Refresh_token = request.data["refresh"]
        token = RefreshToken(Refresh_token)
        token.blacklist()
        return Response("Successful Logout", status=status.HTTP_200_OK)
    except:
        Refresh_token == request.data["access"]
        return Response({"Msg": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
