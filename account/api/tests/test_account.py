from django.contrib.auth import get_user_model
from rest_framework import status
from model_bakery import baker
import pytest

User = get_user_model()


@pytest.mark.django_db
def test_get_all_users_if_user_is_staff(api_client, authenticate):
    authenticate(is_staff=True)

    response = api_client.get("api/users/")

    return response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_all_users_if_user_is_not_staff(api_client, authenticate):
    authenticate()

    response = api_client.get("api/users/")

    return response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_user_if_user_exists(api_client, authenticate):
    user = baker.make(User)
    authenticate()

    response = api_client.get(f"api/users/{user.id}")

    return response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_user_if_user_does_not_exists(api_client, authenticate):
    authenticate()

    response = api_client.get(f"api/users/90/")

    return response.status_code == status.HTTP_404_NOT_FOUND
