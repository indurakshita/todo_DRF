from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todoapp import views


router = DefaultRouter()
router.register(r'todo', views.TodoViewset, basename='task')

router.register(r'subscriptions', views.SubscriptionViewSet, basename='subscription')

urlpatterns = [
   
    path('api/', include(router.urls)),
]