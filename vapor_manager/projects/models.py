import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext as _
from fernet_fields import EncryptedTextField
from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel, UUIDModel

from vapor_manager.clients.models import Client
from vapor_manager.accounts.models import Account

User = get_user_model()


def account_project_path(instance, filename):
    unique_filename = uuid.uuid4()
    return 'accounts/{0}/clients/{1}/projects/{2}/files/{3}'.format(
        instance.project.account.id,
        instance.project.client.id,
        instance.project.id,
        unique_filename)


class ProjectQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status='active')

    def inactive(self):
        return self.filter(status='inactive')

    def by_account(self, account):
        return self.filter(account=account)


class ProjectManager(models.Manager):
    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def inactive(self):
        return self.get_queryset().inactive()

    def by_account(self, account):
        return self.get_queryset().by_account(account)


class Project(TimeStampedModel, StatusModel, UUIDModel):
    STATUS = Choices(
        ('active', _('Active')),
        ('inactive', _('Inactive')),
    )
    client = models.ForeignKey(Client, related_name='projects', on_delete=models.CASCADE)
    account = models.ForeignKey(Account, related_name='projects', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    private_info = EncryptedTextField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    objects = ProjectManager()

    def get_absolute_url(self):
        return reverse('projects:detail', args=(self.id,))


class ProjectNote(TimeStampedModel):
    project = models.ForeignKey(Project, related_name="notes", on_delete=models.CASCADE)
    details = models.TextField()

    def get_absolute_url(self):
        return reverse('projects:detail', args=(self.project.id,))


class ProjectFile(TimeStampedModel):
    project = models.ForeignKey(Project, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(max_length=512, upload_to=account_project_path)
    # store the original filename
    filename = models.CharField(max_length=255)
    user = models.ForeignKey(User, null=True, blank=True, related_name="project_files", on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return reverse('projects:detail', args=(self.project.id,))
