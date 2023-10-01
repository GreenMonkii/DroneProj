from django.core.management.base import BaseCommand
from DroneAPI.models import Drone, DroneBatteryLevelEvent


class Command(BaseCommand):
    help = 'Check drone battery levels and create history/audit event log for this'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "--drone",
            type=int,
            help="Get Battery Level for Specific Drone",
        )

    def handle(self, *args, **options):
        # Get all drones
        drones = Drone.objects.all()

        def out(drone):
            # Get the drone's battery level.
            drone_battery_level = drone.battery_capacity

            # Write the battery level to the console, with a different color depending on the level.
            if drone_battery_level > 25:
                self.stdout.write(self.style.SUCCESS(
                    f"Drone-{drone.pk} battery level is at {drone_battery_level}%"))
            elif drone_battery_level == 0:
                self.stderr.write(self.style.ERROR(
                    f"Drone-{drone.pk} battery level is at {drone_battery_level}%"))
            else:
                self.stdout.write(self.style.WARNING(
                    f"Drone-{drone.pk} battery level is at {drone_battery_level}%"))

        # Initialize the `battery_level` variable in the function closure.
        out.battery_level = None

        # Iterate over all drones and check their battery levels
        if not options.get("drone"):
            for drone in drones:
                out(drone)
                out.battery_level = drone.battery_capacity
                DroneBatteryLevelEvent.objects.create(
                    drone=drone,
                    battery_level=out.battery_level,
                )
            self.stdout.write(
                self.style.SUCCESS(
                    f"\nThe battery levels of all drones have been successfully checked and added to the event log.")
            )

        else:
            drone = Drone.objects.get(pk=options.get("drone"))
            out(drone)
            out.battery_level = drone.battery_capacity
            DroneBatteryLevelEvent.objects.create(
                drone=drone,
                battery_level=out.battery_level,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"\nThe battery level Drone-{options.get('drone')} has been successfully checked and added to the event log.")
            )
