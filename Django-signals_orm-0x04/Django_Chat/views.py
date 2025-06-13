from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Message
from django.views.decorators.cache import cache_page

@login_required
def user_threaded_messages(request):
    messages = Message.objects.filter(
        sender=request.user
    ).select_related('sender', 'receiver', 'parent_message') \
     .prefetch_related('replies') \
     .only('id', 'content', 'receiver__username', 'sender__username', 'parent_message__id')

    threads = []
    for msg in messages:
        threads.append({
            'id': msg.id,
            'content': msg.content,
            'receiver': msg.receiver.username,
            'sender': msg.sender.username,
            'parent': msg.parent_message.id if msg.parent_message else None,
            'replies': [
                {
                    'id': reply.id,
                    'content': reply.content,
                    'sender': reply.sender.username
                } for reply in msg.replies.all()
            ]
        })

    return JsonResponse({'threads': threads})


@login_required
def unread_inbox(request):
    user = request.user
    unread_msgs = Message.unread.for_user(user).select_related('sender').only('id', 'content', 'sender__username', 'timestamp')

    data = [{
        'id': msg.id,
        'content': msg.content,
        'sender': msg.sender.username,
        'timestamp': msg.timestamp
    } for msg in unread_msgs]

    return JsonResponse({'unread_messages': data})


# Message.unread.unread_for_user

# "cache_page", "60"
@cache_page(60)  # Cache for 60 seconds
@login_required
def conversation_messages(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id).select_related('sender')
    data = [{
        'id': msg.id,
        'content': msg.content,
        'sender': msg.sender.username,
        'timestamp': msg.timestamp,
    } for msg in messages]
    return JsonResponse({'messages': data})