from django.db.models import F, ExpressionWrapper, DateTimeField, IntegerField, \
    DecimalField
from django.db.models.functions import Cast
from django.utils import timezone
from django_filters import rest_framework as filters
from rest_framework import viewsets, mixins

from employee.filters import EmployeeFilter
from employee.models import Employee
from employee.serializers import EmployeeSerializer, EmployeeListSerializer, \
    EmployeeUpdateSerializer


class EmployeeViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EmployeeFilter
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        return Employee.objects.all().select_related("employee_cafe",
                                                     "employee_cafe__cafe")


class EmployeeListViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EmployeeFilter
    serializer_class = EmployeeListSerializer

    def get_queryset(self):
        queryset = Employee.objects.all().select_related("employee_cafe",
                                                         "employee_cafe__cafe")
        today = timezone.now()
        return queryset.annotate(
            microseconds=ExpressionWrapper(
                Cast(today, DateTimeField()) - F(
                    'employee_cafe__employee_start_date'),
                output_field=IntegerField()
            )
        ).annotate(
            days_worked=ExpressionWrapper(F('microseconds') / 86400000000,
                                          output_field=DecimalField())
        ).order_by('-days_worked')


class EmployeeDetailViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    serializer_class = EmployeeUpdateSerializer
    queryset = Employee.objects.all()
