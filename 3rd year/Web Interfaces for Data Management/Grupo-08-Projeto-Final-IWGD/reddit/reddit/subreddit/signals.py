# No arquivo signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import RedditUser, Message

@receiver(post_save, sender=RedditUser)
def handle_user_creation(sender, instance, created, **kwargs):
    if created and not Message.objects.filter(sender=instance.user).exists():
        print(f'RedditUser criado: {instance.user.username}')
        pass
