# Generated by Django 4.2.7 on 2023-11-29 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portrait', '0002_alter_purchaseimage_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseimage',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=6),
            preserve_default=False,
        ),
    ]
