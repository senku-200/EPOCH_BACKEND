# Generated by Django 5.1.1 on 2024-09-23 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='time_limit',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
