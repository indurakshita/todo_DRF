
import pytest
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import AnonymousUser, User
from todoapp.throttles import AnonUserThrottle, BasicUserThrottle, AdvanceUserThrottle, PremiumUserThrottle

@pytest.fixture
def api_factory():
    return APIRequestFactory()

@pytest.fixture
def anon_user():
    return AnonymousUser()

@pytest.mark.django_db
@pytest.fixture
def basic_user():
    return User.objects.create_user(username='basicuser', password='password')

@pytest.mark.django_db
@pytest.fixture
def advance_user():
    return User.objects.create_user(username='advanceuser', password='password')

@pytest.mark.django_db
@pytest.fixture
def premium_user():
    return User.objects.create_user(username='premiumuser', password='password')

@pytest.mark.django_db
def test_anon_user_throttle(api_factory, anon_user):
    throttle = AnonUserThrottle()
    request = api_factory.get('/')
    request.user = anon_user
    assert throttle.allow_request(request, None)

@pytest.mark.django_db
def test_basic_user_throttle(api_factory, basic_user):
    throttle = BasicUserThrottle()
    request = api_factory.get('/')
    request.user = basic_user
    assert throttle.allow_request(request, None)

@pytest.mark.django_db
def test_advance_user_throttle(api_factory, advance_user):
    throttle = AdvanceUserThrottle()
    request = api_factory.get('/')
    request.user = advance_user
    assert throttle.allow_request(request, None)

@pytest.mark.django_db
def test_premium_user_throttle(api_factory, premium_user):
    throttle = PremiumUserThrottle()
    request = api_factory.get('/')
    request.user = premium_user
    assert throttle.allow_request(request, None)
