from django.urls import path, include
from rest_framework import routers

from employee.views import EmployeeViewSet, EmployeeDetailViewSet, EmployeeListViewSet

app_name = "employee"

router = routers.DefaultRouter()
router.register(r"employee", EmployeeViewSet, basename='employee')
router.register(r"employees", EmployeeListViewSet, basename='employee_list')
router.register(r"employee", EmployeeDetailViewSet,
                basename='employee_detail')

urlpatterns = [
    path("", include(router.urls)),
]
