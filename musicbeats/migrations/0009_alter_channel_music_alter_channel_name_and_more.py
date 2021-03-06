# Generated by Django 4.0 on 2021-12-29 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicbeats', '0008_channel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='music',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='channel',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='history',
            name='music_id',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='watchlater',
            name='video_id',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
