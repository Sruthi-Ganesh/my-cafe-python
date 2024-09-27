import uuid

from django.db import models
from django_countries.fields import CountryField


class Cafe(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=10)
    description = models.CharField(max_length=255)
    logo = models.ImageField(null=True, blank=True, upload_to="logo/")
    location = CountryField()


class EmployeeCafe(models.Model):
    employee = models.OneToOneField('employee.Employee', on_delete=models.CASCADE,
                                    related_name='employee_cafe')
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE,
                             related_name="employee_cafes")
    employee_start_date = models.DateTimeField(auto_now_add=True)
