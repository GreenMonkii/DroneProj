from django.shortcuts import render
from rest_framework.decorators import APIView, api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *


class DroneView(APIView):
    def get(self, request: Request):
        params = request.query_params
        available = params.get("available")
        query_set = Drone.objects.filter(
            state=Drone.State.IDLE) if (available == "True") else Drone.objects.all()
        ser = DroneSerializer(query_set, many=True)
        return Response(ser.data)

    def post(self, request: Request):
        ser = DroneSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status.HTTP_201_CREATED)


class Medicationsview(APIView):
    def get(self, request: Request):
        query_set = Medications.objects.all().select_related()
        ser = MedicationsSerializer(query_set, many=True)
        return Response(ser.data)

    def post(self, request: Request):
        ser = MedicationsSerializer(data=request.data)
        drone = Drone.objects.get(pk=(request.data.get("drone")))
        if drone and ((drone.weight() + int(request.data.get("weight")) <= drone.weight_limit)):
            ser.is_valid(raise_exception=True)
            ser.save()
            drone.state = drone.State.LOADED if drone.weight() > 0 else drone.state
            drone.battery_capacity -= 20
            drone.save()
            return Response(ser.data, status.HTTP_201_CREATED)
        else:
            return Response({"message": f"Drone-{drone.pk} weight limit exceeded!"}, status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def load_drone(request: Request, pk: int):
    if request.method == "POST":
        meds = request.data.get("meds").split(",")
        drone = Drone.objects.get(pk=pk)
        if drone and (drone.state == drone.State.IDLE):
            drone.state = drone.State.LOADING
            drone.battery_capacity -= 20
            drone.save()
            for med in meds:
                med_obj = Medications.objects.get(pk=int(med))
                if (drone.weight() + med_obj.weight <= drone.weight_limit):
                    med_obj.drone = drone
                    med_obj.save()
                else:
                    drone.state = drone.State.LOADED
                    drone.save()
                    return Response({"message": f"Drone-{pk} is currently full and cannot take the medication order!"}, status.HTTP_400_BAD_REQUEST)
            return Response({"message": f"Medications Added to Drone-{pk}"}, status.HTTP_201_CREATED)
        else:
            return Response({"message": f"Drone-{pk} is Full!"}, status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_drone_load(request: Request, pk: int):
    if request.method == "GET":
        drone_load_data = Medications.objects.filter(drone=pk)
        ser = MedicationsSerializer(drone_load_data, many=True)
        return Response(ser.data)


@api_view(["GET"])
def get_drone_battery(request: Request, pk: int):
    if request.method == "GET":
        drone_battery = Drone.objects.get(pk=pk).battery_capacity
        return Response({"Battery Level": drone_battery})
