# Generated by Django 5.1.6 on 2025-03-21 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watch',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
    ]
