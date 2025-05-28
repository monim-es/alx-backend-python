from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # Nested User info

    class Meta:
        model = Message
        fields = ['message_id', 'message_body', 'sent_at', 'sender']

class ConversationSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)  # Many-to-many users
    messages = MessageSerializer(many=True, read_only=True)  # Nested messages

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'users', 'messages']
