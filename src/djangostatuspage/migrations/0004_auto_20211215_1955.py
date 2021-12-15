# Generated by Django 3.2.10 on 2021-12-15 17:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('djangostatuspage', '0003_alter_incident_origin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incident',
            name='is_hidden',
        ),
        migrations.AddField(
            model_name='incident',
            name='is_visible',
            field=models.BooleanField(default=True, verbose_name='Visible'),
        ),
        migrations.CreateModel(
            name='SystemCategory',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('system_category_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_visible', models.BooleanField(default=True, verbose_name='Visible')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='system_category_created_set', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='system_category_updated_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='System',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('system_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('alias', models.CharField(max_length=128, null=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_visible', models.BooleanField(default=True, verbose_name='Visible')),
                ('is_enabled', models.BooleanField(default=True, verbose_name='Enabled')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='djangostatuspage.systemcategory')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='system_created_set', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='system_updated_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='incident',
            name='affected_system',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='djangostatuspage.system'),
        ),
    ]