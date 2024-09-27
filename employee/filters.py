from django_filters import rest_framework as filters

from employee.models import Employee


class EmployeeFilter(filters.FilterSet):
    cafe = filters.UUIDFilter(field_name="employee_cafe__cafe_id")

    class Meta:
        model = Employee
        fields = ['cafe']
