# Generated by Django 5.0 on 2024-05-28 15:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_remove_follow_following_list_follow_following_list'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='follower_list',
        ),
        migrations.AddField(
            model_name='follow',
            name='follower_list',
            field=models.ManyToManyField(blank=True, null=True, related_name='follower_list', to=settings.AUTH_USER_MODEL),
        ),
    ]
