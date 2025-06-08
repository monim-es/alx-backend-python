from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'profile_pic']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'message_body', 'sent_at', 'sender']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages']

    def get_messages(self, obj):
        return MessageSerializer(obj.messages.all().order_by('sent_at'), many=True).data

    def create(self, validated_data):
        participants_usernames = self.initial_data.get("participants", [])
        users = User.objects.filter(username__in=participants_usernames)
        if len(users) < 2:
            raise serializers.ValidationError("At least 2 valid participants required.")
        conversation = Conversation.objects.create()
        conversation.participants.set(users)
        return conversation
