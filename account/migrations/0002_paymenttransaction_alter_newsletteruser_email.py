# Generated by Django 4.2.7 on 2024-01-24 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('token', models.CharField(max_length=100, null=True, unique=True)),
                ('status', models.CharField(choices=[('success', 'success'), ('failed', 'failed'), ('pending', 'pending')], default='pending', max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='newsletteruser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
