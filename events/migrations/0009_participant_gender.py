# Generated by Django 4.2.3 on 2024-09-28 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_remove_incharge_events_incharge_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'female')], default=1, max_length=10),
            preserve_default=False,
        ),
    ]
