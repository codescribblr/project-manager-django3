from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProjectsConfig(AppConfig):
    name = 'vapor_manager.projects'
    verbose_name = _("Projects")

    def ready(self):
        try:
            import vapor_manager.projects.signals  # noqa F401
        except ImportError:
            pass
