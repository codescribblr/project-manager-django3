from django.urls import path
from django.views.generic import RedirectView

from vapor_manager.servers import views

app_name = "vapor_mamager.servers"
urlpatterns = [
    path('', RedirectView.as_view(pattern_name='servers:list.by_status'), kwargs={'status': 'active'}, name='list'),
    path('list/<str:status>/', views.ServerListView.as_view(), name='list.by_status'),
    path('add/', views.ServerCreateView.as_view(), name='create'),
    path('<uuid:pk>/', views.ServerDetailView.as_view(), name='detail'),
    path('<uuid:pk>/update/', views.ServerUpdateView.as_view(), name='update'),
    path('<uuid:pk>/delete/', views.ServerDeleteView.as_view(), name='delete'),
    # files
    path('<uuid:server_pk>/file/add/', views.ServerFileCreateView.as_view(), name='file.create'),
    path('<uuid:server_pk>/file/<int:pk>/delete/', views.ServerFileDeleteView.as_view(), name='file.delete'),
    path('<uuid:server_pk>/file/<int:pk>/download/', views.ServerFileDownloadView.as_view(), name='file.download'),
    # notes
    path('<uuid:server_pk>/note/add/', views.ServerNoteCreateView.as_view(), name='note.create'),
    path('<uuid:server_pk>/note/<int:pk>/update/', views.ServerNoteUpdateView.as_view(), name='note.update'),
    path('<uuid:server_pk>/note/<int:pk>/delete/', views.ServerNoteDeleteView.as_view(), name='note.delete'),
]
