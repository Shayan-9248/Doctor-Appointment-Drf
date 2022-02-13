from rest_framework import serializers
import appointment

from appointment.models import Doctor, Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    doctor = serializers.StringRelatedField()

    class Meta:
        model = Appointment
        fields = ("doctor", "date")

    def create(self, validated_data):
        doctor_id = validated_data.get("doctor").id
        appointment = Appointment(**validated_data)
        appointment.save()

        doctor = Doctor.objects.get(doctor_id=doctor_id)
        doctor.appointments.add(appointment)
        return validated_data
