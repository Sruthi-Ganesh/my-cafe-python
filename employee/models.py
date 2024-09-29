from django.db import models
from django.db.models import Max


class Employee(models.Model):
    class Gender(models.TextChoices):
        MALE = "M"
        FEMALE = "F"

    id = models.CharField(primary_key=True, editable=False, max_length=9)
    name = models.CharField(max_length=10)
    email_address = models.EmailField()
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(choices=Gender.choices, max_length=2)

    def save(self, **kwargs) -> None:
        if not self.id:
            id_max = Employee.objects.aggregate(id_max=Max('id'))['id_max']
            if id_max is not None:
                id_max_split = id_max.split("UI")
                if len(id_max_split) > 1:
                    id_max_int = int(id_max.split("UI")[1])
                    self.id = "{}{:07d}".format('UI', id_max_int + 1)
            else:
                self.id = "{}{:07d}".format('UI', 1)
        super().save(**kwargs)
