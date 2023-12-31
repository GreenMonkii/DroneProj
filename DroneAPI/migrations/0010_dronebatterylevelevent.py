# Generated by Django 4.2.5 on 2023-10-01 20:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DroneAPI', '0009_alter_medications_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='DroneBatteryLevelEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('battery_level', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100, 'Battery Level Limit is 100%')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('drone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DroneAPI.drone')),
            ],
        ),
    ]
