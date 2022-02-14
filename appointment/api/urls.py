from django.urls import path, include

from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register("appointment", views.AppointmentViewSet, basename="apppointment")

doctor_router = SimpleRouter()
doctor_router.register("doctor", views.DoctorViewSet, basename="doctor")

urlpatterns = [
    path(
        "cancel-appointment/<int:pk>/",
        views.cancel_appointment,
        name="cancel_appointment",
    ),
    path("", include(router.urls)),
    path("", include(doctor_router.urls)),
]
