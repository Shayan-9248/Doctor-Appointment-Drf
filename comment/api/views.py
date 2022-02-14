from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import CommentSerializer
from comment.models import Comment


class CommentViewSet(ModelViewSet):
    def get_permissions(self):
        # if self.action == "list":
        #     permission_classes = (IsAdminUser,)
        # else:
        permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        return CommentSerializer
    
    def get_serializer_context(self):
        return {
            "user_id": self.request.user.id,
            "appointment_id": self.kwargs["appointment_pk"]
        }
    
    def get_queryset(self):
        return Comment.objects.all()
