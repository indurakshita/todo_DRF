import pytest
from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from todoapp.models import Task, Subscription, SubscriptionPlan
from account.serializers import UserRegistrationSerializer, CustomLoginSerializer
from todoapp.serializers import TaskSerializer, SubscriptionSerializer
from rest_framework.exceptions import ValidationError

@pytest.fixture
def authenticated_user(db):
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def request_factory():
    return APIRequestFactory()

@pytest.fixture
def task_data():
    return {'title': 'Test Task', 'description': 'Task description', 'completed': False, 'date': '2024-01-01'}

@pytest.fixture
def subscription_data():
    return {'plan': 'Basic'}

@pytest.mark.django_db
class TestUserRegistrationSerializer:
    def test_valid_data(self):
        data = {'username': 'testuser', 'password': 'testpassword'}
        serializer = UserRegistrationSerializer(data=data)
        assert serializer.is_valid()

        user = serializer.save()
        assert User.objects.filter(username='testuser').exists()
        assert user.check_password('testpassword')

    @pytest.mark.parametrize("data, expected_error", [
        ({'username': 'ab', 'password': 'newpassword'}, 'username'),
        ({'username': 'user@name', 'password': 'newpassword'}, 'username'),
        ({'username': 'existinguser', 'password': 'newpassword'}, 'username'),
    ])
    def test_invalid_data(self, data, expected_error):
        User.objects.create_user(username='existinguser', password='password123')
        serializer = UserRegistrationSerializer(data=data)

        assert not serializer.is_valid()
        assert expected_error in serializer.errors


@pytest.mark.django_db
class TestCustomLoginSerializer:
    
    @pytest.mark.parametrize("user_data, data", [
        ({'username': 'testuser', 'password': 'testpassword'}, {'username': 'testuser', 'password': 'testpassword'}),
    ])
    def test_valid_credentials(self, authenticated_user, user_data, data):
        # Valid credentials
        serializer_valid = CustomLoginSerializer(data=data)


        assert serializer_valid.is_valid(), f"Validation errors: {serializer_valid.errors}"
        validated_data_valid = serializer_valid.validated_data
        assert validated_data_valid['username'] == user_data['username']
        assert validated_data_valid['password'] == user_data['password']

    @pytest.mark.parametrize("user_data, data", [
        ({'username': 'testuser2', 'password': 'testpassword2'}, {'username': 'testuser2', 'password': 'wrongpassword'}),
    ])
    def test_invalid_credentials(self, authenticated_user, user_data, data):
        # Invalid credentials
        serializer_invalid = CustomLoginSerializer(data=data)

        if not serializer_invalid.is_valid():
            print(serializer_invalid.errors)

        with pytest.raises(ValidationError, match='Invalid login credentials.'):
            serializer_invalid.is_valid(raise_exception=True)


            
@pytest.mark.django_db
class TestTaskSerializer:
    def test_create_authenticated_user(self, authenticated_user, task_data, request_factory):
        request = request_factory.post('/tasks/', task_data, format='json')
        request.user = authenticated_user if authenticated_user else None
        serializer = TaskSerializer(data=task_data, context={'request': Request(request)})

        assert serializer.is_valid()

        if authenticated_user:
            task = serializer.save(user=request.user)  
            assert task.user == authenticated_user
        else:
            with pytest.raises(ValueError, match='Cannot assign'):
                serializer.save()

@pytest.mark.django_db
class TestSubscriptionSerializer:
    def test_create(self, subscription_data, authenticated_user):
        Subscription.objects.filter(user=authenticated_user).delete()
        serializer = SubscriptionSerializer(data=subscription_data)
        assert serializer.is_valid()
        subscription = serializer.save(user=authenticated_user)

        assert subscription.plan == subscription_data['plan']
        assert subscription.user == authenticated_user

    def test_update_existing_subscription(self, authenticated_user, subscription_data):
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