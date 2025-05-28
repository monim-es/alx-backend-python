from django.db import models
import uuid

# Create your models here.

from django.contrib.auth.models import AbstractUser

# Custom User model
class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    password = models.CharField(max_length=128) 
    profile_pic = models.ImageField(upload_to='profiles/', null=True, blank=True)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)

# Conversation model
class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.conversation_id)

# Message model

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f'{self.sender}: {self.message_body[:20]}...'
