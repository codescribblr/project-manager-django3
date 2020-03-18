from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TasksConfig(AppConfig):
    name = 'vapor_manager.tasks'
    verbose_name = _("Tasks")

    def ready(self):
        try:
            import vapor_manager.tasks.signals  # noqa F401
        except ImportError:
            pass
