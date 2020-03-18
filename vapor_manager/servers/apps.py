from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ServersConfig(AppConfig):
    name = 'vapor_manager.servers'
    verbose_name = _("Servers")

    def ready(self):
        try:
            import vapor_manager.servers.signals  # noqa F401
        except ImportError:
            pass
