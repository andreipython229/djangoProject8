from django.apps import AppConfig


class MydogsConfig(AppConfig):
    name = 'mydogs'

    def ready(self):
        import mydogs.models  # Импортируем, чтобы сигналы зарегистрировались
