from rest_framework import serializers

from cafe.models import EmployeeCafe, Cafe
from employee.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    cafe_id = serializers.UUIDField(required=False)

    def create(self, validated_data: dict):
        cafe_id = validated_data.pop("cafe_id", None)
        print(validated_data)
        employee = Employee.objects.create(**validated_data)
        if cafe_id is not None:
            if Cafe.objects.filter(id=cafe_id).exists():
                EmployeeCafe.objects.create(cafe_id=cafe_id, employee=employee)
            else:
                raise serializers.ValidationError(
                    "Cafe does not exist to assign employee. "
                    "Please leave cafe blank or assign the correct id")
        return employee

    def to_representation(self, instance: Employee):
        data = super().to_representation(instance)
        employee_cafe = getattr(instance, "employee_cafe", None)
        data.update(
            {"cafe_id": employee_cafe.cafe_id if employee_cafe is not None else None})
        return data

    class Meta:
        model = Employee
        fields = ["id", "name", "email_address", "phone_number", "gender", "cafe_id"]
        read_only_fields = ["id"]


class EmployeeUpdateSerializer(serializers.ModelSerializer):
    cafe_id = serializers.UUIDField(required=False)

    def update(self, employee, validated_data):
        cafe_id = validated_data.pop("cafe_id", None)
        print(validated_data)
        for item, value in validated_data.items():
            setattr(employee, item, value)
        employee.save()
        if cafe_id is not None:
            print(cafe_id)
            if Cafe.objects.filter(id=cafe_id).exists():
                print("cafe exists")
                if EmployeeCafe.objects.filter(employee=employee).exists():
                    EmployeeCafe.objects.filter(employee=employee).delete()
                    print("deleting previous cafe")
                EmployeeCafe.objects.create(cafe_id=cafe_id, employee=employee)
                print("added new cafe")
            else:
                raise serializers.ValidationError(
                    "Cafe does not exist to assign employee. "
                    "Please leave cafe blank or assign the correct id")
        return employee

    def to_representation(self, instance: Employee):
        data = super().to_representation(instance)
        employee_cafe = getattr(instance, "employee_cafe", None)
        data.update(
            {"cafe_id": employee_cafe.cafe_id if employee_cafe is not None else None})
        return data

    class Meta:
        model = Employee
        fields = ["id", "name", "email_address", "phone_number", "gender", "cafe_id"]


class EmployeeListSerializer(serializers.ModelSerializer):
    cafe = serializers.SerializerMethodField()
    days_worked = serializers.DecimalField(max_digits=10, decimal_places=4)

    def get_cafe(self, obj: Employee):
        employee_cafe = getattr(obj, "employee_cafe", None)
        if employee_cafe is not None:
            return employee_cafe.cafe.name
        return None

    class Meta:
        model = Employee
        fields = ["id", "name", "email_address", "phone_number", "gender", "cafe",
                  "days_worked"]
