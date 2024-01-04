from rest_framework import serializers
from .models import Task
from rest_framework import serializers

   
class TaskSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'completed', 'date', 'username')

    def create(self, validated_data):
        user = self.context.get('request').user  
        task = Task.objects.create(user=user, **validated_data)
        return task
