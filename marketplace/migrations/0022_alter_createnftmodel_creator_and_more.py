# Generated by Django 4.1.5 on 2023-04-14 09:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('marketplace', '0021_alter_createnftmodel_gas_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createnftmodel',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator_nft', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='nftcollection',
            name='banner_image',
            field=models.ImageField(blank=True, default='', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='nftcollection',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_category', to='marketplace.category'),
        ),
        migrations.AlterField(
            model_name='nftcollection',
            name='featured_image',
            field=models.ImageField(blank=True, default='', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='nftcollection',
            name='logo_image',
            field=models.ImageField(blank=True, default='', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='nftcollection',
            name='user_collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_collections', to=settings.AUTH_USER_MODEL),
        ),
    ]