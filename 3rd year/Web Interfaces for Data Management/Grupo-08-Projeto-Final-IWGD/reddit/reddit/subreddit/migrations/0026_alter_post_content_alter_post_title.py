# Generated by Django 4.1 on 2023-10-24 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subreddit', '0025_comment_image_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
