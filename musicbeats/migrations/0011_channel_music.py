# Generated by Django 4.0 on 2021-12-30 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicbeats', '0010_remove_channel_music'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='music',
            field=models.CharField(default='', max_length=1000000),
        ),
    ]
