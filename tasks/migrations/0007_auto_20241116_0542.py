# Generated by Django 3.0.6 on 2024-11-16 00:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_auto_20241116_0542'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_tasks',
            old_name='last_updated_at',
            new_name='abbc',
        ),
        migrations.RenameField(
            model_name='user_tasks_log',
            old_name='last_updated_at',
            new_name='abbc',
        ),
    ]
