# Generated by Django 3.2 on 2022-08-20 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20220815_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='bank_of_transfer',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='transfer_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
