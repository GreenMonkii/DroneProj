from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Drone, Medications


class TestDataSetup(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.drone_data = {
            "model": 2,
            "weight_limit": 100,
            "battery_capacity": 100,
            "state": Drone.State.IDLE,
        }
        self.drone = Drone.objects.create(**self.drone_data)

        self.med_data = {
            "name": "Medication 1",
            "weight": 10,
            "code": "1122",
            "drone": self.drone,
        }
        self.medication = Medications.objects.create(**self.med_data)

    def assertResponseSuccess(self, response):
        self.assertTrue(200 <= response.status_code < 300)

    def assertResponseFail(self, response):
        self.assertFalse(200 <= response.status_code < 300)


class DroneViewTests(TestDataSetup):

    def test_get_all_drones(self):
        response = self.client.get('/api/drone')
        self.assertResponseSuccess(response)

    def test_get_available_drones(self):
        response = self.client.get('/api/drone?available=True')
        self.assertResponseSuccess(response)

    def test_create_drone(self):
        data = {
            "model": 2,
            "weight_limit": 200,
            "battery_capacity": 100,
            "state": Drone.State.IDLE,
            "SN": "4"
        }
        response = self.client.post('/api/drone', data, format='json')
        self.assertResponseSuccess(response)


class MedicationsViewTests(TestDataSetup):

    def test_get_all_medications(self):
        response = self.client.get('/api/meds')
        self.assertResponseSuccess(response)

    def test_create_medication(self):
        data = {
            "name": "New-Medication",
            "weight": 5,
            "drone": self.drone.pk,
            "code": "1022"
        }
        response = self.client.post('/api/meds', data, format='json')
        self.assertResponseSuccess(response)


class LoadDroneViewTests(TestDataSetup):

    def test_load_drone(self):
        data = {
            "meds": f"{self.medication.pk}",
        }
        response = self.client.post(
            f'/api/load/{self.drone.pk}', data, format='json')
        if self.drone.state == Drone.State.IDLE:
            self.assertResponseSuccess(response)
        else:
            self.assertResponseFail(response)


class GetDroneLoadViewTests(TestDataSetup):

    def test_get_drone_load(self):
        response = self.client.get(f'/api/meds/{self.drone.pk}')
        self.assertResponseSuccess(response)


class GetDroneBatteryViewTests(TestDataSetup):

    def test_get_drone_battery(self):
        response = self.client.get(f'/api/drone/{self.drone.pk}/battery')
        self.assertResponseSuccess(response)
