import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from todoapp.models import Task

@pytest.fixture
@pytest.mark.django_db
def test_user():
    return User.objects.create_user(username='chandru', password='chan@1234')


@pytest.mark.django_db
def test_signup_view():
    client = APIClient()
    url = reverse('signup')
    data = {'username': 'chandru', 'password': 'chan@1234'}
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK

    

@pytest.mark.django_db
def test_signup_view_invalid_data():
    client = APIClient()
    
    url = reverse('signup')
    invalid_data = {'username': 'chandru', 'password': 'chan'}

    response = client.post(url, invalid_data, format='json')
    print(response)

@pytest.mark.django_db
def test_custom_login_view_authenticated_user(test_user):
    client = APIClient()
    url = reverse('login')

    data = {
        'username': test_user.username,
        'password': "chan@1234"
    }

    response = client.post(url, data, format='json')
    
    assert response.status_code == status.HTTP_302_FOUND
  

@pytest.mark.django_db
def test_custom_login_view_invalid_credentials():
    client = APIClient()
    url = reverse('login')
    data = {'username': 'nonexistentuser', 'password': 'wrongpassword'}

    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_logout_view(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    url = reverse('logout')
    response = api_client.post(url)
    assert response.status_code == status.HTTP_200_OK
    
     
@pytest.fixture
def test_task(test_user):
    return Task.objects.create(user=test_user, title='Test Task', description='Description for test task')

@pytest.fixture
def api_client(test_user):
    client = APIClient()
    token, _ = Token.objects.get_or_create(user=test_user)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    return client

@pytest.mark.django_db
def test_todo_viewset_list(api_client, test_task):
    url = reverse('task-list')
    
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['title'] == test_task.title

@pytest.mark.django_db
def test_todo_viewset_create(api_client):
    url = reverse('task-list')
    data = {'title': 'New Task', 'description': 'Description for new task'}
    
    response = api_client.post(url, data, format='json')
    
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_todo_viewset_retrieve(api_client, test_task):
    url = reverse('task-detail', args=[test_task.id])
    
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == test_task.title
