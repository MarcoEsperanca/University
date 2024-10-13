from django.apps import AppConfig

class SubredditConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subreddit'

    def ready(self):
        import subreddit.signals
