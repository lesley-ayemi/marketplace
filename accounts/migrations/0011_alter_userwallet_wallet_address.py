# Generated by Django 4.1.5 on 2023-01-30 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_userwallet_wallet_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userwallet',
            name='wallet_address',
            field=models.TextField(),
        ),
    ]