# Generated by Django 4.1.5 on 2023-01-30 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_usertransactions_upload_proof'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertransactions',
            name='w_wallet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='withdrawal_wallet', to='accounts.userwallet'),
        ),
    ]
