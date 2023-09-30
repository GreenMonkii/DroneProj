from rest_framework import serializers
from .models import *


class DroneSerializer(serializers.ModelSerializer):
    SN = serializers.CharField(source="serial_number")
    weight = serializers.SerializerMethodField("weight")
    class Meta:
        model = Drone
        fields = ["model", "weight_limit", "battery_capacity", "state", "SN", "weight"]
    
    def weight(self, drone:Drone) -> int:
        return drone.weight()

class MedicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medications
        fields = ["name", "weight", "code", "image", "drone"]
