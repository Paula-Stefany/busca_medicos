# Generated by Django 5.0 on 2024-04-08 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicSearch', '0006_alter_profile_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]
