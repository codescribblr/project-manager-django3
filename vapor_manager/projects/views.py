from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, FormView
from django_downloadview import ObjectDownloadView

from vapor_manager.clients.models import Client
from vapor_manager.projects.forms import ProjectAttachServerForm
from vapor_manager.projects.models import Project, ProjectFile, ProjectNote
from vapor_manager.servers.models import Server
from vapor_manager.tasks.models import Task
from vapor_manager.users.models import Account


class ProjectListView(ListView):
    model = Project
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.active().by_account(self.request.account).all() if self.kwargs.get('status', 'active') == 'active' else Project.objects.inactive().by_account(self.request.account).all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update({
            'status': self.kwargs.get('status', 'active'),
            'alt_status': 'inactive' if self.kwargs.get('status', 'active') == 'active' else 'active'
        })
        return data


class ProjectCreateView(CreateView):
    model = Project
    context_object_name = 'project'
    fields = ['name', 'description']

    def form_valid(self, form):
        form.instance.client_id = form.data.get('client')
        form.instance.account_id = self.request.account.id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['account'] = get_object_or_404(Account, pk=self.request.account.pk)
        return data


class ProjectDetailView(DetailView):
    model = Project
    context_object_name = 'project'

    def get_queryset(self):
        return self.model.objects.by_account(self.request.account).all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['open_tasks'] = Task.objects.open().by_account(self.request.account).filter(project=self.object.id)
        data['completed_tasks'] = Task.objects.completed().by_account(self.request.account).filter(project=self.object.id)
        data['servers'] = Server.objects.active().by_account(self.request.account).filter(projects=self.object)
        data['files'] = self.object.files.all()
        return data


class ProjectUpdateView(UpdateView):
    model = Project
    context_object_name = 'project'
    fields = ['name', 'description', 'private_info', 'status']

    def get_queryset(self):
        return self.model.objects.by_account(self.request.account).all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['client'] = get_object_or_404(Client, pk=self.object.client.pk)
        return data


class ProjectAttachServerView(FormView):
    template_name = 'projects/project_attach_server_form.html'
    form_class = ProjectAttachServerForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['project'] = get_object_or_404(Project, pk=self.kwargs.get('pk'), account=self.request.account)
        return data

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['account'] = self.request.account
        return kwargs

    def get_success_url(self):
        return reverse('projects:detail', kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form):
        project = Project.objects.by_account(self.request.account).get(pk=self.kwargs.get('pk'))
        project.servers.add(form.cleaned_data.get('server'))
        return HttpResponseRedirect(self.get_success_url())


class ProjectDeleteView(DeleteView):
    model = Project
    context_object_name = 'project'

    def get_queryset(self):
        return self.model.objects.by_account(self.request.account).all()

    def get_success_url(self):
        return reverse('dashboard')


class ProjectFileCreateView(CreateView):
    model = ProjectFile
    context_object_name = 'file'
    fields = ['file']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['project'] = get_object_or_404(Project, pk=self.kwargs.get('project_pk'), account=self.request.account)
        return data

    def form_valid(self, form):
        form.instance.project_id = self.kwargs.get('project_pk')
        form.instance.filename = form.cleaned_data.get('file').name
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProjectFileDeleteView(DeleteView):
    model = ProjectFile
    context_object_name = 'file'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['project'] = get_object_or_404(Project, pk=self.kwargs.get('project_pk'), account=self.request.account)
        return data

    def get_success_url(self):
        return reverse('projects:detail', kwargs={'pk': self.kwargs.get('project_pk')})


class ProjectFileDownloadView(ObjectDownloadView):
    model = ProjectFile
    basename_field = 'filename'

    def get_queryset(self):
        return self.model.objects.filter(project__account=self.request.account).all()


class ProjectNoteCreateView(CreateView):
    model = ProjectNote
    context_object_name = 'note'
    fields = ['details']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['project'] = get_object_or_404(Project, pk=self.kwargs.get('project_pk'), account=self.request.account)
        return data

    def form_valid(self, form):
        form.instance.project_id = self.kwargs.get('project_pk')
        return super().form_valid(form)


class ProjectNoteUpdateView(UpdateView):
    model = ProjectNote
    context_object_name = 'note'
    fields = ['details']

    def get_queryset(self):
        return self.model.objects.filter(project__account=self.request.account).all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['project'] = get_object_or_404(Project, pk=self.kwargs.get('project_pk'), account=self.request.account)
        return data


class ProjectNoteDeleteView(DeleteView):
    model = ProjectNote
    context_object_name = 'note'

    def get_queryset(self):
        return self.model.objects.filter(project__account=self.request.account).all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['project'] = get_object_or_404(Project, pk=self.kwargs.get('project_pk'), account=self.request.account)
        return data

    def get_success_url(self):
        return reverse('projects:detail', kwargs={'pk': self.kwargs.get('project_pk')})

