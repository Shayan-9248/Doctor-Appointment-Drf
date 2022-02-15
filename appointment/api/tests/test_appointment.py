# Stdlib imports
import json

# 3rd-party imports
from rest_framework import status
from model_bakery import baker
import pytest

# Local imports
from appointment.models import Appointment, Doctor


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


@pytest.mark.django_db
def test_create_doctor_if_user_is_staff(api_client, authenticate):
    authenticate(is_staff=True)

    response = api_client.post("/api/doctor/", data={
        "name": 1,
        "expertise": "test",
        "age": 40,
        "gender": "m"
    })

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_doctor_if_user_is_not_staff(api_client, authenticate):
    authenticate()

    response = api_client.post("/api/doctor/", data={
        "name": 1,
        "expertise": "test",
        "age": 40,
        "gender": "m"
    })

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_create_doctor_if_data_is_invalid(api_client, authenticate):
    authenticate(is_staff=True)

    response = api_client.post("/api/doctor/", data={
        "expertise": "test",
        "age": 40,
        "gender": "m"
    })

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert json.loads(response.content) == {"name": ["This field is required."]}


@pytest.mark.django_db
def test_get_all_doctors_returns_200(api_client, authenticate):
    authenticate(is_staff=True)

    response = api_client.get("/api/doctor/")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_one_doctor_returns_200(api_client, authenticate):
    authenticate(is_staff=True)
    doctor = baker.make(Doctor)

    response = api_client.get(f"/api/doctor/{doctor.id}/")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_delete_doctor_returns_204(api_client, authenticate):
    authenticate(is_staff=True)
    doctor = baker.make(Doctor)

    response = api_client.delete(f"/api/doctor/{doctor.id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_update_doctor_returns_200(api_client, authenticate):
    authenticate(is_staff=True)
    doctor = baker.make(Doctor)

    response = api_client.patch(f"/api/doctor/{doctor.id}/", data={
        "age": 42
    })

    assert response.status_code == status.HTTP_200_OK
