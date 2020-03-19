import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext as _
from fernet_fields import EncryptedTextField
from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel, UUIDModel

from vapor_manager.projects.models import Project
from vapor_manager.accounts.models import Account

User = get_user_model()


def account_server_path(instance, filename):
    unique_filename = uuid.uuid4()
    return 'accounts/{0}/servers/{1}/files/{2}'.format(
        instance.server.account.id,
        instance.server.id,
        unique_filename)


class ServerQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status='active')

    def inactive(self):
        return self.filter(status='inactive')

    def by_account(self, account):
        return self.filter(account=account)


class ServerManager(models.Manager):
    def get_queryset(self):
        return ServerQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def inactive(self):
        return self.get_queryset().inactive()

    def by_account(self, account):
        return self.get_queryset().by_account(account)


class Server(TimeStampedModel, StatusModel, UUIDModel):
    STATUS = Choices(
        ('active', _('Active')),
        ('inactive', _('Inactive')),
    )
    account = models.ForeignKey(Account, related_name="servers", on_delete=models.CASCADE)
    hostname = models.CharField(max_length=255)
    public_ip = models.GenericIPAddressField(null=True, blank=True)
    platform = models.CharField(max_length=255, null=True, blank=True)
    capacity = models.CharField(max_length=255, null=True, blank=True)
    private_info = EncryptedTextField(null=True, blank=True)
    cost = models.PositiveIntegerField(default=0, help_text="Monthly cost in whole cents")
    slots = models.PositiveIntegerField(default=10, help_text="Number of sites available on this server")

    projects = models.ManyToManyField(Project, related_name="servers")

    objects = ServerManager()

    def get_absolute_url(self):
        return reverse('servers:detail', args=(self.id,))

    @property
    def available_slots(self):
        return self.slots - self.slots

    def __str__(self):
        return self.hostname


class ServerNote(TimeStampedModel):
    server = models.ForeignKey(Server, related_name="notes", on_delete=models.CASCADE)
    details = models.TextField()

    def get_absolute_url(self):
        return reverse('servers:detail', args=(self.server.id,))


class ServerFile(TimeStampedModel):
    server = models.ForeignKey(Server, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(max_length=512, upload_to=account_server_path)
    # store the original filename
    filename = models.CharField(max_length=255)
    user = models.ForeignKey(User, null=True, blank=True, related_name="server_files", on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return reverse('servers:detail', args=(self.server.id,))
