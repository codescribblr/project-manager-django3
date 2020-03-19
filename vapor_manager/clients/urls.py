from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "vapor_manager.clients"
urlpatterns = [
    path('', RedirectView.as_view(pattern_name='clients:list.by_status'), kwargs={'status': 'active'}, name='list'),
    path('list/<str:status>/', views.ClientListView.as_view(), name='list.by_status'),
    path('add/', views.ClientCreateView.as_view(), name='create'),
    path('<uuid:pk>/', views.ClientDetailView.as_view(), name='detail'),
    path('<uuid:pk>/update/', views.ClientUpdateView.as_view(), name='update'),
    path('<uuid:pk>/archive/', views.ClientArchiveView.as_view(), name='archive'),
    path('<uuid:pk>/delete/', views.ClientDeleteView.as_view(), name='delete'),
    # contacts
    path('<uuid:client_pk>/contact/add/', views.ClientContactCreateView.as_view(), name='create_contact'),
    path('<uuid:client_pk>/contact/<int:pk>/update/', views.ClientContactUpdateView.as_view(), name='update_contact'),
    path('<uuid:client_pk>/contact/<int:pk>/delete/', views.ClientContactDeleteView.as_view(), name='delete_contact'),
    # notes
    path('<uuid:client_pk>/note/add/', views.ClientNoteCreateView.as_view(), name='note.create'),
    path('<uuid:client_pk>/note/<int:pk>/update/', views.ClientNoteUpdateView.as_view(), name='note.update'),
    path('<uuid:client_pk>/note/<int:pk>/delete/', views.ClientNoteDeleteView.as_view(), name='note.delete'),
]
