from rest_framework.test import APIClient
from django.urls import reverse
import pytest

from accounts.models import User, Profile
from ..models import Task


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user1():
    user = User.objects.create_user(
        email="test1@admin.com", password="anvari@7768", is_verified=True
    )
    return user


@pytest.fixture
def common_user2():
    user = User.objects.create_user(
        email="test2@admin.com", password="anvari@7768", is_verified=True
    )
    return user


@pytest.mark.django_db
class TestTaskDetailApi:

    # GET/PUT/PATCH/DELETE task with no login user:
    def test_task_unauthorized_response_401(self, api_client, common_user1):
        api_client.force_login(user=common_user1)
        profile = Profile.objects.get(user=common_user1)
        task = Task.objects.create(
            author=profile,
            title="test",
            status=True,
        )
        api_client.logout()  # logout user for test unauthorized
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": task.id})

        # GET:
        response_get = api_client.get(url)
        assert response_get.status_code == 401

        # PUT
        data_put = {
            "title": "test2",
            "status": False,
        }
        response_put = api_client.put(url, data_put)
        assert response_put.status_code == 401

        # PATCH:
        data_patch = {
            "title": "test2",
        }
        response_patch = api_client.patch(url, data_patch)
        assert response_patch.status_code == 401

        # DELETE:
        response_delete = api_client.delete(url)
        assert response_delete.status_code == 401

    # GET/PUT/PATCH/DELETE task created by login user:
    def test_task_create_by_user(self, api_client, common_user1):
        api_client.force_login(user=common_user1)
        profile = Profile.objects.get(user=common_user1)
        task = Task.objects.create(
            author=profile,
            title="test",
            status=True,
        )
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": task.id})

        # GET:
        response_get = api_client.get(url)
        assert response_get.status_code == 200

        # PUT:
        data_put = {
            "title": "test2",
            "status": False,
        }
        response_put = api_client.put(url, data_put)
        assert response_put.status_code == 200

        # PATCH invalid data:
        data_patch_invalid = {
            "title": "test2",
        }
        response_patch = api_client.patch(url, data_patch_invalid)
        assert response_patch.status_code == 400

        # PATCH valid data:
        data_patch_valid = {
            "status": False,
        }
        response_patch = api_client.patch(url, data_patch_valid)
        assert response_patch.status_code == 200

        # DELETE:
        response_delete = api_client.delete(url)
        assert response_delete.status_code == 204

    # GET/PUT/PATCH/DELETE task not created by login user:
    def test_task_not_create_by_user(self, api_client, common_user1, common_user2):
        api_client.force_login(user=common_user2)
        profile = Profile.objects.get(user=common_user1)
        task = Task.objects.create(
            author=profile,
            title="test",
            status=True,
        )
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": task.id})

        # GET:
        response_get = api_client.get(url)
        assert response_get.status_code == 404

        # PUT
        data_put = {
            "title": "test2",
            "status": False,
        }
        response_put = api_client.put(url, data_put)
        assert response_put.status_code == 404

        # PATCH:
        data_patch = {
            "title": "test2",
        }
        response_patch = api_client.patch(url, data_patch)
        assert response_patch.status_code == 404

        # DELETE:
        response_delete = api_client.delete(url)
        assert response_delete.status_code == 404
