# Generated by Django 5.0.4 on 2024-04-06 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0002_rename_district_schools_district_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schools',
            old_name='district_name',
            new_name='city',
        ),
    ]
