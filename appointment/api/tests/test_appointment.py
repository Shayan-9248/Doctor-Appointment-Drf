# Stdlib imports
import json

# 3rd-party imports
from rest_framework import status
from model_bakery import baker
import pytest

# Local imports
from appointment.models import Appointment


@pytest.mark.django_db
def test_get_all_appointments_if_user_is_staff(api_client, authenticate):
    authenticate(is_staff=True)

    response = api_client.get("/api/appointment/")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_all_appointments_if_user_is_not_staff(api_client, authenticate):
    authenticate()

    response = api_client.get("/api/appointment/")

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_get_appointment_if_value_exists(api_client, authenticate):
    authenticate(is_staff=True)
    appointment = baker.make(Appointment)

    response = api_client.get(f"/api/appointment/{appointment.id}/")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_appointment_if_value_does_not_exists(api_client, authenticate):
    authenticate(is_staff=True)

    response = api_client.get(f"/api/appointment/77/")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_create_appointment_if_data_is_valid(api_client, authenticate):
    authenticate()

    response = api_client.post(
        "/api/appointment/", data={"doctor": 1, "patient": 2, "date": "2022-2-13"}
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_appointment_if_data_is_invalid(api_client, authenticate):
    authenticate()

    response = api_client.post(
        "/api/appointment/", data={"patient": 2, "date": "2022-2-13"}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert json.loads(response.content) == {"doctor": ["This field is required."]}
