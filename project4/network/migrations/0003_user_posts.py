# Generated by Django 5.0 on 2024-05-27 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_user_followers_user_following_comment_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='posts',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]