import django_filters
from .models import Voiture

class VoitureFilter(django_filters.FilterSet):
    marque=django_filters.CharFilter(lookup_expr='icontains')
    modele=django_filters.CharFilter(lookup_expr='icontains')
    annee_min=django_filters.NumberFilter(field_name='annee',lookup_expr='gte')
    annee_max=django_filters.NumberFilter(field_name='annee',lookup_expr='lte')
    prix_min=django_filters.NumberFilter(field_name='prix_journalier',lookup_expr='gte')
    prix_max=django_filters.NumberFilter(field_name='prix_journalier',lookup_expr='lte')
    class Meta:
        model:Voiture
        fields=['Categorie','statut','marque','modele']