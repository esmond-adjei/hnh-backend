# Generated by Django 4.2.2 on 2023-07-24 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0014_alter_room_room_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_id',
            field=models.CharField(max_length=10, primary_key=True, serialize=False, unique=True),
        ),
    ]