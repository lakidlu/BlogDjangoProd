# Generated by Django 4.2.1 on 2023-06-09 14:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_connections_exchanges_summary_czas'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exchanges',
            old_name='_import',
            new_name='importt',
        ),
        migrations.AlterField(
            model_name='connections',
            name='czas',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 9, 14, 0, 22, 497843, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='exchanges',
            name='czas',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 9, 14, 0, 22, 498173, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='summary',
            name='czas',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 9, 14, 0, 22, 497470, tzinfo=datetime.timezone.utc)),
        ),
    ]
