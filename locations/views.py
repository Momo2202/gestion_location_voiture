from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import LocationFilter
from .models import Location
from .serializers import LocationReadSerializer, LocationWriteSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.select_related('client', 'voiture').all()
    filterset_class = LocationFilter
    search_fields = [
        'client__nom', 'client__prenom',
        'voiture__marque', 'voiture__modele', 'voiture__immatriculation',
    ]
    ordering_fields = ['date_debut', 'date_fin', 'prix_total', 'created_at']
    ordering = ['-date_debut']

    def get_serializer_class(self):
        """Utilise WriteSerializer pour create/update, ReadSerializer sinon."""
        if self.action in ['create', 'update', 'partial_update']:
            return LocationWriteSerializer
        return LocationReadSerializer

    def get_serializer(self, *args, **kwargs):
        """
        Pour la réponse après création/modification, on renvoie les données
        en lecture (client + voiture imbriqués).
        """
        if self.action in ['create', 'update', 'partial_update']:
            kwargs['context'] = self.get_serializer_context()
            write_serializer = LocationWriteSerializer(*args, **kwargs)
            return write_serializer
        return super().get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = LocationWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        location = serializer.save()

        # On renvoie la version "read"
        read_serializer = LocationReadSerializer(location)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = LocationWriteSerializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        location = serializer.save()

        read_serializer = LocationReadSerializer(location)
        return Response(read_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='annuler')
    def annuler(self, request, pk=None):
        """Annule une location et remet la voiture en disponible."""
        location = self.get_object()

        if location.statut in ['terminee', 'annulee']:
            return Response(
                {'detail': "Cette location ne peut plus être annulée."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        location.statut = 'annulee'
        location.save()

        # Remettre la voiture disponible
        voiture = location.voiture
        voiture.statut = 'disponible'
        voiture.save()

        return Response(LocationReadSerializer(location).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='terminer')
    def terminer(self, request, pk=None):
        """Termine une location et remet la voiture en disponible."""
        location = self.get_object()

        if location.statut != 'en_cours' and location.statut != 'en_attente':
            return Response(
                {'detail': "Cette location ne peut pas être terminée."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        location.statut = 'terminee'
        location.save()

        voiture = location.voiture
        voiture.statut = 'disponible'
        voiture.save()

        return Response(LocationReadSerializer(location).data, status=status.HTTP_200_OK)