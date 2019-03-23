from django.apps import AppConfig


class RbacConfig(AppConfig):
    name = 'rbac'

    def ready(self):
        from .signals import create_user
