from rest_framework import serializers
from .models import Task,Subscription
from rest_framework import serializers
from django.contrib.auth.models import User

   
class TaskSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'completed', 'date', 'username')

    def create(self, validated_data):
        user = self.context.get('request').user 
        if user.is_authenticated:
            task = Task.objects.create(user=user, **validated_data)
        else:
            task = Task.objects.create(**validated_data)
        return task

 
    
class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Subscription
        fields = '__all__'
        
    def get_user(self, obj):
        return obj.user.username if obj.user else None
    
 
   
