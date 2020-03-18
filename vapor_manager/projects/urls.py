from django.urls import path
from django.views.generic import RedirectView

from vapor_manager.projects import views
app_name = "vapor_manager.projects"

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='projects:list.by_status'), kwargs={'status': 'active'}, name='list'),
    path('list/<str:status>/', views.ProjectListView.as_view(), name='list.by_status'),
    path('add/', views.ProjectCreateView.as_view(), name='create'),
    path('<uuid:pk>/', views.ProjectDetailView.as_view(), name='detail'),
    path('<uuid:pk>/update/', views.ProjectUpdateView.as_view(), name='update'),
    path('<uuid:pk>/delete/', views.ProjectDeleteView.as_view(), name='delete'),
    path('<uuid:pk>/attach/server/', views.ProjectAttachServerView.as_view(), name='attach.server'),
    # files
    path('<uuid:project_pk>/file/add/', views.ProjectFileCreateView.as_view(), name='file.create'),
    path('<uuid:project_pk>/file/<int:pk>/delete/', views.ProjectFileDeleteView.as_view(), name='file.delete'),
    path('<uuid:project_pk>/file/<int:pk>/download/', views.ProjectFileDownloadView.as_view(), name='file.download'),
    # notes
    path('<uuid:project_pk>/note/add/', views.ProjectNoteCreateView.as_view(), name='note.create'),
    path('<uuid:project_pk>/note/<int:pk>/update/', views.ProjectNoteUpdateView.as_view(), name='note.update'),
    path('<uuid:project_pk>/note/<int:pk>/delete/', views.ProjectNoteDeleteView.as_view(), name='note.delete'),
]
