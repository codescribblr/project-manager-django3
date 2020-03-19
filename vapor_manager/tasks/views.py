from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django_downloadview import ObjectDownloadView

from vapor_manager.projects.models import Project
from vapor_manager.tasks.models import Task, TaskFile, TaskNote
from vapor_manager.accounts.models import Account


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.open().by_account(self.request.account).all() if self.kwargs.get('status', 'open') == 'open' else Task.objects.completed().by_account(self.request.account).all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update({
            'status': self.kwargs.get('status', 'open'),
            'alt_status': 'completed' if self.kwargs.get('status', 'open') == 'open' else 'open'
        })
        return data


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    context_object_name = 'task'
    fields = ['name', 'description', 'start_date', 'due_date']

    def form_valid(self, form):
        form.instance.project_id = form.data.get('project')
        form.instance.account_id = self.request.account.id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['account'] = get_object_or_404(Account, pk=self.request.account.pk)
        return data


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'

    def get_queryset(self):
        return self.model.objects.by_account(self.request.account).all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['files'] = self.object.files.all()
        return data


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    context_object_name = 'task'
    fields = ['name', 'description', 'start_date', 'due_date', 'status']

    def get_queryset(self):
        return self.model.objects.by_account(self.request.account).all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['project'] = get_object_or_404(Project, pk=self.object.project.pk, account=self.request.account)
        return data


class TaskArchiveView(LoginRequiredMixin, UpdateView):
    model = Task
    context_object_name = 'task'
    fields = ['status']
    http_method_names = ['post', ]

    def get_queryset(self):
        return self.model.objects.by_account(self.request.account).all()

    def form_valid(self, form):
        form.instance.status = 'completed'
        form.instance.completed_at = timezone.now()
        messages.add_message(
            self.request, messages.SUCCESS, _("Task marked as complete.")
        )
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'

    def get_queryset(self):
        return self.model.objects.by_account(self.request.account).all()

    def get_success_url(self):
        return reverse('dashboard')


class TaskFileCreateView(LoginRequiredMixin, CreateView):
    model = TaskFile
    context_object_name = 'file'
    fields = ['file']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['task'] = get_object_or_404(Task, pk=self.kwargs.get('task_pk'), account=self.request.account)
        return data

    def form_valid(self, form):
        form.instance.task_id = self.kwargs.get('task_pk')
        form.instance.filename = form.cleaned_data.get('file').name
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskFileDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskFile
    context_object_name = 'file'

    def get_queryset(self):
        return self.model.objects.filter(task__account=self.request.account).all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['task'] = get_object_or_404(Task, pk=self.kwargs.get('task_pk'), account=self.request.account)
        return data

    def get_success_url(self):
        return reverse('tasks:detail', kwargs={'pk': self.kwargs.get('task_pk')})


class TaskFileDownloadView(LoginRequiredMixin, ObjectDownloadView):
    model = TaskFile
    basename_field = 'filename'

    def get_queryset(self):
        return self.model.objects.filter(task__account=self.request.account).all()


class TaskNoteCreateView(LoginRequiredMixin, CreateView):
    model = TaskNote
    context_object_name = 'note'
    fields = ['details']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['task'] = get_object_or_404(Task, pk=self.kwargs.get('task_pk'), account=self.request.account)
        return data

    def form_valid(self, form):
        form.instance.task_id = self.kwargs.get('task_pk')
        return super().form_valid(form)


class TaskNoteUpdateView(LoginRequiredMixin, UpdateView):
    model = TaskNote
    context_object_name = 'note'
    fields = ['details']

    def get_queryset(self):
        return self.model.objects.filter(task__account=self.request.account).all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['task'] = get_object_or_404(Task, pk=self.kwargs.get('task_pk'), account=self.request.account)
        return data


class TaskNoteDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskNote
    context_object_name = 'note'

    def get_queryset(self):
        return self.model.objects.filter(task__account=self.request.account).all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['task'] = get_object_or_404(Task, pk=self.kwargs.get('task_pk'), account=self.request.account)
        return data

    def get_success_url(self):
        return reverse('tasks:detail', kwargs={'pk': self.kwargs.get('task_pk')})
