# Generated by Django 3.1.6 on 2021-03-16 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_auto_20210316_1614'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_likes',
        ),
        migrations.AddField(
            model_name='user',
            name='user_likes',
            field=models.ManyToManyField(related_name='post_likes', to='network.Post'),
        ),
    ]