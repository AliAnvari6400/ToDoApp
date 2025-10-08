from rest_framework.test import APIClient
from django.urls import reverse
import pytest

from accounts.models import User


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def url():
    url = reverse("todo:api-v1:task-list")
    return url


@pytest.fixture
def common_user():
    user = User.objects.create_user(
        email="test@admin.com", password="anvari@7768", is_verified=True
    )
    return user


@pytest.mark.django_db
class TestTaskApi:

    def test_get_task_response_401(self, api_client, url):  # GET unauthorized
        response = api_client.get(url)
        assert response.status_code == 401

    def test_get_task_response_200(
        self, api_client, common_user, url
    ):  # GET with login user
        api_client.force_login(user=common_user)
        response = api_client.get(url)
        assert response.status_code == 200

    def test_post_task_response_401(self, api_client, url):  # POST unauthorized
        data = {
            "title": "test",
            "status": True,
        }
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_post_task_response_201(
        self, api_client, common_user, url
    ):  # POST with login user
        api_client.force_login(user=common_user)
        data = {
            "title": "test",
            "status": True,
        }
        response = api_client.post(url, data)
        assert response.status_code == 201

    def test_post_task_response_400(
        self, api_client, common_user, url
    ):  # POST with incomplete data
        api_client.force_login(user=common_user)
        data = {
            "title": "",
            "status": "test",
        }
        response = api_client.post(url, data)
        assert response.status_code == 400
