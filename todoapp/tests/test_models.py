import pytest
from django.contrib.auth.models import User
from todoapp.models import Task, Subscription, SubscriptionPlan

@pytest.fixture
def create_todo_user(username='testuser', password='testpassword'):
    return User.objects.create_user(username=username, password=password)

@pytest.fixture
def create_task(create_todo_user):
    user = create_todo_user
   
    return Task.objects.create(user=user, title='Test Task', description='Task description', completed=False, date='2024-01-01')

@pytest.fixture
def create_subscription(create_todo_user):
    user = create_todo_user
    existing_subscription = Subscription.objects.filter(user=user).first()

    if existing_subscription:
        return existing_subscription
    else:
        return Subscription.objects.create(user=user, plan=SubscriptionPlan.BASIC)
    
    
@pytest.mark.django_db
def test_task_model(create_task):
    task = create_task
    assert str(task) == 'Test Task'
    assert task.user.username == 'testuser'
    assert task.title == 'Test Task'
    assert task.description == 'Task description'
    assert task.completed is False
    assert str(task.date) == '2024-01-01'

@pytest.mark.django_db
def test_subscription_model(create_subscription):
    subscription = create_subscription
    assert str(subscription) == "testuser's Subscription"
    assert subscription.user.username == 'testuser'
    assert subscription.plan == SubscriptionPlan.BASIC
