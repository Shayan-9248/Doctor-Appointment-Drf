# Core Django imports
from django.shortcuts import get_object_or_404

# 3rd-party imports
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    AllowAny,
)

from .serializers import (
    AppointmentSerializer,
)
from appointment.models import Appointment, Doctor


class AppointmentViewSet(ModelViewSet):
    def get_permissions(self):
        if self.action == "list":
            permission_classes = (IsAdminUser,)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Appointment.objects.select_related("doctor__doctor").all()

    def get_serializer_class(self):
        return AppointmentSerializer
