from django.db import models
from django.db.models import Max


class Employee(models.Model):
    class Gender(models.TextChoices):
        MALE = "1"
        FEMALE = "2"

    id = models.CharField(primary_key=True, editable=False, max_length=9)
    name = models.CharField(max_length=10)
    email_address = models.EmailField()
    phone_number = models.IntegerField()
    gender = models.CharField(choices=Gender.choices, max_length=2)
    employee_cafe = models.OneToOneField("cafe.EmployeeCafe", on_delete=models.SET_NULL,
                                         null=True, blank=True, related_name='emp')

    def save(self, **kwargs) -> None:
        if not self.id:
            max = Employee.objects.aggregate(id_max=Max('id'))['id_max']
            self.id = "{}{:07d}".format('UI', max if max is not None else 1)
