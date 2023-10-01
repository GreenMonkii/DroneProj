from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator
# Create your models here.


class Drone(models.Model):
    class State(models.TextChoices):
        IDLE = "IDLE",
        LOADING = "LOADING"
        LOADED = "LOADED"
        DELIVERING = "DELIVERING"
        DELIVERED = "DELIVERED"
        RETURNING = "RETURNING"
    MODEL = models.IntegerChoices(
        "MODEL", "Lightweight Middleweight Cruiserweight Heavyweight")
    serial_number = models.AutoField(primary_key=True)
    model = models.IntegerField(choices=MODEL.choices)
    weight_limit = models.PositiveIntegerField(
        validators=[MaxValueValidator(500, "Weight cannot be above 500 Grams")])
    battery_capacity = models.PositiveIntegerField(
        validators=[MaxValueValidator(100, "Battery Percentage Limit is 100%")], default=100, editable=False)
    state = models.CharField(choices=State.choices, max_length=255)

    def __str__(self) -> str:
        return f"Drone {self.serial_number}"

    def weight(self) -> int:
        meds = self.Medications.all()
        return sum(map(lambda x: x.weight, meds))

class Medications(models.Model):
    name = models.CharField(max_length=255, validators=[RegexValidator(
        regex=r"^[a-zA-Z0-9-_]+$", message="Only Letters, Numbers, '-' and '_' are allowed", code="Invalid Input")])
    weight = models.PositiveIntegerField()
    code = models.CharField(max_length=255, validators=[RegexValidator(
        regex=r"^[A-Z0-9_]+$", message="Only Uppercase Letters, Numbers and '_' are allowed", code="Invalid Code")])
    image = models.ImageField(upload_to="uploads/", blank=True)
    drone = models.ForeignKey(Drone, on_delete=models.PROTECT, related_name="Medications")

    def __str__(self) -> str:
        return f"{self.name} - {self.code}, to be delivered by {self.drone}"
    
    class Meta:
        verbose_name = "Medication"
        verbose_name_plural = "Medications"