# Generated by Django 3.2.15 on 2023-04-18 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20230418_2130'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='invoice_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='maintenance_invoice',
            name='invoice_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='type_of_user',
            field=models.CharField(choices=[('d', 'Default'), ('v', 'Read Only'), ('w', 'Read and Write')], default='d', max_length=20),
        ),
    ]
