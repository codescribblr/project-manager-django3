from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from rest_framework.authtoken.views import obtain_auth_token

from vapor_manager.dashboard.views import DashboardView

urlpatterns = [
    path("", DashboardView.as_view(), name="home"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path(settings.ADMIN_URL, admin.site.urls),
    path("users/", include("vapor_manager.users.urls", namespace="users")),
    path("accounts/", include("vapor_manager.users.urls_account", namespace="accounts")),
    path("clients/", include("vapor_manager.clients.urls", namespace="clients")),
    path("projects/", include("vapor_manager.projects.urls", namespace="projects")),
    path("tasks/", include("vapor_manager.tasks.urls", namespace="tasks")),
    path("servers/", include("vapor_manager.servers.urls", namespace="servers")),
    path("accounts/", include("allauth.urls")),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
