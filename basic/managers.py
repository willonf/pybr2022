from django.db.models import Manager, ExpressionWrapper, Sum, FloatField, F
from django.db.models.functions import ExtractYear, ExtractMonth


# TODO: Manager customizado.
# Deve ser associado ao manager do model especificado
class SaleItemManager(Manager):
    def sold_by_year(self):
        return self.get_queryset().values(
            'sale__date__year'
        ).annotate(
            subtotal=Sum(ExpressionWrapper(F('quantity') * F('product__sale_price'), output_field=FloatField())),
            year=F('sale__date__year')
        ).values(
            'year', 'subtotal'
        ).order_by('-year')


class SaleManager(Manager):

    def actives(self):
        return self.get_queryset().filter(active=True)

    def by_year(self):
        return self.get_queryset().prefetch_related('saleitem_set').annotate(
            year=ExtractYear('date'),
            month=ExtractMonth('date'),
        ).values('year', 'month').annotate(
            total=Sum(ExpressionWrapper(
                F('saleitem__quantity') * F('saleitem__product__sale_price'),
                output_field=FloatField()
            )),
        ).values('year', 'month', 'total').order_by('-year', '-month')
