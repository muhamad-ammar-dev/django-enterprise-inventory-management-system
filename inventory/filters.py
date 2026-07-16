import django_filters
from .models import *

class StockFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Stock
        fields = ['name', 'quantity']

        