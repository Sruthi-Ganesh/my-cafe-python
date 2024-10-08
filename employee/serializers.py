from rest_framework import serializers

from cafe.models import EmployeeCafe, Cafe
from cafe.serializers import EmployeeCafeSerializer
from employee.models import Employee


class EmployeeTemplateRequestSerializer(serializers.Serializer):
    class Meta:
        model = Employee
        fields = ["id", "name", "email_address", "phone_number", "gender", "cafe_id"]
        read_only_fields = ["id"]


class EmployeeTemplateResponseSerializer(serializers.Serializer):
    class Meta:
        model = Employee
        fields = ["id", "name", "email_address", "phone_number", "gender", "cafe"]
        read_only_fields = ["id", "cafe"]


class EmployeeSerializer(serializers.ModelSerializer):
    cafe_id = serializers.UUIDField(required=False, allow_null=True, write_only=True)
    cafe = EmployeeCafeSerializer(source='employee_cafe', read_only=True)

    def create(self, validated_data: dict):
        cafe_id = validated_data.pop("cafe_id", None)
        print(validated_data)
        employee = Employee.objects.create(**validated_data)
        if cafe_id:
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
            {"cafe_id": employee_cafe.cafe_id
            if employee_cafe is not None else None,
             "gender": instance.get_gender_display().upper()
             if instance.gender else None})
        return data

    class Meta:
        model = Employee
        fields = ["id", "name", "email_address", "phone_number", "gender", "cafe_id",
                  "cafe"]
        read_only_fields = ["id", "cafe"]


class EmployeeUpdateSerializer(serializers.ModelSerializer):
    cafe_id = serializers.UUIDField(required=False, allow_null=True, write_only=True)
    cafe = EmployeeCafeSerializer(source='employee_cafe', read_only=True)

    def update(self, employee, validated_data):
        cafe_id = validated_data.pop("cafe_id", None)
        print(validated_data)
        for item, value in validated_data.items():
            setattr(employee, item, value)
        employee.save()
        if cafe_id:
            if Cafe.objects.filter(id=cafe_id).exists():
                if EmployeeCafe.objects.filter(employee=employee).exists():
                    EmployeeCafe.objects.filter(employee=employee).delete()
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
            {"cafe_id": employee_cafe.cafe_id
            if employee_cafe is not None else None,
             "gender": instance.get_gender_display().upper()
             if instance.gender else None}
        )
        return data

    class Meta:
        model = Employee
        fields = ["id", "name", "email_address", "phone_number", "gender", "cafe_id",
                  "cafe"]
        read_only_fields = ["cafe"]


class EmployeeListSerializer(serializers.ModelSerializer):
    cafe = EmployeeCafeSerializer(source="employee_cafe")
    days_worked = serializers.DecimalField(max_digits=10, decimal_places=4)
    gender = serializers.SerializerMethodField()

    def get_gender(self, obj: Employee):
        return obj.get_gender_display().upper() if obj.gender else None

    class Meta:
        model = Employee
        fields = ["id", "name", "email_address", "phone_number", "gender",
                  "cafe",
                  "days_worked"]
