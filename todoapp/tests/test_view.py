import pytest,json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from todoapp.models import Subscription, SubscriptionPlan

@pytest.fixture
def authenticated_user():
    user = User.objects.create_user(username='testuser', password='testpass')
    return user

@pytest.fixture
def api_client():
    return APIClient()



@pytest.fixture
def subscription(authenticated_user):
    return User.objects.create(user=authenticated_user, plan='Basic')


@pytest.fixture
def authenticated_client(authenticated_user):
    client = APIClient()
    client.force_authenticate(user=authenticated_user)
    return client

# Tests
@pytest.mark.django_db
def test_signup_view(api_client):
    url = reverse('signup')
    data = {'username': 'testuser', 'password': 'testpass'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_signup_view_invalid_data(api_client):
    url = reverse('signup')
    invalid_data = {'username': 'ch', 'password': 'chan'}
    response = api_client.post(url, invalid_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_custom_login_view_authenticated_user(api_client, authenticated_user):
    url = reverse('login')
    data = {'username': authenticated_user.username, 'password': "testpass"}
    response = api_client.post(url, data, format='json')
    
    assert response.status_code == status.HTTP_302_FOUND
    assert response.url == reverse('task-list')

@pytest.mark.django_db
def test_custom_login_view_invalid_credentials(api_client):
    url = reverse('login')
    data = {'username': 'nonexistentuser', 'password': 'wrongpassword'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_logout_view(authenticated_client):
    url = reverse('logout')
    response = authenticated_client.post(url, follow=True)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_subscription_create(api_client, authenticated_user):
    api_client.force_authenticate(user=authenticated_user)
    url = reverse('subscription-list')
    data = {'plan': SubscriptionPlan.ADVANCED}
    response = api_client.post(url, data=json.dumps(data), content_type='application/json') 
    assert response.status_code == status.HTTP_200_OK
    subscription = Subscription.objects.get(user=authenticated_user)
    assert subscription.plan == SubscriptionPlan.ADVANCED


@pytest.mark.django_db
def test_subscription_update(api_client, authenticated_user):
    api_client.force_authenticate(user=authenticated_user)

    subscription, created = Subscription.objects.get_or_create(user=authenticated_user, defaults={'plan': SubscriptionPlan.BASIC})
    url = reverse('subscription-detail', args=[subscription.id])
    data = {'plan': SubscriptionPlan.ADVANCED}
    response = api_client.patch(url, data=json.dumps(data), content_type='application/json')
    assert response.status_code == status.HTTP_200_OK
    subscription.refresh_from_db()
    assert subscription.plan == SubscriptionPlan.ADVANCED
    
@pytest.mark.django_db
def test_todo_create_unauthenticated(api_client):
    data = {'title': 'Test Task', 'description': 'This is a test task'} 
    response = api_client.post('/api/todo/', data=json.dumps(data), content_type='application/json')
    assert response.status_code == status.HTTP_200_OK
    assert 'Authentication required to create tasks.' in response.data['detail']
    
    
@pytest.mark.django_db
def test_task_list_anonymous(api_client):
    url = reverse('task-list')
    response = api_client.get(url)
    print(response.status_code)
    assert response.status_code == status.HTTP_200_OK
    

@pytest.mark.django_db
def test_task_list_authenticated(authenticated_client):
    response = authenticated_client.get(reverse('task-list'))
    assert response.status_code == status.HTTP_200_OK
   


