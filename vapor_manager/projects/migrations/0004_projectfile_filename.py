# Generated by Django 3.0.4 on 2020-03-17 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20200317_0028'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectfile',
            name='filename',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]
