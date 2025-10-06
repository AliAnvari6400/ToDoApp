from rest_framework.test import APIClient
from django.urls import reverse
import pytest

from accounts.models import User

@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def common_user():
    user = User.objects.create_user(email='test@admin.com',password='anvari@7768',is_verified=True)
    return user
    

@pytest.mark.django_db  
class TestTaskApi:
    
    def test_get_task_response_401_status(self,api_client): # GET unauthorized
        url = reverse('todo:api-v1:task-list')
        response = api_client.get(url)
        assert response.status_code == 401
           
    def test_get_task_response_200_status(self,api_client,common_user): # GET with login user
        api_client.force_login(user = common_user)
        url = reverse('todo:api-v1:task-list')
        response = api_client.get(url)
        assert response.status_code == 200
        
    
    