from datetime import date, timedelta

from django.db.models import Count, Sum, Q
from django.db.models.functions import TruncMonth
from rest_framework.response import Response
from rest_framework.views import APIView

from clients.models import Client
from locations.models import Location
from voitures.models import Voiture


class StatsGlobalesView(APIView):
    """KPI globaux du système."""

    def get(self, request):
        total_voitures = Voiture.objects.count()
        total_clients = Client.objects.count()
        total_locations = Location.objects.count()

        locations_en_cours = Location.objects.filter(statut='en_cours').count()
        locations_en_attente = Location.objects.filter(statut='en_attente').count()
        locations_terminees = Location.objects.filter(statut='terminee').count()
        locations_annulees = Location.objects.filter(statut='annulee').count()

        chiffre_affaires = Location.objects.filter(
            statut__in=['en_cours', 'terminee']
        ).aggregate(total=Sum('prix_total'))['total'] or 0

        voitures_disponibles = Voiture.objects.filter(statut='disponible').count()
        voitures_louees = Voiture.objects.filter(statut='louee').count()
        voitures_maintenance = Voiture.objects.filter(statut='maintenance').count()

        return Response({
            'total_voitures': total_voitures,
            'total_clients': total_clients,
            'total_locations': total_locations,
            'locations_en_cours': locations_en_cours,
            'locations_en_attente': locations_en_attente,
            'locations_terminees': locations_terminees,
            'locations_annulees': locations_annulees,
            'chiffre_affaires': float(chiffre_affaires),
            'voitures_disponibles': voitures_disponibles,
            'voitures_louees': voitures_louees,
            'voitures_maintenance': voitures_maintenance,
        })


class RevenusParMoisView(APIView):
    """Chiffre d'affaires par mois sur les 12 derniers mois."""

    def get(self, request):
        douze_mois = date.today() - timedelta(days=365)

        revenus = (
            Location.objects
            .filter(
                statut__in=['en_cours', 'terminee'],
                date_debut__gte=douze_mois,
            )
            .annotate(mois=TruncMonth('date_debut'))
            .values('mois')
            .annotate(total=Sum('prix_total'), nb_locations=Count('id'))
            .order_by('mois')
        )

        resultat = [
            {
                'mois': item['mois'].strftime('%Y-%m'),
                'total': float(item['total'] or 0),
                'nb_locations': item['nb_locations'],
            }
            for item in revenus
        ]

        return Response(resultat)


class TauxOccupationView(APIView):
    """Taux d'occupation : pourcentage de voitures louées vs total."""

    def get(self, request):
        total = Voiture.objects.count()
        louees = Voiture.objects.filter(statut='louee').count()
        taux = (louees / total * 100) if total > 0 else 0

        # Détail par catégorie
        par_categorie = (
            Voiture.objects
            .values('categorie__id', 'categorie__nom')
            .annotate(
                total=Count('id'),
                louees=Count('id', filter=Q(statut='louee')),
            )
        )

        categories = [
            {
                'categorie_id': item['categorie__id'],
                'categorie_nom': item['categorie__nom'],
                'total_voitures': item['total'],
                'voitures_louees': item['louees'],
                'taux_occupation': round(item['louees'] / item['total'] * 100, 2) if item['total'] else 0,
            }
            for item in par_categorie
        ]

        return Response({
            'total_voitures': total,
            'voitures_louees': louees,
            'taux_occupation_global': round(taux, 2),
            'par_categorie': categories,
        })


class TopVoituresView(APIView):
    """Top 5 des voitures les plus louées."""

    def get(self, request):
        top = (
            Location.objects
            .values(
                'voiture__id',
                'voiture__immatriculation',
                'voiture__marque',
                'voiture__modele',
            )
            .annotate(nb_locations=Count('id'), revenus=Sum('prix_total'))
            .order_by('-nb_locations')[:5]
        )

        resultat = [
            {
                'voiture_id': item['voiture__id'],
                'immatriculation': item['voiture__immatriculation'],
                'marque': item['voiture__marque'],
                'modele': item['voiture__modele'],
                'nb_locations': item['nb_locations'],
                'revenus': float(item['revenus'] or 0),
            }
            for item in top
        ]

        return Response(resultat)


class TopClientsView(APIView):
    """Top 5 des clients les plus actifs."""

    def get(self, request):
        top = (
            Location.objects
            .values(
                'client__id',
                'client__nom',
                'client__prenom',
                'client__email',
            )
            .annotate(nb_locations=Count('id'), total_depense=Sum('prix_total'))
            .order_by('-nb_locations')[:5]
        )

        resultat = [
            {
                'client_id': item['client__id'],
                'nom': item['client__nom'],
                'prenom': item['client__prenom'],
                'email': item['client__email'],
                'nb_locations': item['nb_locations'],
                'total_depense': float(item['total_depense'] or 0),
            }
            for item in top
        ]

        return Response(resultat)


class LocationsRecentesView(APIView):
    """10 dernières locations créées."""

    def get(self, request):
        locations = (
            Location.objects
            .select_related('client', 'voiture')
            .order_by('-created_at')[:10]
        )

        resultat = [
            {
                'id': loc.id,
                'client': f"{loc.client.prenom} {loc.client.nom}",
                'voiture': f"{loc.voiture.marque} {loc.voiture.modele}",
                'immatriculation': loc.voiture.immatriculation,
                'date_debut': loc.date_debut,
                'date_fin': loc.date_fin,
                'prix_total': float(loc.prix_total),
                'statut': loc.statut,
                'created_at': loc.created_at,
            }
            for loc in locations
        ]

        return Response(resultat)