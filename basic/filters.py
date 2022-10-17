from django.db.models import Q, OuterRef, Exists
from django_filters import filterset
from django_filters.widgets import BooleanWidget

from basic import models


# TODO: Filtros
# Filtro in
class NumberInFilter(filterset.BaseInFilter, filterset.NumberFilter):
    pass


class CharInFilter(filterset.BaseInFilter, filterset.CharFilter):
    pass


# Filtro por range
class NumberRangeFilter(filterset.BaseRangeFilter, filterset.NumberFilter):
    pass


class ZoneFilter(filterset.FilterSet):
    name = filterset.CharFilter(lookup_expr='icontains')
    # BooleanWidget faz a conversão entre valores json e python: true (json) para True(python)
    active = filterset.BooleanFilter(widget=BooleanWidget)

    class Meta:
        model = models.Zone
        # Lookup expression padrão = exact. Nesse caso, estamos sobrescrevendo os filtros name e active
        fields = ['name', 'active', 'id']


class EmployeeFilter(filterset.FilterSet):
    name_or_department = filterset.CharFilter(method='filter_name_or_department')
    start_salary = filterset.NumberFilter(field_name='salary', lookup_expr='gte')
    end_salary = filterset.NumberFilter(field_name='salary', lookup_expr='lte')

    salary_range = NumberRangeFilter(field_name='salary', lookup_expr='range')
    # Na request: .../?salary_range=1000,2000 (entre 1000 e 2000)

    salary_in = NumberInFilter(field_name='salary', lookup_expr='range')
    # Na request: .../?salary_in=1000,2000 (salário igual a 1000 ou 2000)

    gender_in = CharInFilter(field_name='gender', lookup_expr='in')

    # Na request: .../?gender_in=m,f

    @staticmethod
    def filter_name_or_department(queryset, name, value):
        # queryset: queryset do viewset que invoca a classe de filtro
        # name: nome do filtro
        # value: dado oriundo da requisição
        # Sendo assim já podemos usar a queryset padrão do viewset para busca
        return queryset.filter(Q(name__icontains=value) | Q(department__name__icontains=value))

    class Meta:
        model = models.Employee
        fields = ['name_or_department', 'start_salary', 'end_salary', 'salary_range', 'salary_in', 'gender_in']


class ProductiFilter(filterset.FilterSet):
    exists_sale = filterset.BooleanFilter(widget=BooleanWidget, method='filter_exists_sale')

    @staticmethod
    def filter_exists_sale(queryset, name, value):
        subquery = models.SaleItem.objects.filter(product=OuterRef('id'))
        return queryset.annotate(exists=Exists(subquery)).filter(exists=value)

    class Meta:
        models = models.Product
        fields = ['exists_sale']
