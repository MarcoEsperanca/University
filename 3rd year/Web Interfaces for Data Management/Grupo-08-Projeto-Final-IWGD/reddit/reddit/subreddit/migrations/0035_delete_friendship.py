# Generated by Django 4.2.6 on 2023-10-28 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subreddit', '0034_subreddit_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Friendship',
        ),
    ]
