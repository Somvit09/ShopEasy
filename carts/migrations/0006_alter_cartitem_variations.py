# Generated by Django 4.0.1 on 2023-03-09 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_productgallerymodel_options'),
        ('carts', '0005_cartitem_user_alter_cartitem_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='variations',
            field=models.ManyToManyField(blank=True, to='store.VariationModel'),
        ),
    ]
