import django_filters
from .models import Categorie

class CategorieFilter(django_filters.FilterSet):
    nom=django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model=Categorie
        fields=['nom']