# Generated by Django 3.0.4 on 2020-03-13 14:32

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import fernet_fields.fields
import model_utils.fields
import uuid
import vapor_manager.servers.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', model_utils.fields.StatusField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=100, no_check_for_status=True, verbose_name='status')),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status', verbose_name='status changed')),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('hostname', models.CharField(max_length=255)),
                ('public_ip', models.GenericIPAddressField(blank=True, null=True)),
                ('platform', models.CharField(max_length=255)),
                ('capacity', models.CharField(blank=True, max_length=255, null=True)),
                ('private_info', fernet_fields.fields.EncryptedTextField(blank=True, null=True)),
                ('cost', models.PositiveIntegerField(default=0, help_text='Monthly cost in whole cents')),
                ('slots', models.PositiveIntegerField(default=10, help_text='Number of sites available on this server')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServerNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('details', models.TextField()),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servers.Server')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServerFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('file', models.FileField(upload_to=vapor_manager.servers.models.account_server_path)),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='servers.Server')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
