# Generated by Django 4.2.2 on 2023-07-22 02:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0011_hostel_manager'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Facility',
            new_name='Amenity',
        ),
        migrations.RenameField(
            model_name='room',
            old_name='facilities',
            new_name='amenities',
        ),
    ]
