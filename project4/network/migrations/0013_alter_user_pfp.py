# Generated by Django 5.0 on 2024-06-17 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0012_user_pfp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='pfp',
            field=models.CharField(default='https://static.vecteezy.com/system/resources/thumbnails/009/292/244/small/default-avatar-icon-of-social-media-user-vector.jpg', max_length=400),
        ),
    ]
