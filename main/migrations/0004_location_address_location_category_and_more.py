# Generated by Django 4.1.3 on 2022-11-20 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='address',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='location',
            name='category',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='location',
            name='lot_address',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='location',
            name='phone',
            field=models.CharField(blank=True, max_length=13),
        ),
        migrations.AddField(
            model_name='location',
            name='time',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='location',
            name='url',
            field=models.URLField(blank=True),
        ),
    ]