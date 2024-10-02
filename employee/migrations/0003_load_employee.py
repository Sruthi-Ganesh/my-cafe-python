import json
import random

from django.db import migrations


def generate_id(e, index):
    if not e.id:
        e.id = "{}{:07d}".format('UI', index)


def load_employee(apps, schema_editor):
    employee_model = apps.get_model('employee', 'Employee')
    json_data = open('employee/migrations/data/employee.json')
    employees = json.load(json_data)

    emp_list = []
    for index, employee in enumerate(employees):
        e = employee_model(name=employee.get("name")[:10],
                           email_address=employee.get("email"),
                           phone_number=employee.get("phone_number"),
                           gender=employee.get("gender"))
        generate_id(e, index)
        emp_list.append(e)

    saved_employees = employee_model.objects.bulk_create(emp_list)

    employee_cafe_model = apps.get_model('cafe', 'EmployeeCafe')
    cafe_model = apps.get_model('cafe', 'Cafe')
    emp_cafe_list = []
    for employee in saved_employees[:15]:
        cafe_ids = list(cafe_model.objects.all().values_list('id', flat=True))
        emp_cafe_list.append(
            employee_cafe_model(employee=employee, cafe_id=random.choice(cafe_ids)))
    employee_cafe_model.objects.bulk_create(emp_cafe_list)


class Migration(migrations.Migration):
    dependencies = [
        ('employee', '0002_alter_employee_phone_number'),
        ('cafe', '0002_load_cafe'),
    ]

    operations = [
        migrations.RunPython(load_employee),
    ]
