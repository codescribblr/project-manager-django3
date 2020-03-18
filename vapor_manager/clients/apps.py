from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ClientsConfig(AppConfig):
    name = 'vapor_manager.clients'
    verbose_name = _("Clients")

    def ready(self):
        try:
            import vapor_manager.clients.signals  # noqa F401
        except ImportError:
            pass
