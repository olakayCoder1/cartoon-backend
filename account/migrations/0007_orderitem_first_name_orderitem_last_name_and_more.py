# Generated by Django 4.2.7 on 2024-01-24 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_orderitem_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='first_name',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='last_name',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='phone',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
