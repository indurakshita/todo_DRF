from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Task, Subscription
from .serializers import TaskSerializer, SubscriptionSerializer
from rest_framework.response import Response

from .throttles import *

class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user_subscription = Subscription.objects.filter(user=request.user).first()

        if user_subscription:
            serializer = self.get_serializer(user_subscription, data=request.data,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)

        return Response(serializer.data)
    
            
    # def get_throttles(self):
       
    #     if self.request.user.is_authenticated:
            
    #         user_profile = self.request.user.subscription
        
    #         if user_profile and hasattr(user_profile, 'plan'):
    #             user_type = user_profile.plan
                
    #             if user_type == 'Advanced':
    #                 self.throttle_classes = [AdvanceUserThrottle]
    #             elif user_type == 'Premium':
    #                 self.throttle_classes = [PremiumUserThrottle]
    #         return super().get_throttles()
    #     else:
    #         self.throttle_classes = [AnonUserThrottle]
    #         return super().get_throttles()
        
    
class TodoViewset(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]
    throttle_classes = [BasicUserThrottle, AdvanceUserThrottle, PremiumUserThrottle]
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action == 'list':
            return [IsAuthenticated()]
        else:
            return super().get_permissions()
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Task.objects.filter(user=self.request.user)
        else:
            
            return Task.objects.none()
        
    def create(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            
            return Response({'detail': 'Authentication required to create tasks.'})
        
        return super().create(request, *args, **kwargs)



    def get_throttles(self):
        if self.request.user.is_authenticated:
            user_profile = self.request.user.subscription
            if user_profile and hasattr(user_profile, 'plan'):
                user_type = user_profile.plan
                if user_type == 'Basic':
                    self.throttle_classes = [BasicUserThrottle]
                if user_type == 'Advanced':
                    self.throttle_classes = [AdvanceUserThrottle]
                elif user_type == 'Premium':
                    self.throttle_classes = [PremiumUserThrottle]
            return super().get_throttles()
        else:
            self.throttle_classes = [AnonUserThrottle]
            return super().get_throttles()
        

          
    





