# Generated by Django 4.1.5 on 2023-01-30 10:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0002_alter_post_post_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='time_created',
            new_name='creation',
        ),
        migrations.AddField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='SubscribedUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.category')),
                ('subscriber', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
