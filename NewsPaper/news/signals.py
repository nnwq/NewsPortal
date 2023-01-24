from django.dispatch import receiver
from django.core.mail import mail_managers
from .models import Post, Category, SubscribedUsers
from django.db.models.signals import post_save


@receiver(post_save, sender=Post)
def send_mail_to_subs(sender, instance, created, **kwargs):
    if created:
        for SubscribedUsers in instance.author.subscribed.all():
            send_mail(
                f'New Post from {instance.author}',
                f'Title: {instance.post_title}',
                'youremail',
                [subs.email],
            )
