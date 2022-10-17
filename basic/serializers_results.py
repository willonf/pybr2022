from rest_framework import serializers


class SoldByYearSerializer(serializers.Serializer):
    year = serializers.IntegerField(read_only=True)
    subtotal = serializers.DecimalField(read_only=True, max_digits=16, decimal_places=3)

# class SoldByYearSerializer(serializers.Serializer):
    # O source abaixo indica para qual campo a variável 'year' (que vai na response) vai apontar
#     year = serializers.IntegerField(read_only=True, source='sale__date__year')
#     subtotal = serializers.DecimalField(read_only=True, max_digits=16, decimal_places=3)

class GetZoneByNameSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
