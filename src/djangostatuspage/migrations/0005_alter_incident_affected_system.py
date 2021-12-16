# Generated by Django 3.2.10 on 2021-12-15 17:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangostatuspage', '0004_auto_20211215_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='affected_system',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='djangostatuspage.system'),
        ),
    ]
