from django.dispatch import receiver
from django.core.mail import mail_managers
from .models import Post, Category, PostCategory, Author, SubscribedUsers, send_email_to_subscribers
from django.db.models.signals import post_save, m2m_changed


@receiver(m2m_changed, sender=PostCategory)
def notify_post_subscribers(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add':
        user_ = Author.objects.filter(id=instance.author_id).values('user__username')[0]['user__username']
        title = instance.object_title
        text = instance.object_content

        url = f"http://127.0.0.1:8000/{'news/' if instance.post_type == 'N' else 'articles/'}{instance.id}"

        for cat_ in PostCategory.objects.filter(post_id=instance.id).values('category_id'):
            id_to_send = SubscribedUsers.objects.filter(category_id=cat_['category_id']).values('user_id')
            category = Category.objects.filter(id=cat_['category_id']).values('name')[0]['name']

            send_email_to_subscribers(user_, category, title, text, id_to_send, url)
