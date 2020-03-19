from allauth.account.forms import SignupForm
from django import forms


class NameSignupForm(SignupForm):
    name = forms.CharField(max_length=55, label='Name')

    def save(self, request):
        user = super().save(request)
        user.name = self.cleaned_data['name']
        user.save()
        return user


