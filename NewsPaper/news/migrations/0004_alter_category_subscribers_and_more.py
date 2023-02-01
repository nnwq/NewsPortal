# Generated by Django 4.1.5 on 2023-02-01 14:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0003_rename_time_created_post_creation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(through='news.SubscribedUsers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='subscribedusers',
            name='subscriber',
        ),
        migrations.AddField(
            model_name='subscribedusers',
            name='subscriber',
            field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
