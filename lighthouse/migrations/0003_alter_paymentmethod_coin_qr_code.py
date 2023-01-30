# Generated by Django 4.1.5 on 2023-01-30 02:02

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lighthouse', '0002_paymentmethod_coin_network_paymentmethod_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmethod',
            name='coin_qr_code',
            field=cloudinary.models.CloudinaryField(default='', max_length=255, verbose_name='image'),
        ),
    ]
