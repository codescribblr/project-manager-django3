# Generated by Django 3.0.4 on 2020-03-19 17:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='accountuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='accountnote',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='accounts.Account'),
        ),
        migrations.AddField(
            model_name='accountinvite',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invites', to='accounts.Account'),
        ),
        migrations.AddField(
            model_name='account',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this account belongs to. An account will get all permissions granted to each of its groups.', to='accounts.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='account',
            name='owner',
            field=models.ForeignKey(help_text='User who owns or administrates this account', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='account', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='account',
            name='permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permission for this account', to='accounts.Permission', verbose_name='permissions'),
        ),
        migrations.AddField(
            model_name='account',
            name='users',
            field=models.ManyToManyField(blank=True, help_text='Members of the company represented by this account.', related_name='accounts', through='accounts.AccountUser', to=settings.AUTH_USER_MODEL, verbose_name='users'),
        ),
    ]
