from django.contrib import admin
from todoapp.models import *

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["id", "title","user"]

@admin.register(Subscription)  
class TaskAdmin(admin.ModelAdmin):
    list_display = ['user','plan']




