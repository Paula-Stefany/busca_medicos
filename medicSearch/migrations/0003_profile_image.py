# Generated by Django 5.0 on 2023-12-20 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicSearch', '0002_address_city_dayweek_speciality_state_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
