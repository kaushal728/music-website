# Generated by Django 4.0 on 2021-12-29 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicbeats', '0006_history'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='credit',
        ),
        migrations.AlterField(
            model_name='song',
            name='image',
            field=models.ImageField(upload_to='images'),
        ),
        migrations.AlterField(
            model_name='song',
            name='song',
            field=models.FileField(upload_to='songs'),
        ),
    ]
