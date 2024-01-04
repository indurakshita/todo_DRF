from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect,render
from rest_framework.permissions import AllowAny
from rest_framework import generics,permissions,status
from rest_framework.response import Response
from rest_framework import serializers
from .serializers import UserRegistrationSerializer



class SignupView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]  

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()       
            response_data = {
                "detail": "Successfully signed up",
                "username": user.username,
                
            }
            return Response(response_data)
        except serializers.ValidationError as e:
            return Response({'detail': e.detail}, status=status.HTTP_400_BAD_REQUEST)


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
        # if not request.accepted_renderer.format == 'json':
        #     return redirect('login')
        return Response({"detail": "Logout successful"})