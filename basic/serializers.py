from rest_framework import serializers
from basic import models
from rest_flex_fields import FlexFieldsModelSerializer


# TODO: Custom fields serializer
# class EmployeeSerializer(serializers.Serializer):  # TODO: Serializar mais "manual"
#     name = serializers.CharField(read_only=True)
#     district = serializers.CharField(read_only=True, source='district__name')
#     city = serializers.CharField(read_only=True, source='district__city__name')
#     state = serializers.CharField(
#         read_only=True, source='district__city__state__name')

#     class Meta:
#         model = models.Employee
#         fields = ['url', 'username', 'name']  # TODO: Campos que queremos serializar

# TODO: métodos padrões do serializer. Podem ser sobrescritos
# Geralmente, esses métodos não são sobrescritos quando serializamos utilizando o ModelSerializer
# class BranchExampleSerializer(serializers.ModelSerializer):
#
#     def validate(self, attrs):  # Camada de validação dos dados
#         return super(BranchExampleSerializer, self).validate(attrs)
#
#     def create(self, validated_data):
#         return super(BranchExampleSerializer, self).create(validated_data)
#
#     def update(self, instance, validated_data):
#         return super(BranchExampleSerializer, self).update(instance, validated_data)
#
#     def to_representation(self, instance):  # Customização de campos
#         data = super(BranchExampleSerializer, self).to_representation(instance)
#         data['new_field'] = 10 * 10
#         return data
#
#     class Meta:
#         model = models.Branch
#         fields = ['url', 'name', 'district']

class BranchSerializer(serializers.ModelSerializer):  # TODO: serializer baseado no modelo informado
    class Meta:
        model = models.Branch
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.District
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = '__all__'


class MaritalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MaritalStatus
        fields = '__all__'


class ProductGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductGroup
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sale
        fields = '__all__'


class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SaleItem
        fields = '__all__'


# class ProductListSerializer(serializers.ModelSerializer):
#     # TODO: "Expand" manual apenas para listagem
#     class Meta:
#         model = models.Product
#         fields = ['id', 'name']


class SupplierSerializer(FlexFieldsModelSerializer):  # para usar o expand, herdar FlexFieldsModelSerializer
    # class SupplierSerializer(serializers.ModelSerializer):
    # products = ProductListSerializer(source='product_set', many=True, read_only=True)
    # Para a busca acima ser performática, sobrescrever o método list() no serializer de supplier com o select_related

    class Meta:
        model = models.Supplier
        fields = '__all__'
        # O expand, por padrão não realiza os joins corretamente, causando problema de performance

    expandable_fields = {
        'product': ('basic.ProductSerializer',
                    {'source': 'product_set', 'many': True})
        # source obrigatório quando o nome do campo a ser expandido é diferente do source ('product' != 'product_set')
    }


class ProductSerializer(FlexFieldsModelSerializer):
    # class ProductSerializer(serializers.ModelSerializer):
    # TODO: "Expand" manual (entretanto, com JOIN errado na consulta)
    # Usando a forma abaixo, para cada produto na busca, ele fará outra busca para saber o supplier correspondente
    # supplier_obj = SupplierSerializer(source='supplier', read_only=True)

    class Meta:
        model = models.Product
        fields = '__all__'

    expandable_fields = {
        'product_group': ('basic.ProductGroupSerializer', )
    }


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.State
        fields = '__all__'


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Zone
        fields = '__all__'


# TODO: serializer manual
class Zone2Serializer(serializers.Serializer):
    # Campos a serem serializados:

    # Id é autoincrement, então ele será read_only
    id = serializers.IntegerField(read_only=True)
    # created_at e modified_at é gerenciado pelo Django, podendo ser read_only
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)

    active = serializers.BooleanField(required=False, default=True)
    name = serializers.CharField(required=True, max_length=64)

    # O métodos abaixo são chamados automaticamente por "debaixo dos panos"

    def validate(self, attrs):
        if not attrs.get('name').isupper():
            raise Exception('O nome deve estar em uppercase')
        return super(Zone2Serializer, self).validate(attrs)

    # Após o validate:
    def create(self, validated_data):
        # Forma 1
        # zone = models.Zone()
        # zone.name = validated_data['name']
        # zone.save()

        # Forma 2:
        return models.Zone.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Instance é objeto já cadastrado no banco
        # validated_data são os dados enviados pela request
        for key, value in validated_data.items():
            setattr(__obj=instance, __name=key, __value=value)
        instance.save()
        return instance

    # Após o create:
    # O to_representation vai pegar o objeto (instance) e serializar para JSON para enviar para o front
    def to_representation(self, instance):
        data = super(Zone2Serializer, self).to_representation(instance)
        print(data)
        return data
