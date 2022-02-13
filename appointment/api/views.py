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
from rest_framework import status

# Local imports
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
        return Appointment.objects.select_related("doctor__name").all()

    def get_serializer_class(self):
        return AppointmentSerializer
    
    def get_serializer_context(self):
        return {'user_id': self.request.user.id}
    
    # @action(detail=False, methods=['GET'])
    # def me(self, request):
    #     # appointment = get_object_or_404(Appointment, patient_id=request.user.id)
    #     appointment = Appointment.objects.get(patient_id=request.user.id)
    #     serializer = AppointmentSerializer(appointment)
    #     return Response(serializer.data)


@permission_classes((IsAuthenticated,))
@api_view(('GET',))
def cancel_appointment(request, pk):
    appointment = Appointment.objects.get(pk=pk)
    appointment.status = 'c'
    appointment.save()
    return Response('Appointment Canceled')
