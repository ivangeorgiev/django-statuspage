# Generated by Django 3.2.10 on 2021-12-15 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangostatuspage', '0010_alter_incident_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incidentupdate',
            name='title',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
