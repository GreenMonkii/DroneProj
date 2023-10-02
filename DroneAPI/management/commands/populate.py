from django.core.management.base import BaseCommand
import random
from DroneAPI.models import Drone, Medications

class Command(BaseCommand):
    help = 'Prepopulates the database with 10 drones and 50 medications.'

    def handle(self, *args, **options):
        # Create 10 drones
        drones = []
        for i in range(10):
            drone = Drone(
                model=random.choice(Drone.MODEL.choices)[0],
                weight_limit=500,
                battery_capacity=100,
                state=Drone.State.IDLE
            )
            drones.append(drone)

        # Create 50 medications
        medications = []
        for i in range(50):
            medication = Medications(
                name=f"Medication {i + 1}",
                weight=random.randint(1, 100),
                code=f"MED{i + 1}",
                drone=random.choice(drones)
            )
            medications.append(medication)

        # Save all of the drones and medications to the database
        Drone.objects.bulk_create(drones)
        Medications.objects.bulk_create(medications)

        self.stdout.write(self.style.SUCCESS('The database has been prepopulated with 10 drones and 50 medications.'))
