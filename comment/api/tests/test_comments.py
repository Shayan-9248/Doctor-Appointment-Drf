# Stdlib imports
import json

# Core Django imports
from django.contrib.auth import get_user_model

# 3rd-party imports
from rest_framework import status
from model_bakery import baker
import pytest

# Local imports
from appointment.models import Appointment
from comment.models import Comment

User = get_user_model()


@pytest.mark.django_db
def test_get_all_comments_returns_200(api_client):
    appointment = baker.make(Appointment)
    response = api_client.get(f"/api/appointment/{appointment.id}/comment/")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_one_comment_returns_200(api_client):
    appointment = baker.make(Appointment)
    comment = baker.make(Comment)
    response = api_client.get(f"/api/appointment/{appointment.id}/comment/{comment.id}/")

    response_content = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert response_content.get("content") == comment.content


@pytest.mark.skip
def test_create_comment_if_user_is_authenticated(api_client, authenticate):
    authenticate()
    appointment = baker.make(Appointment)
    user = baker.make(User)

    response = api_client.post(f"/api/appointment/{appointment.id}/comment/", data={
        "author_id": user.id,
        "content": "hello",
        "content_type": appointment.get_content_type,
        "object_id": appointment.id
    })

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_comment_if_user_is_not_authenticated(api_client):
    appointment = baker.make(Appointment)
    user = baker.make(User)

    response = api_client.post(f"/api/appointment/{appointment.id}/comment/", data={
        "author_id": user.id,
        "content": "hello",
        "content_type": appointment.get_content_type,
        "object_id": appointment.id
    })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_comment_if_user_is_not_authenticated(api_client):
    appointment = baker.make(Appointment)
    user = baker.make(User)

    response = api_client.post(f"/api/appointment/{appointment.id}/comment/", data={
        "author_id": user.id,
        "content": "hello",
        "content_type": appointment.get_content_type,
        "object_id": appointment.id
    })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
