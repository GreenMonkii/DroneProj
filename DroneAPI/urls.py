from django.urls import path
from .views import *
urlpatterns = [
    path("drone", DroneView.as_view(), name="drone_view"),
    path("meds", MedicationsView.as_view(), name="meds_view"),
    path("load/<int:pk>", load_drone, name="load_drone_view"),
    path("meds/<int:pk>", get_drone_load, name="gdl_view"),
    path("drone/<int:pk>/battery", get_drone_battery, name="gdb_view"),
    path("drone/<int:pk>/delivery", send_drone_delivery, name="sdd_view")
]