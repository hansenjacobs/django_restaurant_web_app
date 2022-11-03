from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User, UserProfile

# Decorator for connecting to signal, PREFERRED METHOD
# This method requires: from django.dispatch import receiver; from django.db.models.signals import post_save
# Alternative to decorator is lower in file
@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save
        except:
            # Create user profile if one doesn't exist
            UserProfile.objects.create(user=instance)

# Alternative way to connect signal, however, decorator is preferred
# The method below requires from django.db.models.signals import post_save
# post_save.connect(post_save_create_profile_receiver, sender=User)
