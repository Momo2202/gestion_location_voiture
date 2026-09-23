from rest_framework import serializers
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Client
        fields=[
            'id',
            'nom',
            'prenom',
            'email',
            'telephone',
            'adresse',
            'numero_permis',
            'actif',
            'created_at',
            'updated_at'
        ]
        read_only_fields=['id','created_at','updated_at']
        
        
    def validate_telephone(self,value):
        if not value.isdigit() or len(value)<8:
            raise serializers.ValidationError("Le telephone doit contenir 8 chiffres")
        return value