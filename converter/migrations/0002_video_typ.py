# Generated by Django 4.0.5 on 2023-01-19 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='typ',
            field=models.CharField(default='mp3', max_length=20),
        ),
    ]
