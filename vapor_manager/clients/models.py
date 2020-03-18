from django.db import models, transaction
from django.urls import reverse
from django.utils.translation import ugettext as _
from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel, UUIDModel

from vapor_manager.users.models import Account


def account_client_path(instance, filename):
    return 'accounts/{0}/clients/{1}/files/{2}'.format(instance.client.account.guid, instance.client.guid, filename)


class ClientQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status='active')

    def inactive(self):
        return self.filter(status='inactive')

    def by_account(self, account):
        return self.filter(account=account)


class ClientManager(models.Manager):
    def get_queryset(self):
        return ClientQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def inactive(self):
        return self.get_queryset().inactive()

    def by_account(self, account):
        return self.get_queryset().by_account(account)


class Client(TimeStampedModel, StatusModel, UUIDModel):
    STATUS = Choices(
        ('active', _('Active')),
        ('inactive', _('Inactive')),
    )
    account = models.ForeignKey(Account, related_name='clients', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    objects = ClientManager()

    def get_absolute_url(self):
        return reverse('clients:detail', args=(self.id,))


class ClientNote(TimeStampedModel):
    client = models.ForeignKey(Client, related_name="notes", on_delete=models.CASCADE)
    details = models.TextField()

    def get_absolute_url(self):
        return reverse('clients:detail', args=(self.client.id,))


class ClientContact(TimeStampedModel):
    client = models.ForeignKey(Client, related_name="contacts", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_primary', 'created']

    def get_absolute_url(self):
        return reverse('clients:detail', args=(self.client.id,))

    def save(self, *args, **kwargs):
        if not self.is_primary:
            return super().save(*args, **kwargs)
        with transaction.atomic():
            ClientContact.objects.filter(is_primary=True).update(is_primary=False)
            return super().save(*args, **kwargs)


class ClientFile(TimeStampedModel):
    client = models.ForeignKey(Client, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to=account_client_path)

    def get_absolute_url(self):
        return reverse('clients:detail', args=(self.client.id,))
