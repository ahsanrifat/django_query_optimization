# Generated by Django 4.0rc1 on 2022-03-14 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0007_city_land_city_mayor'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='area_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='area',
            name='chairman',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='area',
            name='maintain_cost',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]