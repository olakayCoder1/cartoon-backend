# Generated by Django 4.2.7 on 2024-01-24 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_paymenttransaction_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='image',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='additional_info',
            field=models.TextField(null=True),
        ),
    ]
