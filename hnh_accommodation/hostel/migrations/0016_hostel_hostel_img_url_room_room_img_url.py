# Generated by Django 4.2.2 on 2023-07-25 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0015_alter_room_room_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostel',
            name='hostel_img_url',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='room',
            name='room_img_url',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]