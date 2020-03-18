from django import forms

from vapor_manager.clients.models import Client, ClientContact


class ClientCreateForm(forms.ModelForm):
    contact_name = forms.CharField(
        max_length=255,
        label="Primary Contact Name",
        required=False
    )
    contact_email = forms.EmailField(
        max_length=255,
        label="Primary Contact Email",
        required=False
    )
    contact_phone = forms.CharField(
        max_length=15,
        label="Primary Contact Phone",
        required=False
    )
    contact_position = forms.CharField(
        max_length=255,
        label="Primary Contact Position",
        required=False
    )

    class Meta:
        model = Client
        fields = ['name', 'contact_name', 'contact_email', 'contact_phone', 'contact_position']

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)
        self.contact = ClientContact()
        self.fields['name'].label = 'Client Name'
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Client Name'
        self.fields['contact_name'].widget.attrs['placeholder'] = 'Enter Primary Contact Name'
        self.fields['contact_email'].widget.attrs['placeholder'] = 'Enter Primary Contact Email'
        self.fields['contact_phone'].widget.attrs['placeholder'] = 'Enter Primary Contact Phone'
        self.fields['contact_position'].widget.attrs['placeholder'] = 'Enter Primary Contact Position'

    def save(self, commit=True):
        data = self.cleaned_data
        self.instance.account = self.account
        client = super().save(commit)
        if data.get('contact_name') or data.get('contact_email') or data.get('contact_phone'):
            self.contact = ClientContact(
                name=data.get('contact_name'),
                email=data.get('contact_email'),
                phone=data.get('contact_phone'),
                position=data.get('contact_position'),
                is_primary=True,
                client=client,
            )
            if commit:
                self.contact.save()
        return client
