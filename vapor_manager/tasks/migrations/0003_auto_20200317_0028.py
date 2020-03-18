# Generated by Django 3.0.4 on 2020-03-17 00:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('projects', '0003_auto_20200317_0028'),
        ('tasks', '0002_auto_20200313_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='users.Account'),
        ),
        migrations.AlterField(
            model_name='task',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='projects.Project'),
        ),
        migrations.AlterField(
            model_name='tasknote',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='tasks.Task'),
        ),
    ]