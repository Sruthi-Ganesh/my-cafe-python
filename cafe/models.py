import uuid

from django.db import models


class Cafe(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=10)
    description = models.CharField(max_length=255)
    logo = models.CharField(max_length=25)
    location = models.CharField(max_length=10)


class EmployeeCafe(models.Model):
    employee = models.ForeignKey('employee.Employee', on_delete=models.CASCADE)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    employee_start_date = models.DateTimeField(auto_now_add=True)
