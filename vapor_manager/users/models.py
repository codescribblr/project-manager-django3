import hashlib

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, Group as UserGroup, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel, StatusModel, UUIDModel

from vapor_manager.accounts.models import Account


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class AbstractEmailUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), max_length=254, unique=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.')
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.')
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        abstract = True
        ordering = ['email']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Sends an email to this User."""

        send_mail(subject, message, from_email, [self.email], **kwargs)


class User(UUIDModel, AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    current_account = models.ForeignKey('accounts.Account', null=True, blank=True, on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"email": self.email})

    def __str__(self):
        return '{name} <{email}>'.format(
            name=self.name,
            email=self.email,
        )

    def get_full_name(self):
        return self.name

    def activate(self, account=None):
        if account is None:
            account = Account.objects.create(owner=self, company=self.email)
            account.users.add(self)
        self.current_account = account
        self.save()

    @property
    def profile_image_url(self):
        return f"https://gravatar.com/avatar/{hashlib.md5(self.email.encode('utf-8')).hexdigest()}"
