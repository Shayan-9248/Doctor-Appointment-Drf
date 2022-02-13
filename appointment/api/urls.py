from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("appointment", views.AppointmentViewSet, basename="apppointment")

doctor_router = DefaultRouter()
doctor_router.register("doctor", views.DoctorViewSet, basename="doctor")

urlpatterns = [
    path("cancel-appointment/<int:pk>/", views.cancel_appointment, name='cancel_appointment'),
    path("", include(router.urls)),
    path("", include(doctor_router.urls)),
]
