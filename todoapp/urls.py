from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todoapp import views


router = DefaultRouter()
router.register('', views.TodoViewset, basename='task')


urlpatterns = [
   
    path('todo/', include(router.urls)),
]