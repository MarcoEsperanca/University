# Generated by Django 4.2.6 on 2023-10-13 13:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('subreddit', '0011_comment_disliked_by_comment_comment_dislikes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='pub_data_comentario',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='data de publicacao_comentario'),
            preserve_default=False,
        ),
    ]
