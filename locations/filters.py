import django_filters

from .models import Location

class LocationFilter(django_filters.FilterSet):
    date_debut_min=django_filters.DateFilter(field_name='date_debut',lookup_expr='gte')
    date_debut_max=django_filters.DateFilter(field_name='date_debut',lookup_expr='lte')
    date_fin_min=django_filters.DateFilter(field_name='date_fin',lookup_expr='gte')
    date_fin_max=django_filters.DateFilter(field_name='date_fin',lookup_expr='lte')
    class Meta:
        model:Location
        fields=['statut','client','voiture']