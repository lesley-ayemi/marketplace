# Generated by Django 4.1.5 on 2023-01-21 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_moredetails_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moredetails',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('woman', 'Woman'), ('transgender', 'Transgender'), ('non-binary/non-conforming', 'Non Binary'), ('Prefer not to respond', 'Prefer Not To Respond')], default='', max_length=100),
        ),
    ]
