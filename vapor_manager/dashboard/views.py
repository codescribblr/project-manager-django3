from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.db.models.aggregates import Sum
from django.utils import timezone
from django.views.generic import TemplateView

from vapor_manager.projects.models import Project
from vapor_manager.clients.models import Client
from vapor_manager.tasks.models import Task
from vapor_manager.servers.models import Server


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['accounts'] = self.request.user.accounts.all()
        data['active_projects'] = Project.objects.active().by_account(self.request.account)[:5]
        data['active_clients'] = Client.objects.active().by_account(self.request.account)[:5]
        data['active_tasks'] = Task.objects.open().by_account(self.request.account)[:5]
        data['active_servers'] = Server.objects.active().by_account(self.request.account)[:5]
        overdue_tasks_percent = 0
        if Task.objects.open().by_account(self.request.account).filter(due_date__lt=timezone.now()).count() > 0:
            overdue_tasks = Task.objects.open().by_account(self.request.account).filter(
                due_date__lt=timezone.now()).count()
            total_tasks = Task.objects.open().by_account(self.request.account).all().count()
            overdue_tasks_percent = overdue_tasks / total_tasks * 100

        total_monthly_server_cost = 0
        if Server.objects.active().by_account(self.request.account).filter(cost__gt=0).count() > 0:
            servers = Server.objects.active().by_account(self.request.account).filter(cost__gt=0)
            total_monthly_server_cost = servers.aggregate(total_monthly_server_cost=Sum('cost'))

        data['totals'] = {
            'total_projects': Project.objects.active().by_account(self.request.account).all().count(),
            'total_clients': Client.objects.active().by_account(self.request.account).all().count(),
            'overdue_tasks_percent': '{:0.2f}'.format(overdue_tasks_percent),
            'total_monthly_server_cost': total_monthly_server_cost,
        }
        return data
