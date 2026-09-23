from rest_framework import viewsets

from .models import Client
from .filters import ClientFilter
from .serializers import ClientSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset=Client.objects.all()
    serializer_class=ClientSerializer
    filterset_class=ClientFilter
    search_fields=['nom','prenom','email','telephone','numero_permis']
    ordering_fields=['nom','prenom','created_at']
    ordering=['nom','prenom']
