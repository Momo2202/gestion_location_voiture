from rest_framework import viewsets

from .models import Categorie
from .serializers import CategorieSerializer
from .filters import CategorieFilter

class CategorieViewSet(viewsets.ModelViewSet):
    queryset=Categorie.objects.all()
    serializer_class=CategorieSerializer
    filterset_class=CategorieFilter
    search_fields=['nom','description']
    ordering_fields=['nom','created_at']
    ordering=['nom']