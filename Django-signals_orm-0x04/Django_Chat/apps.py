from django.apps import AppConfig

class DjangoChatConfig(AppConfig):
    name = 'Django_Chat'

    def ready(self):
        import Django_Chat.signals
