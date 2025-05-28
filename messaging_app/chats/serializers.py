from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField()

    class Meta:
        model = Message
        fields = ['message_id', 'message_body', 'sent_at', 'sender']

class ConversationSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'users', 'messages']

    def get_messages(self, obj):
        messages = obj.message_set.all().order_by('sent_at')
        return MessageSerializer(messages, many=True).data

    def validate(self, data):
        users = self.initial_data.get('users')
        if not users or len(users) < 2:
            raise serializers.ValidationError("A conversation must have at least two users.")
        return data
