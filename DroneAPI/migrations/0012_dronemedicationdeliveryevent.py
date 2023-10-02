# Generated by Django 4.2.5 on 2023-10-02 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DroneAPI', '0011_alter_drone_battery_capacity'),
    ]

    operations = [
        migrations.CreateModel(
            name='DroneMedicationDeliveryEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_time', models.DateTimeField(auto_now_add=True)),
                ('drone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DroneAPI.drone')),
                ('medication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DroneAPI.medications')),
            ],
        ),
    ]