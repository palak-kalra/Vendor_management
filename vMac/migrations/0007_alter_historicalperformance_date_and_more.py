# Generated by Django 4.2.7 on 2023-12-03 13:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vMac', '0006_po_delivered_at_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalperformance',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 3, 18, 35, 15, 419844)),
        ),
        migrations.AlterField(
            model_name='po',
            name='delivery_date',
            field=models.DateTimeField(editable=False),
        ),
        migrations.AlterField(
            model_name='po',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 3, 18, 35, 15, 419844)),
        ),
        migrations.AlterField(
            model_name='po',
            name='po_number',
            field=models.CharField(editable=False, max_length=30, unique=True),
        ),
    ]
