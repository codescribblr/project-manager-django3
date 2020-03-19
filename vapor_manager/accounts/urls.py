from django.urls import path

from vapor_manager.accounts import views

app_name = "vapor_manager.accounts"
urlpatterns = [
    path("list/", views.AccountListView.as_view(), name="list"),
    path("<uuid:pk>/", views.AccountDetailView.as_view(), name="detail"),
    path("<uuid:pk>/update/", views.AccountUpdateView.as_view(), name="update"),
    path("<uuid:pk>/invite/", views.AccountInviteView.as_view(), name="invite"),
    path("<uuid:account_pk>/invite/<uuid:pk>", views.AccountInviteJoinView.as_view(), name="invite.join"),
    path("<uuid:pk>/switch/", views.AccountSwitchView.as_view(), name="switch"),
]
