from django.apps import AppConfig


class PlayersProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'players_profile'

    def ready(self):
        import players_profile.signals
