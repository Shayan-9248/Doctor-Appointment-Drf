from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import (
    CommentSerializer,
    CommentReplySerializer,
)
from comment.models import Comment


class CommentViewSet(ModelViewSet):
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        return CommentSerializer

    def get_serializer_context(self):
        return {
            "user_id": self.request.user.id,
            "appointment_id": self.kwargs["appointment_pk"],
        }

    def get_queryset(self):
        return Comment.objects.select_related("author").all()


class CommentReplyViewSet(ModelViewSet):
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        return CommentReplySerializer

    def get_serializer_context(self):
        return {
            "user_id": self.request.user.id,
            "appointment_id": self.kwargs["appointment_pk"],
            "comment_id": self.kwargs["comment_pk"],
        }

    def get_queryset(self):
        return Comment.objects.select_related("parent").all()
