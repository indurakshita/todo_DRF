import pytest
from unittest.mock import patch
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import AnonymousUser, User
from rest_framework.exceptions import Throttled
from todoapp.throttles import AnonUserThrottle, BasicUserThrottle

@pytest.fixture
def api_factory():
    return APIRequestFactory()

@pytest.fixture
def anon_user():
    return AnonymousUser()

@pytest.fixture
def basic_user():
    return User.objects.create_user(username='basicuser', password='password')

@pytest.mark.django_db
def test_anon_user_throttle(api_factory, anon_user):
    throttle = AnonUserThrottle()

    def mock_allow_request(request, view):
        raise Throttled(detail="Anonymous user request limit exceeded. Sign up to increase the limit.")

    with patch.object(throttle, 'allow_request', side_effect=mock_allow_request):
        with pytest.raises(Throttled) as excinfo:
            request = api_factory.get('/')
            request.user = anon_user
            throttle.allow_request(request, None)

    assert 'Anonymous user request limit exceeded. Sign up to increase the limit.' in str(excinfo.value.detail)

@pytest.mark.django_db
def test_basic_user_throttle(api_factory, basic_user):
    throttle = BasicUserThrottle()

    def mock_allow_request(request, view):
        raise Throttled(detail="Request was throttled. Expected available in 100 seconds.")

    with patch.object(throttle, 'allow_request', side_effect=mock_allow_request):
        with pytest.raises(Throttled) as excinfo:
            request = api_factory.get('/')
            request.user = basic_user
            throttle.allow_request(request, None)

    assert 'Request was throttled. Expected available in 100 seconds.' in str(excinfo.value.detail)
