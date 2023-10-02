import time
from django.core.management.base import BaseCommand
import random
from DroneAPI.models import Drone, Medications


class Command(BaseCommand):
    """Charges A Drone with a provided Drone ID"""

    help = "Charges A Drone with a provided Drone ID"

    def add_arguments(self, parser):
        """Adds command line arguments"""
        parser.add_argument(
            "--drone",
            type=int,
            help="Charge Specific Drone",
        )

    def handle(self, *args, **options):
        """Charges the drone"""
        pk = options["drone"]
        drone = Drone.objects.get(pk=pk)

        if drone.state != Drone.State.IDLE or drone.battery_capacity == 100:
            self.stdout.write(
                self.style.WARNING(
                    f"Drone-{pk} must be in IDLE state and must not be fully charged to perform this operation!")
            )

        if drone.state == Drone.State.IDLE and drone.battery_capacity != 100:
            while drone.battery_capacity + 15 <= 100:
                time.sleep(5)
                drone.battery_capacity += 15
                drone.save()
                self.stdout.write(
                    self.style.WARNING(
                        f"Drone-{pk} has been charged to {drone.battery_capacity}%")
                )
            else:
                time.sleep(2)
                drone.battery_capacity = 100
                drone.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Drone-{pk} has been charged successfully!")
                )
