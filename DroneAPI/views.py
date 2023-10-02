"""
A Django API for managing drones and medications.
"""

from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from rest_framework.decorators import APIView, api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .models import Drone, DroneMedicationDeliveryEvent, Medications
from .serializers import DroneMedicationDeliveryEventSerializer, DroneSerializer, MedicationsSerializer


class DroneView(APIView):
    """
    A view for managing drones.
    """

    def get(self, request: Request):
        """
        Get a list of all drones.

        ### Query parameters:

        * `available`: If `True`, only return drones that are available.

        ### Returns:

        A JSON object containing a list of drones.
        """

        params = request.query_params
        available = params.get("available")
        if available == "True":
            query_set = Drone.objects.filter(state=Drone.State.IDLE)
        else:
            query_set = Drone.objects.all()
        ser = DroneSerializer(query_set, many=True)
        return Response(ser.data)

    def post(self, request: Request):
        """
        Create a new drone.

        **Request body:**

        A JSON object containing the drone's data.

        **Returns:**

        A JSON object containing the newly created drone.
        """

        ser = DroneSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=status.HTTP_201_CREATED)


class MedicationsView(APIView):
    """
    A view for managing medications.
    """

    def get(self, request: Request):
        """
        Get a list of all medications.

        **Returns:**

        A JSON object containing a list of medications.
        """

        query_set = Medications.objects.all().select_related("drone")
        ser = MedicationsSerializer(query_set, many=True)
        return Response(ser.data)

    def post(self, request: Request):
        """
        Create a new medication.

        **Request body:**

        A JSON object containing the medication's data.

        **Returns:**

        A JSON object containing the newly created medication.
        """

        ser = MedicationsSerializer(data=request.data)
        drone = Drone.objects.get(pk=request.data.get("drone"))
        if drone and (drone.weight() + int(request.data.get("weight")) <= drone.weight_limit):
            if drone.battery_capacity >= 25:
                ser.is_valid(raise_exception=True)
                ser.save()
                drone.state = Drone.State.LOADED if drone.weight(
                ) == drone.weight_limit else Drone.State.LOADING
                drone.battery_capacity -= 20
                drone.save()
                return Response(ser.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": f"Drone-{drone.pk} battery level is below 25% and cannot be loaded!"},
                                status=status.HTTP_400_BAD_REQUEST,)
        else:
            return Response(
                {"message": f"Drone-{drone.pk} weight limit exceeded!"},
                status=status.HTTP_400_BAD_REQUEST,
            )


@api_view(["POST"])
def load_drone(request: Request, pk: int):
    """
    Load medications onto a drone.

    **Request body:**

    A JSON object containing a list of medication IDs.

    **Returns:**

    A JSON object containing a message indicating whether the medications were loaded successfully or not.
    """

    if request.method == "POST":

        meds = request.data.get("meds").split(",")
        drone = Drone.objects.get(pk=pk)
        if drone and drone.state == Drone.State.IDLE:
            if drone.battery_capacity >= 25:
                drone.state = Drone.State.LOADING
                drone.battery_capacity -= 20
                drone.save()
                for med in meds:
                    med_obj = Medications.objects.get(pk=int(med))
                    if drone.weight() + med_obj.weight <= drone.weight_limit:
                        med_obj.drone = drone
                        med_obj.save()
                    else:
                        drone.state = Drone.State.LOADED
                        drone.save()
                        return Response(
                            {
                                "message": f"Drone-{pk} is currently full and cannot take the medication order!"
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                else:
                    return Response({
                        "message": f"Drone-{pk} loaded successfully!"
                    }, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": f"Drone-{pk} battery level is below 25% and cannot be loaded!"})
        else:
            return Response({
                "message": f"Drone-{pk} is currently not on standby and cannot be loaded!"
            }, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(["GET"])
def get_drone_load(request: Request, pk: int):
    """
    Get a list of medications that are loaded onto a drone.

    **Request parameters:**

    * `pk`: The ID of the drone.

    **Returns:**

    A JSON object containing a list of medications.
    """

    if request.method == "GET":
        drone_load_data = Medications.objects.filter(drone=pk)
        ser = MedicationsSerializer(drone_load_data, many=True)
        return Response(ser.data)


@api_view(["GET"])
def get_drone_battery(request: Request, pk: int):
    """
    Get the battery level of a drone.

    **Request parameters:**

    * `pk`: The ID of the drone.

    **Returns:**

    A JSON object containing the drone's battery level.
    """

    if request.method == "GET":
        drone_battery = Drone.objects.get(pk=pk).battery_capacity
        return Response({"Battery Level": drone_battery})

@api_view(["POST"])
def send_drone_delivery(request: Request, pk: int):
    if request.method == "POST":
        drone = Drone.objects.get(pk=pk)
        drone.state = Drone.State.DELIVERING
        drone.save()
        medications = Medications.objects.filter(drone=pk)
        print(f"There are {len(medications)} related to this drone!")

        for medication in medications:
            drone_medication_delivery_event = DroneMedicationDeliveryEvent(
                drone=drone,
                medication=medication
            )
            drone_medication_delivery_event.save()

            medication.active = False
            medication.save()
        
        drone.state = Drone.State.DELIVERED
        drone.save()
        data = DroneMedicationDeliveryEvent.objects.filter(drone=pk).select_related()
        ser_data = DroneMedicationDeliveryEventSerializer(data, many=True)
        return Response(ser_data.data)