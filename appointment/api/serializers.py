# Core Django imports
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage

# 3rd-party imports
from rest_framework import serializers

# Local imports
from appointment.models import Doctor, Appointment
from appointment.tasks import send_email_appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ("doctor", "date")

    def create(self, validated_data):
        user_id = self.context.get('user_id')
        user = self.context.get('user')
        doctor = validated_data.get("doctor").id
        doctor_name = validated_data.get("doctor")
        date = validated_data.get('date')

        appointment = Appointment(patient_id=user_id ,**validated_data)
        appointment.save()
        email_body = (
            "Hi "
            + user.username
            + f" \nYou have an appointment with {doctor_name} on {date}"
        )
        doctor = get_object_or_404(Doctor, pk=doctor)
        doctor.appointments.add(appointment)

        email = EmailMessage(
            subject='Doctor Appointment',
            body=email_body,
            to=[user.email]
        )
        send_email_appointment.delay(email)
        return validated_data


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('name', 'expertise', 'age', 'gender', 'picture')
