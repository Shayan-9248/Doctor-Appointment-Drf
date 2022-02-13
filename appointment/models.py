# Core Django imports
from django.db import models
from django.conf import settings
from django.utils.text import slugify


class TimeStamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Doctor(TimeStamp):
    class Gender(models.TextChoices):
        male = "m", "Male"
        female = "f", "Female"

    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expertise = models.CharField(max_length=150)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=15, choices=Gender.choices)
    appointments = models.ManyToManyField(
        "Appointment", blank=True, related_name="appointments"
    )
    picture = models.ImageField(upload_to="media/%Y-%m-%d/", null=True, blank=True)

    def __str__(self):
        return f"{self.doctor.username} - {self.expertise}"


class Appointment(TimeStamp):
    class Status(models.TextChoices):
        accepted = "a", "Accepted"
        canceled = "c", "Canceled"
        finished = "f", "Finished"

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True
    )
    status = models.CharField(
        max_length=15, default=Status.accepted, choices=Status.choices
    )
    date = models.DateField()

    def __str__(self):
        return f"{self.doctor} - {self.category}"
