from rest_framework import generics,permissions,views,status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect,render
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import Task
from .serializers import UserRegistrationSerializer,TaskSerializer
from .permissions import IsOwner  


class SignupView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]  

    def create(self, request, *args, **kwargs):
        return redirect('login')


class CustomLoginView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/todo/')  
        return Response({"detail": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def get(self, request):
        return render(request, 'logout.html')

    def post(self, request):
        logout(request)
        if not request.accepted_renderer.format == 'json':
            return redirect('login')
        return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)


class TodoViewset(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


