from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from vapor_manager.clients.forms import ClientCreateForm
from vapor_manager.clients.models import Client, ClientContact, ClientNote
from vapor_manager.projects.models import Project
from vapor_manager.servers.models import Server
from vapor_manager.tasks.models import Task


class ClientListView(ListView):
    model = Client
    context_object_name = 'clients'

    def get_queryset(self):
        return Client.objects.active().by_account(self.request.account).all() if self.kwargs.get('status', 'active') == 'active' else Client.objects.inactive().by_account(self.request.account).all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update({
            'status': self.kwargs.get('status', 'active'),
            'alt_status': 'inactive' if self.kwargs.get('status', 'active') == 'active' else 'active'
        })
        return data


class ClientCreateView(CreateView):
    model = Client
    context_object_name = 'client'
    form_class = ClientCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['account'] = self.request.account
        return kwargs


class ClientDetailView(DetailView):
    model = Client
    context_object_name = 'client'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['active_projects'] = Project.objects.active().by_account(self.request.account).filter(client=self.object.id)
        data['inactive_projects'] = Project.objects.inactive().by_account(self.request.account).filter(client=self.object.id)
        data['servers'] = Server.objects.active().by_account(self.request.account).filter(projects__client=self.object.id)
        data['tasks'] = Task.objects.open().by_account(self.request.account).filter(project__client=self.object.id)
        return data


class ClientUpdateView(UpdateView):
    model = Client
    context_object_name = 'client'
    fields = ['name', 'status']


class ClientDeleteView(DeleteView):
    model = Client
    context_object_name = 'client'

    def get_success_url(self):
        return reverse('dashboard')


class ClientContactCreateView(CreateView):
    model = ClientContact
    context_object_name = 'contact'
    fields = ['name', 'email', 'phone', 'position']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['client'] = get_object_or_404(Client, pk=self.kwargs.get('client_pk'))
        return data

    def form_valid(self, form):
        form.instance.client_id = self.kwargs.get('client_pk')
        return super().form_valid(form)


class ClientContactUpdateView(UpdateView):
    model = ClientContact
    context_object_name = 'contact'
    fields = ['name', 'email', 'phone', 'position']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['client'] = get_object_or_404(Client, pk=self.kwargs.get('client_pk'))
        return data


class ClientContactDeleteView(DeleteView):
    model = ClientContact
    context_object_name = 'contact'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['client'] = get_object_or_404(Client, pk=self.kwargs.get('client_pk'))
        return data

    def get_success_url(self):
        return reverse('clients:detail', kwargs={'pk': self.kwargs.get('client_pk')})


class ClientNoteCreateView(CreateView):
    model = ClientNote
    context_object_name = 'note'
    fields = ['details']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['client'] = get_object_or_404(Client, pk=self.kwargs.get('client_pk'))
        return data

    def form_valid(self, form):
        form.instance.client_id = self.kwargs.get('client_pk')
        return super().form_valid(form)


class ClientNoteUpdateView(UpdateView):
    model = ClientNote
    context_object_name = 'note'
    fields = ['details']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['client'] = get_object_or_404(Client, pk=self.kwargs.get('client_pk'))
        return data


class ClientNoteDeleteView(DeleteView):
    model = ClientNote
    context_object_name = 'note'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['client'] = get_object_or_404(Client, pk=self.kwargs.get('client_pk'))
        return data

    def get_success_url(self):
        return reverse('clients:detail', kwargs={'pk': self.kwargs.get('client_pk')})
