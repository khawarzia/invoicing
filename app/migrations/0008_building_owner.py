# Generated by Django 3.2 on 2022-08-20 19:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20220821_0015'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.invoice_owner'),
        ),
    ]