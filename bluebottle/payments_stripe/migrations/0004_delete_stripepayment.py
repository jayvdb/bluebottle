# Generated by Django 3.0.8 on 2020-10-02 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments_logger', '0002_delete_paymentlogentry'),
        ('payments', '0007_auto_20201002_1055'),
        ('payments_stripe', '0003_auto_20190130_1231'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StripePayment',
        ),
    ]
