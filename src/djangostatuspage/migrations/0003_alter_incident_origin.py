# Generated by Django 3.2.10 on 2021-12-15 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangostatuspage', '0002_alter_incident_id_at_origin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='origin',
            field=models.CharField(blank=True, choices=[('manual', 'Manual')], max_length=32, null=True),
        ),
    ]
