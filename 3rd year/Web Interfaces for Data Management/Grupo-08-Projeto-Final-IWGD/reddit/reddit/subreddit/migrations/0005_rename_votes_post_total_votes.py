# Generated by Django 4.2.6 on 2023-10-11 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("subreddit", "0004_post_votes"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="votes",
            new_name="total_votes",
        ),
    ]
