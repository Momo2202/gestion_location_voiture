from rest_framework import viewsets
from .filters import VoitureFilter
from .models import Voiture
from .serializers import VoitureSerializer

class VoitureViewSet(viewsets.ModelViewSet):
    queryset=Voiture.objects.select_related('categorie').all()
    serializer_class=VoitureSerializer
    filterset_class=VoitureFilter
    search_fields=['immatriculation','marque','modele','couleur']
    ordering_fields=['marque','modele','annee','prix_journalier','created_at']
    ordering=['marque','modele']