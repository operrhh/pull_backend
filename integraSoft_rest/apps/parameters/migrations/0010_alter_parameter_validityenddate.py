# Generated by Django 4.0 on 2023-11-10 18:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('parameters', '0009_alter_parameter_validityenddate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameter',
            name='ValidityEndDate',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 9, 18, 55, 49, 657789, tzinfo=utc)),
        ),
    ]