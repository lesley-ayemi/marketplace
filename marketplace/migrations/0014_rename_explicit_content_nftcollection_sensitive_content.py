# Generated by Django 4.1.5 on 2023-01-26 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0013_rename_customize_url_nftcollection_custom_url_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nftcollection',
            old_name='explicit_content',
            new_name='sensitive_content',
        ),
    ]
