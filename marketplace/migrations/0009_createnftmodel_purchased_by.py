# Generated by Django 4.1.5 on 2023-01-25 04:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('marketplace', '0008_alter_createnftmodel_collection'),
    ]

    operations = [
        migrations.AddField(
            model_name='createnftmodel',
            name='purchased_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchased_by_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
