from django.db.models.signals import post_save , pre_save , post_delete
from django.dispatch import receiver
from uuid import uuid4
from .models import (
    User , UserProfile 
)
import os



@receiver(post_save , sender=User)
def user_profile_signal(sender, instance , created , **kwarg):
    if created:
        UserProfile.objects.create(user=instance)


