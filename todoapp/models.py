

from django.db import models

from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True) 
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title



class SubscriptionPlan(models.TextChoices):
    BASIC = 'Basic','Basic'
    ADVANCED = 'Advanced', 'Advanced'
    PREMIUM = 'Premium', 'Premium'

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription',unique=True)
    plan = models.CharField(max_length=10, choices=SubscriptionPlan.choices,default=SubscriptionPlan.BASIC)

    def __str__(self):
        return f"{self.user.username}'s Subscription"
