# Generated by Django 4.2.5 on 2023-09-29 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DroneAPI', '0007_alter_drone_serial_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medications',
            name='drone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Medications', to='DroneAPI.drone'),
        ),
    ]
