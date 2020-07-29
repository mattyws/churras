from django.db import models

# Create your models here.

class Employee(models.Model):
    email = models.EmailField(primary_key=True)
    isDrinking = models.BooleanField(default=False)

class Guest(models.Model):
    email = models.EmailField(primary_key=True)
    isDrinking = models.BooleanField(default=False)
    employee = models.OneToOneField(Employee, related_name="guest", on_delete=models.CASCADE, default=None, null=True)

