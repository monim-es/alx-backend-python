from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, MessageHistory, Notification

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass




@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    # Remove messages sent/received
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Remove notifications for this user
    Notification.objects.filter(user=instance).delete()

    # Remove message histories edited by this user
    MessageHistory.objects.filter(edited_by=instance).delete()
