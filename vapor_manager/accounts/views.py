import uuid

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, ListView
from django.views.generic.detail import SingleObjectMixin

from vapor_manager.accounts.models import Account, AccountInvite

User = get_user_model()


class AccountListView(LoginRequiredMixin, ListView):

    model = Account
    context_object_name = 'accounts'

    def get_queryset(self):
        return self.request.user.accounts.all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        return data


class AccountSwitchView(LoginRequiredMixin, RedirectView):
    http_method_names = ['get', ]
    url = reverse_lazy('dashboard')

    def get(self, request, *args, **kwargs):
        account = get_object_or_404(Account, pk=kwargs.get('pk'), users=request.user)
        request.user.current_account = account
        request.user.save()
        messages.add_message(
            self.request, messages.SUCCESS, _("Account switched successfully")
        )
        return super().get(request, *args, **kwargs)


class AccountDetailView(LoginRequiredMixin, DetailView):

    model = Account

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        return data


class AccountUpdateView(LoginRequiredMixin, UpdateView):

    model = Account
    fields = ["company"]

    def get_success_url(self):
        return reverse("accounts:detail", kwargs={"pk": self.object.pk})

    def get_object(self):
        return Account.objects.get(pk=self.kwargs.get('pk'), users=self.request.user)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS, _("Account Profile successfully updated")
        )
        return super().form_valid(form)


class AccountInviteView(LoginRequiredMixin, RedirectView):
    http_method_names = ['post', ]

    def get(self, request, *args, **kwargs):
        account = get_object_or_404(Account, pk=kwargs.get('pk'), owner=request.user)
        email = request.POST.get('email')
        if email:
            if User.objects.filter(email=email, account=account).exists():
                messages.add_message(
                    self.request, messages.ERROR, _("You must provide a valid email address to invite a collaborator.")
                )
                return super().get(request, *args, **kwargs)

            invite = AccountInvite.objects.create(
                account=account,
                email=email,
            )

            # TODO: send email with invite code
            print(reverse('accounts:invite.join', kwargs={'account_pk': account.pk, 'pk': invite.pk}))

            messages.add_message(
                self.request, messages.SUCCESS, _("Account Invite Sent Successfully")
            )
        else:
            messages.add_message(
                self.request, messages.ERROR, _("You must provide a valid email address to invite a collaborator.")
            )
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, pk):
        return reverse('accounts:detail', kwargs={'pk': pk})


class AccountInviteJoinView(LoginRequiredMixin, SingleObjectMixin, RedirectView):
    model = AccountInvite
    http_method_names = ['get', ]
    fields = ['get']

    def get_queryset(self):
        return super().get_queryset().filter(account=self.kwargs.get('account_pk'), used=False, expires__gte=timezone.now())

    def get(self, request, *args, **kwargs):
        account = get_object_or_404(Account, pk=self.kwargs.get('account_pk'))
        invite = self.get_object()
        if invite:
            invite.used = True
            invite.save()
            # try to find the user in the db
            user = User.objects.get(email=invite.email)
            # if found, add them to the account
            if user:
                account.users.add(user)
                user.current_account = account
                user.save()
                messages.add_message(
                    self.request, messages.SUCCESS, _(f"You have been added to {account.company}'s account.")
                )
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                user = User.objects.create(email=invite.email, username=invite.email, current_account=account)
                account.users.add(user)
            # if not found, create the new user and add them to the account
                # mark email as verified (since they got the invite)
                # redirect the user to the reset password page to create a new password for their account
            messages.add_message(
                self.request, messages.SUCCESS, _(f"You have been added to the {account.company} account.")
            )
        else:
            messages.add_message(
                self.request, messages.ERROR, _("This invitation has expired. Please request another "
                                                "invite from the company you wish to collaborate with.")
            )
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self):
        return reverse('users:profile')
