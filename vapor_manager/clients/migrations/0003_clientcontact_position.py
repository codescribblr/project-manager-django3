# Generated by Django 3.0.4 on 2020-03-16 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_auto_20200313_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientcontact',
            name='position',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
