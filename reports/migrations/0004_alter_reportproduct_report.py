# Generated by Django 5.0.6 on 2024-06-22 09:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_alter_product_quantity_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportproduct',
            name='report',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reports.report'),
        ),
    ]
