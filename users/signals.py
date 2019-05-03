from django.db.models.signals import post_save
from django.dispatch import receiver

# from .models import User, Wishlist


# @receiver(post_save, sender=User)
# def create_wishlist_if_new_user(sender, instance=None, created=False, **kwargs):
#     if created:
#         Wishlist.objects.create(user=instance)
