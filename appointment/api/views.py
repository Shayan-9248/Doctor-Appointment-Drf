# Core Django imports
from django.shortcuts import get_object_or_404

# 3rd-party imports
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

# Local imports
from .serializers import (
    AppointmentSerializer,
    DoctorSerializer,
)
from appointment.models import Appointment, Doctor
from .permissions import PatientPermission


class AppointmentViewSet(ModelViewSet):
    def get_permissions(self):
        if self.action == "list":
            permission_classes = (IsAdminUser,)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Appointment.objects.select_related("doctor__name").all()

    def get_serializer_class(self):
        return AppointmentSerializer
    
    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


@api_view(('GET',))
@permission_classes((IsAuthenticated,))
def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if appointment.patient.id == request.user.id:
        appointment.status = 'c'
        appointment.save()
        return Response('Appointment Canceled', 200)
    else:
        return Response('You do not own this appointment!', 403)


class DoctorViewSet(ModelViewSet):
    def get_permissions(self):
        permission_classes = (IsAdminUser,)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Doctor.objects.select_related("name").all()
    
    def get_serializer_class(self):
        return DoctorSerializer
