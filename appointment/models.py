# Core Django imports
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType

# Local imports
from comment.models import Comment


class TimeStamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Doctor(TimeStamp):
    class Gender(models.TextChoices):
        male = "m", "Male"
        female = "f", "Female"

    name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expertise = models.CharField(max_length=150)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=15, choices=Gender.choices)
    appointments = models.ManyToManyField(
        "Appointment", blank=True, related_name="appointments"
    )
    picture = models.ImageField(upload_to="media/%Y-%m-%d/", null=True, blank=True)

    def __str__(self):
        return f"{self.name.username} - {self.expertise}"


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
    comments = GenericRelation(Comment)

    def __str__(self):
        return f"{self.doctor} - {self.patient.username}"
    
    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type
