from django import forms

from vapor_manager.servers.models import Server


class ProjectAttachServerForm(forms.Form):
    server = forms.ModelChoiceField(queryset=Server.objects.none(), required=True, empty_label=None)

    def __init__(self, *args, **kwargs):
        account = kwargs.pop('account', None)
        super().__init__(*args, **kwargs)
        if account:
            self.fields['server'].queryset = Server.objects.active().by_account(account).all()
