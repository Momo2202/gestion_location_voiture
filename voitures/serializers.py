from rest_framework import serializers

from categories.models import Categorie
from categories.serializers import CategorieSerializer
from .models import Voiture


# ============================================================
# Serializer de LECTURE (GET) — catégorie imbriquée
# ============================================================
class VoitureReadSerializer(serializers.ModelSerializer):
    categorie = CategorieSerializer(read_only=True)

    class Meta:
        model = Voiture
        fields = [
            'id',
            'immatriculation',
            'marque',
            'modele',
            'annee',
            'couleur',
            'categorie',
            'prix_journalier',
            'statut',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


# ============================================================
# Serializer d'ÉCRITURE (POST/PUT/PATCH) — catégorie par ID
# ============================================================
class VoitureWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voiture
        fields = [
            'id',
            'immatriculation',
            'marque',
            'modele',
            'annee',
            'couleur',
            'categorie',
            'prix_journalier',
            'statut',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_annee(self, value):
        if value < 1900 or value > 2100:
            raise serializers.ValidationError("L'année doit être entre 1900 et 2100.")
        return value

    def validate_prix_journalier(self, value):
        if value <= 0:
            raise serializers.ValidationError("Le prix journalier doit être positif.")
        return value


# ============================================================
# Serializer PRINCIPAL — choisit automatiquement selon la méthode HTTP
# ============================================================
class VoitureSerializer(serializers.ModelSerializer):
    categorie = CategorieSerializer(read_only=True)
    categorie_id = serializers.PrimaryKeyRelatedField(
        queryset=Categorie.objects.all(),
        source='categorie',
        write_only=True,
    )

    class Meta:
        model = Voiture
        fields = [
            'id',
            'immatriculation',
            'marque',
            'modele',
            'annee',
            'couleur',
            'categorie',
            'categorie_id',
            'prix_journalier',
            'statut',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_annee(self, value):
        if value < 1900 or value > 2100:
            raise serializers.ValidationError("L'année doit être entre 1900 et 2100.")
        return value

    def validate_prix_journalier(self, value):
        if value <= 0:
            raise serializers.ValidationError("Le prix journalier doit être positif.")
        return value