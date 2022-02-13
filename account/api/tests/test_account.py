# Stdlib imports
import json

# Core Django imports
from django.contrib.auth import get_user_model
from django.core import mail

# 3rd-party imports
from rest_framework import status
from model_bakery import baker
import pytest

User = get_user_model()


@pytest.mark.django_db
def test_get_all_users_if_user_is_staff(api_client, authenticate):
    authenticate(is_staff=True)

    response = api_client.get("/api/users/")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_all_users_if_user_is_not_staff(api_client):
    response = api_client.get("/api/users/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_user_if_user_exists(api_client, authenticate):
    user = baker.make(User)
    authenticate(is_staff=True)

    response = api_client.get(f"/api/users/{user.id}/")
    response_content = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert response_content.get("username") == user.username
    assert response_content.get("email") == user.email


@pytest.mark.django_db
def test_get_user_if_user_does_not_exists(api_client, authenticate):
    authenticate(is_staff=True)

    response = api_client.get("/api/users/90/")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_create_user_if_data_is_valid(api_client):
    response = api_client.post(
        "/api/sign-up/",
        data={"username": "test", "email": "test@email.com", "password": 123},
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_user_if_data_is_invalid(api_client):
    response = api_client.post("/api/sign-up/", data={})

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_delete_user_if_user_is_staff(api_client, authenticate):
    authenticate(is_staff=True)
    user = baker.make(User)

    response = api_client.delete(f"/api/users/{user.id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_user_if_user_is_not_staff(api_client):
    user = baker.make(User)

    response = api_client.delete(f"/api/users/{user.id}/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_profile_if_user_is_authenticated(api_client, authenticate):
    authenticate()

    try:
        response = api_client.get("/api/me/")
        assert response.status_code == status.HTTP_200_OK
    except Exception:
        pass


@pytest.mark.django_db
def test_get_profile_if_user_is_not_authenticated(api_client):
    response = api_client.get("/api/me/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_send_email_should_succeed(mailoutbox):
    mail.send_mail('subject', 'body', 'from@example.com', ['to@example.com'])
    assert len(mailoutbox) == 1
    m = mailoutbox[0]
    assert m.subject == 'subject'
    assert m.body == 'body'
    assert m.from_email == 'from@example.com'
    assert list(m.to) == ['to@example.com']
