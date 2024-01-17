from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect,render
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import serializers
from .serializers import UserRegistrationSerializer
from rest_framework.authtoken.models import Token

from .serializers import UserRegistrationSerializer



class SignupView(CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            
            response_data = {
                "detail": "Successfully signed up",
                "username": user.username,
            }
            return Response(response_data)
        except serializers.ValidationError as e:
            return Response({'detail': e.detail}, status=status.HTTP_400_BAD_REQUEST)

def generate_token_for_user(user):
    existing_token = Token.objects.filter(user=user).first()
    if existing_token:   
        return existing_token
    else:    
        return Token.objects.create(user=user)

class CustomLoginView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/api/todo/')
        else: 
            return render(request, 'login.html')
        
    def post(self, request):
        token = request.data.get('token')
        if token:
            try:
                user = Token.objects.get(key=token).user
                login(request, user)
                return Response({"detail": "Login successful", "token": token}, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response({"detail": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                token = generate_token_for_user(user)
                login(request, user)
                return redirect('/api/todo/')
            else:
                return Response({"detail": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def get(self, request):
        return render(request, 'logout.html')
    
    def post(self, request):
        logout(request)    
        return redirect('login')