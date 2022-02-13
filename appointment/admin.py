from django.contrib import admin

from .models import Appointment, Doctor


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "id")


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("__str__", "id")
