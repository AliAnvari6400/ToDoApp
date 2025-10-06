from rest_framework.test import APIClient
from django.urls import reverse
import pytest

from accounts.models import User,Profile
from ..models import Task


@pytest.fixture
def api_client():
    client = APIClient()
    return client
    
@pytest.fixture
def common_user1():
    user = User.objects.create_user(email='test1@admin.com',password='anvari@7768',is_verified=True)
    return user
    
@pytest.fixture
def common_user2():
    user = User.objects.create_user(email='test2@admin.com',password='anvari@7768',is_verified=True)
    return user


@pytest.mark.django_db  
class TestTaskDetailApi:
    
    def test_get_task_response_401(self,api_client,common_user1): # GET unauthorized
        api_client.force_login(user = common_user1)
        profile = Profile.objects.get(user=common_user1)
        task = Task.objects.create(
            author = profile,
            title = 'test',
            status = True,
        )
        api_client.logout()
        url = reverse('todo:api-v1:task-detail',kwargs={'pk':task.id})
        response = api_client.get(url)
        assert response.status_code == 401
           
    def test_get_task_create_by_user_response_200(self,api_client,common_user1): # GET task created by login user
        api_client.force_login(user = common_user1)
        profile = Profile.objects.get(user=common_user1)
        task = Task.objects.create(
            author = profile,
            title = 'test',
            status = True,
        )
        url = reverse('todo:api-v1:task-detail',kwargs={'pk':task.id})
        response = api_client.get(url)
        assert response.status_code == 200
        
    def test_get_task_not_create_by_user_response_404(self,api_client,common_user1,common_user2): # GET task not created by login user
        api_client.force_login(user = common_user2)
        profile = Profile.objects.get(user=common_user1)
        task = Task.objects.create(
            author = profile,
            title = 'test',
            status = True,
        )
        url = reverse('todo:api-v1:task-detail',kwargs={'pk':task.id})
        response = api_client.get(url)
        assert response.status_code == 404   
    
    
        
        
    # def test_get_task_response_404(self,api_client,common_user,url): # GET with not exist object
    #     api_client.force_login(user = common_user)
    #     response = api_client.get(url)
    #     assert response.status_code == 404
        
    # def test_post_task_response_401(self,api_client,url):  # POST unauthorized
    #     data = {
    #         'title': 'test',
    #         'status': True,
    #     }
    #     response = api_client.post(url,data)
    #     assert response.status_code == 401
    
    # def test_post_task_response_201(self,api_client,common_user,url):  # POST with login user
    #     api_client.force_login(user = common_user)
    #     data = {
    #         'title': 'test',
    #         'status': True,
    #     }
    #     response = api_client.post(url,data)
    #     assert response.status_code == 201
    
    # def test_post_task_response_400(self,api_client,common_user,url):  # POST with incomplete data
    #     api_client.force_login(user = common_user)
    #     data = {
    #         'title':'' ,
    #         'status': 'test',
    #     }
    #     response = api_client.post(url,data)
    #     assert response.status_code == 400
