import django_filters
from .models import Client

class ClientFilter(django_filters.FilterSet):
    nom=django_filters.CharFilter(lookup_expr='icontains')
    prenom=django_filters.CharFilter(lookup_expr='icontains')
    email=django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model:Client
        fields=['actif','nom','prenom','email']