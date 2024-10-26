from rest_framework import serializers
from .models import ToDo
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.urls import reverse
# Serializer for registering a user
from django.contrib.auth import get_user_model
from django.utils import timezone

class UserRegistrationSerializer(serializers.ModelSerializer):
	password = serializers.CharField(max_length=100, min_length=8, style={'input_type': 'password'})
	class Meta:
		model = get_user_model()
		fields = ['email', 'username', 'password']

	def create(self, validated_data):
		user_password = validated_data.get('password', None)
		db_instance = self.Meta.model(email=validated_data.get('email'), username=validated_data.get('username'))
		db_instance.set_password(user_password)
		db_instance.save()
		return db_instance



class UserLoginSerializer(serializers.Serializer):
	email = serializers.CharField(max_length=100)
	username = serializers.CharField(max_length=100, read_only=True)
	password = serializers.CharField(max_length=100, min_length=8, style={'input_type': 'password'})
	token = serializers.CharField(max_length=255, read_only=True)


# Serializer for creating and listing ToDo items
    

# Serializer for listing basic ToDo info
class ListSerializer(serializers.ModelSerializer):
    view_url = serializers.SerializerMethodField()
    class Meta:
        model = ToDo
        fields = ['id','title', 'status', 'due_date', 'view_url', ]
    def get_view_url(self, obj):
        # URL for viewing the task details
        return "http://127.0.0.1:8000/"+reverse('todo-detail', args=[obj.pk])
class ToDoListSerializer(serializers.ModelSerializer):
    
    update_url = serializers.SerializerMethodField()
    delete_url = serializers.SerializerMethodField()

    class Meta:
        model = ToDo
        fields = ['id', 'title', 'description', 'status','created_at', 'updated_at', 'due_date', 'update_url', 'delete_url']
    def validate(self, data):

        due_date = data.get('due_date', None)
        created_at = self.instance.created_at if self.instance else timezone.now()

        # Convert created_at to date for comparison
        created_at_date = created_at.date() if hasattr(created_at, 'date') else created_at

        # Ensure that the due date is not earlier than the creation date
        if due_date and created_at_date > due_date:
            raise serializers.ValidationError("The due date must be later than or equal to the creation date.")
        
        # Return the validated data
        return data


    def get_update_url(self, obj):
        # URL for updating the task
        url="http://127.0.0.1:8000/"+reverse('todo-update', args=[obj.pk])
        return url
    def get_delete_url(self, obj):
        # URL for deleting the task
        url="http://127.0.0.1:8000/"+reverse('todo-delete', args=[obj.pk])
        return url






    
