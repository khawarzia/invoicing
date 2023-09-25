# Generated by Django 3.2.15 on 2023-07-01 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20230701_0108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartment',
            name='curr_tenant',
        ),
        migrations.RemoveField(
            model_name='apartment',
            name='tenant_hist',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='tenant',
        ),
        migrations.RemoveField(
            model_name='maintenance_invoice',
            name='tenant',
        ),
        migrations.DeleteModel(
            name='prev_tenants',
        ),
    ]