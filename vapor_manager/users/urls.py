from django.urls import path

from vapor_manager.users import views

app_name = "vapor_manager.users"
urlpatterns = [
    path("~redirect/", views.UserRedirectView.as_view(), name="redirect"),
    path("~update/", views.UserUpdateView.as_view(), name="update"),
    path("<str:email>/", views.UserDetailView.as_view(), name="detail"),
]
