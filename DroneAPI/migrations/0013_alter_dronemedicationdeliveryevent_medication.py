# Generated by Django 4.2.5 on 2023-10-02 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DroneAPI', '0012_dronemedicationdeliveryevent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dronemedicationdeliveryevent',
            name='medication',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='DroneAPI.medications'),
        ),
    ]