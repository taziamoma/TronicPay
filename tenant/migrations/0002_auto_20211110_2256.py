# Generated by Django 3.1.7 on 2021-11-11 04:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('tenant', '0001_initial'),
        ('landlords', '0002_unit_landlord'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicerequests',
            name='tenant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servicerequestss', to='users.tenant'),
        ),
        migrations.AddField(
            model_name='servicerequests',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servicerequestss', to='landlords.unit'),
        ),
        migrations.AddField(
            model_name='scheduledpayments',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to='tenant.invoice'),
        ),
        migrations.AddField(
            model_name='scheduledpayments',
            name='tenant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tenant', to='users.tenant'),
        ),
        migrations.AddField(
            model_name='payments',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paymentss', to='tenant.invoice'),
        ),
        migrations.AddField(
            model_name='payments',
            name='tenant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.tenant'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='tenant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoicess', to='users.tenant'),
        ),
        migrations.AddField(
            model_name='bankaccounts',
            name='tenant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bankaccountss', to='users.tenant'),
        ),
    ]
