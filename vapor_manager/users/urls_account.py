from django.urls import path

from vapor_manager.users import views

app_name = "vapor_manager.users"
urlpatterns = [
    path("<uuid:pk>/update/", views.AccountUpdateView.as_view(), name="update"),
    path("<uuid:pk>/", views.AccountDetailView.as_view(), name="detail"),
]
