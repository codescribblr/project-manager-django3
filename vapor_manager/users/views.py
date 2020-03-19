from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "email"
    slug_url_kwarg = "email"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['accounts'] = self.object.accounts.all()
        return data


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"email": self.request.user.email})

    def get_object(self):
        return User.objects.get(email=self.request.user.email)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS, _("User Profile successfully updated")
        )
        return super().form_valid(form)


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"email": self.request.user.email})


