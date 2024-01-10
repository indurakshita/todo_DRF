import pytest
from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from todoapp.models import Task, Subscription,SubscriptionPlan
from todoapp.serializers import TaskSerializer, SubscriptionSerializer

@pytest.fixture
def authenticated_user(db):
    user = User.objects.create_user(username='testuser', password='testpass')
    return user

@pytest.fixture
def task_data():
    return {'title': 'Test Task', 'description': 'Task description', 'completed': False, 'date': '2024-01-01'}

@pytest.fixture
def subscription_data():
    return {'plan': 'Basic'}

@pytest.fixture
def request_factory():
    return APIRequestFactory()

@pytest.mark.django_db
def test_task_serializer_create(authenticated_user, task_data, request_factory):
    request = request_factory.post('/tasks/', task_data, format='json')
    request.user = authenticated_user if authenticated_user.is_authenticated else None
    serializer = TaskSerializer(data=task_data, context={'request': Request(request)})

    assert serializer.is_valid()

    if authenticated_user.is_authenticated:
        task = serializer.save(user=request.user)  
        assert task.user == authenticated_user
    else:
        with pytest.raises(ValueError, match='Cannot assign'):
            serializer.save()

@pytest.mark.django_db
def test_subscription_serializer(subscription_data, authenticated_user):
    Subscription.objects.filter(user=authenticated_user).delete()
    serializer = SubscriptionSerializer(data=subscription_data)
    assert serializer.is_valid()
    subscription = serializer.save(user=authenticated_user)

    assert subscription.plan == subscription_data['plan']
    assert subscription.user == authenticated_user
    
@pytest.mark.django_db
def test_subscription_serializer_with_user(authenticated_user, subscription_data):
    existing_subscription = Subscription.objects.filter(user=authenticated_user).first()
    if existing_subscription:
        subscription_data['plan'] = SubscriptionPlan.ADVANCED
        serializer = SubscriptionSerializer(existing_subscription, data=subscription_data)
    else:
        serializer = SubscriptionSerializer(data=subscription_data)

    assert serializer.is_valid()

    subscription = serializer.save(user=authenticated_user)

    assert subscription.plan == subscription_data['plan']
    assert subscription.user == authenticated_user
