import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext as _
from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel, UUIDModel

from vapor_manager.projects.models import Project
from vapor_manager.users.models import Account

User = get_user_model()


def account_task_path(instance, filename):
    unique_filename = uuid.uuid4()
    return 'accounts/{0}/clients/{1}/projects/{2}/tasks/{3}/files/{4}'.format(
        instance.task.account.id,
        instance.task.project.id,
        instance.task.project.client.id,
        instance.task.id,
        unique_filename)


class TaskQuerySet(models.QuerySet):
    def open(self):
        return self.filter(status='open')

    def completed(self):
        return self.filter(status='completed')

    def by_account(self, account):
        return self.filter(account=account)


class TaskManager(models.Manager):
    def get_queryset(self):
        return TaskQuerySet(self.model, using=self._db)

    def open(self):
        return self.get_queryset().open()

    def completed(self):
        return self.get_queryset().completed()

    def by_account(self, account):
        return self.get_queryset().by_account(account)


class Task(TimeStampedModel, StatusModel, UUIDModel):
    STATUS = Choices(
        ('open', _('Open')),
        ('completed', _('Completed')),
    )
    account = models.ForeignKey(Account, related_name="tasks", on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name="tasks", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    objects = TaskManager()

    def get_absolute_url(self):
        return reverse('tasks:detail', args=(self.id,))

    @property
    def is_overdue(self):
        if not self.due_date:
            return False
        return self.due_date < timezone.now().date()


class TaskNote(TimeStampedModel):
    task = models.ForeignKey(Task, related_name="notes", on_delete=models.CASCADE)
    details = models.TextField()

    def get_absolute_url(self):
        return reverse('tasks:detail', args=(self.task.id,))


class TaskFile(TimeStampedModel):
    task = models.ForeignKey(Task, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(max_length=512, upload_to=account_task_path)
    # store the original filename
    filename = models.CharField(max_length=255)
    user = models.ForeignKey(User, null=True, blank=True, related_name="task_files", on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return reverse('tasks:detail', args=(self.task.id,))
