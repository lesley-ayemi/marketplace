# Generated by Django 4.1.5 on 2023-02-10 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_usertransactions_w_gas_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertransactions',
            name='w_gas_fee',
            field=models.FloatField(blank=True, default=0.8, null=True),
        ),
    ]