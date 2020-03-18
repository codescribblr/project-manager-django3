import hashlib

from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group as UserGroup
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel, UUIDModel


class User(UUIDModel, AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)
    current_account = models.ForeignKey('Account', null=True, blank=True, on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"email": self.email})

    def activate(self, account=None):
        if account is None:
            account = Account.objects.create(owner=self, company=self.email)
        self.account = account
        self.save()

    @property
    def profile_image_url(self):
        return f"https://gravatar.com/avatar/{hashlib.md5(self.email.encode('utf-8')).hexdigest()}"


class Permission(models.Model):
    """defines action available to users in Account"""
    name = models.CharField(
        max_length=100,
        help_text='Human-friendly name for permission'
    )
    code_name = models.CharField(
        max_length=100,
        help_text='Computer-friendly name for permission'
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        """unicode representation of Permission"""
        return str(self.name)


class Group(models.Model):
    """defines a group of actions available to users in Account"""
    name = models.CharField(
        max_length=80,
        help_text='Friendly name for grouping'
    )
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('permissions'),
        blank=True,
        help_text='Permissions assiged to all accounts in this group'
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        """unicode representation of Group"""
        return str(self.name)


class Account(TimeStampedModel, StatusModel, UUIDModel):
    STATUS = Choices(
        ('active', _('Active')),
        ('inactive', _('Inactive')),
    )
    company = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        help_text=_('Name of the company'),
    )
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('permissions'),
        blank=True,
        help_text='Specific permission for this account'
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this account belongs to. An account will '
                    'get all permissions granted to each of its groups.'
                    )
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('users'),
        blank=True,
        related_name='accounts',
        through='AccountUser',
        help_text=_('Members of the company represented by this account.')
    )
    owner = models.ForeignKey(
        User,
        related_name='account',
        null=True,
        help_text='User who owns or administrates this account',
        on_delete=models.CASCADE
    )

    class Meta:
        """meta details about Accounts"""
        ordering = ('company', 'owner',)

    def __str__(self):
        """unicode representation of Account"""
        return str('%s (%s)' % (self.company, self.owner))

    def get_group_permissions(self):
        """gets permissions granted to Account based on Group membership"""
        if not hasattr(self, '_group_permissions'):
            self._group_permissions = Permission.objects.filter(group__in=self.groups.all())
        return self._group_permissions

    def get_permissions(self):
        """gets explicitly set permissions granted to Account"""
        if not hasattr(self, '_permissions'):
            self._permissions = self.permissions.all()
        return self._permissions

    def can(self, permission_code_name):
        """determines whether or not a User of this Account can do the action"""
        if permission_code_name in list(self.get_group_permissions().values_list('code_name', flat=True)):
            # match against group permissions first for common use case
            return True
        return permission_code_name in list(self.get_permissions().values_list('code_name', flat=True))


class AccountUser(models.Model):
    """intermediary between Account and User, allowing assignment of roles/permissions"""
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    groups = models.ManyToManyField(
        UserGroup,
        related_name='groups',
        blank=True,
        help_text='Permission groups to which this AccountUser belongs'
    )

    class Meta:
        ordering = ('account', 'user__email')

    def get_all_permissions(self, obj=None):
        """
        returns permissions belonging to user
        """
        return self.get_group_permissions(obj)

    def get_group_permissions(self, obj=None):
        """
        Returns a set of permission strings that this user has through his/her
        groups.
        """
        user_obj = self.user
        if user_obj.is_anonymous or obj is not None:
            return set()
        if not hasattr(self, '_group_perm_cache'):
            if user_obj.is_superuser:
                perms = Permission.objects.all()
            else:
                perms = Permission.objects.filter(group__in=self.groups.all())
            perms = perms.values_list('content_type__app_label', 'codename').order_by()
            self._group_perm_cache = set("%s.%s" % (ct, name) for ct, name in perms)
        return self._group_perm_cache

    def has_perm(self, perm, obj=None):
        """
        Determines if AccountUser has the given permission based on
        Group membership
        """
        user_obj = self.user
        if not user_obj.is_active:
            return False
        return perm in self.get_group_permissions(obj)

    def has_perms(self, perms, obj=None):
        """
        Determines if AccountUser has all of the given permissions based on
        to Group membership
        """
        user_obj = self.user
        if not user_obj.is_active:
            return False
        for perm in perms:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        """
        Determines if AccountUser has any permissions in the given app
        """
        user_obj = self.user
        if not user_obj.is_active:
            return False
        for perm in self.get_all_permissions(user_obj):
            if perm[:perm.index('.')] == app_label:
                return True
        return False


class AccountNote(models.Model):
    """allows recording update about Account"""
    account = models.ForeignKey(
        Account,
        related_name='notes',
        on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=255,
        help_text='Title of note'
    )
    body = models.TextField(
        help_text='Note content'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    modified_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        """meta details about AccountNotes"""
        ordering = ('-created_at',)

