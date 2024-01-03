from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todoapp import views

router = DefaultRouter()
router.register('', views.TodoViewset, basename='task')


urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('todo/', include(router.urls)),
]