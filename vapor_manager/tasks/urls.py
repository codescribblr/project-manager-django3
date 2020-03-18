from django.urls import path
from django.views.generic import RedirectView

from vapor_manager.tasks import views
app_name = "vapor_manager.tasks"

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='tasks:list.by_status'), kwargs={'status': 'open'}, name='list'),
    path('list/<str:status>/', views.TaskListView.as_view(), name='list.by_status'),
    path('add/', views.TaskCreateView.as_view(), name='create'),
    path('<uuid:pk>/', views.TaskDetailView.as_view(), name='detail'),
    path('<uuid:pk>/update/', views.TaskUpdateView.as_view(), name='update'),
    path('<uuid:pk>/delete/', views.TaskDeleteView.as_view(), name='delete'),
    path('<uuid:pk>/archive/', views.TaskArchiveView.as_view(), name='archive'),
    # files
    path('<uuid:task_pk>/file/add/', views.TaskFileCreateView.as_view(), name='file.create'),
    path('<uuid:task_pk>/file/<int:pk>/delete/', views.TaskFileDeleteView.as_view(), name='file.delete'),
    path('<uuid:task_pk>/file/<int:pk>/download/', views.TaskFileDownloadView.as_view(), name='file.download'),
    # notes
    path('<uuid:task_pk>/note/add/', views.TaskNoteCreateView.as_view(), name='note.create'),
    path('<uuid:task_pk>/note/<int:pk>/update/', views.TaskNoteUpdateView.as_view(), name='note.update'),
    path('<uuid:task_pk>/note/<int:pk>/delete/', views.TaskNoteDeleteView.as_view(), name='note.delete'),
]
