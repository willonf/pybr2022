from rest_framework import serializers


class ZoneParamsSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)


class EmployeeParamsSerializer(serializers.Serializer):
    increase = serializers.DecimalField(max_digits=5, decimal_places=2)
