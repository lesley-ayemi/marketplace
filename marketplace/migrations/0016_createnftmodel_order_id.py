# Generated by Django 4.1.5 on 2023-02-01 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0015_alter_createnftmodel_upload_nft'),
    ]

    operations = [
        migrations.AddField(
            model_name='createnftmodel',
            name='order_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
