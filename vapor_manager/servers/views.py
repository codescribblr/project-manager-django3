from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django_downloadview import ObjectDownloadView

from vapor_manager.clients.models import Client
from vapor_manager.servers.models import Server, ServerFile, ServerNote
from vapor_manager.users.models import Account


class ServerListView(ListView):
    model = Server
    context_object_name = 'servers'

    def get_queryset(self):
        return Server.objects.active().by_account(self.request.account).all() if self.kwargs.get('status', 'active') == 'active' else Server.objects.inactive().by_account(self.request.account).all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update({
            'status': self.kwargs.get('status', 'active'),
            'alt_status': 'inactive' if self.kwargs.get('status', 'active') == 'active' else 'active'
        })
        return data


class ServerCreateView(CreateView):
    model = Server
    context_object_name = 'server'
    fields = ['hostname', 'public_ip', 'platform', 'capacity', 'private_info', 'slots', 'cost', ]

    def form_valid(self, form):
        form.instance.account_id = self.request.account.id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['account'] = get_object_or_404(Account, pk=self.request.account.pk)
        return data


class ServerDetailView(DetailView):
    model = Server
    context_object_name = 'server'

    def get_queryset(self):
        return self.model.objects.by_account(self.request.account).all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['projects'] = self.object.projects.all()
        data['clients'] = Client.objects.by_account(self.request.account).filter(projects__servers=self.object.id)
        data['files'] = self.object.files.all()
        return data


class ServerUpdateView(UpdateView):
    model = Server
    context_object_name = 'server'
    fields = ['hostname', 'public_ip', 'platform', 'capacity', 'private_info', 'slots', 'cost', 'status', ]

    def get_queryset(self):
        return self.model.objects.by_account(self.request.account).all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        return data


class ServerDeleteView(DeleteView):
    model = Server
    context_object_name = 'server'

    def get_queryset(self):
        return self.model.objects.by_account(self.request.account).all()

    def get_success_url(self):
        return reverse('dashboard')


class ServerFileCreateView(CreateView):
    model = ServerFile
    context_object_name = 'file'
    fields = ['file']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['server'] = get_object_or_404(Server, pk=self.kwargs.get('server_pk'), account=self.request.account)
        return data

    def form_valid(self, form):
        form.instance.server_id = self.kwargs.get('server_pk')
        form.instance.filename = form.cleaned_data.get('file').name
        form.instance.user = self.request.user
        return super().form_valid(form)


class ServerFileDeleteView(DeleteView):
    model = ServerFile
    context_object_name = 'file'

    def get_queryset(self):
        return self.model.objects.filter(server__account=self.request.account).all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['server'] = get_object_or_404(Server, pk=self.kwargs.get('server_pk'), account=self.request.account)
        return data

    def get_success_url(self):
        return reverse('servers:detail', kwargs={'pk': self.kwargs.get('server_pk')})


class ServerFileDownloadView(ObjectDownloadView):
    model = ServerFile
    basename_field = 'filename'

    def get_queryset(self):
        return self.model.objects.filter(server__account=self.request.account).all()


class ServerNoteCreateView(CreateView):
    model = ServerNote
    context_object_name = 'note'
    fields = ['details']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['server'] = get_object_or_404(Server, pk=self.kwargs.get('server_pk'), account=self.request.account)
        return data

    def form_valid(self, form):
        form.instance.server_id = self.kwargs.get('server_pk')
        return super().form_valid(form)


class ServerNoteUpdateView(UpdateView):
    model = ServerNote
    context_object_name = 'note'
    fields = ['details']

    def get_queryset(self):
        return self.model.objects.filter(server__account=self.request.account).all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['server'] = get_object_or_404(Server, pk=self.kwargs.get('server_pk'), account=self.request.account)
        return data


class ServerNoteDeleteView(DeleteView):
    model = ServerNote
    context_object_name = 'note'

    def get_queryset(self):
        return self.model.objects.filter(server__account=self.request.account).all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['server'] = get_object_or_404(Server, pk=self.kwargs.get('server_pk'), account=self.request.account)
        return data

    def get_success_url(self):
        return reverse('servers:detail', kwargs={'pk': self.kwargs.get('server_pk')})
