from django.shortcuts import get_object_or_404

from rest_framework import serializers

from appointment.models import Doctor, Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ("doctor", "date")

    def create(self, validated_data):
        user_id = self.context.get('user_id')
        doctor = validated_data.get("doctor").id

        appointment = Appointment(patient_id=user_id ,**validated_data)
        appointment.save()

        doctor = get_object_or_404(Doctor, pk=doctor)
        doctor.appointments.add(appointment)
        return validated_data


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('name', 'expertise', 'age', 'gender', 'picture')
