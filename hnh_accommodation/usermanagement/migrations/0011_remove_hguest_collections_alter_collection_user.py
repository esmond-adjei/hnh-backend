# Generated by Django 4.2.2 on 2023-08-16 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0010_alter_hguest_collections'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hguest',
            name='collections',
        ),
        migrations.AlterField(
            model_name='collection',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collections', to='usermanagement.hguest'),
        ),
    ]