from rest_framework import viewsets
from drf_spectacular.utils import extend_schema,extend_schema_view

from .models import Categorie
from .serializers import CategorieSerializer
from .filters import CategorieFilter


@extend_schema_view(
    list=extend_schema(tags=['Catégories'], summary="Liste des catégories"),
    retrieve=extend_schema(tags=['Catégories'], summary="Détail d'une catégorie"),
    create=extend_schema(tags=['Catégories'], summary="Créer une catégorie"),
    update=extend_schema(tags=['Catégories'], summary="Modifier une catégorie"),
    partial_update=extend_schema(tags=['Catégories'], summary="Modifier partiellement une catégorie"),
    destroy=extend_schema(tags=['Catégories'], summary="Supprimer une catégorie"),
)

class CategorieViewSet(viewsets.ModelViewSet):
    queryset=Categorie.objects.all()
    serializer_class=CategorieSerializer
    filterset_class=CategorieFilter
    search_fields=['nom','description']
    ordering_fields=['nom','created_at']
    ordering=['nom']
from django.shortcuts import render

# Create your views here.
