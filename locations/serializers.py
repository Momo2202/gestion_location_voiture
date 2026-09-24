from datetime import date

from rest_framework import serializers
from clients.serializers import ClientSerializer
from voitures.serializers import VoitureSerializer
from .models import Location


class LocationReadSerializer(serializers.ModelSerializer):
    client=ClientSerializer(read_only=True)
    voiture=VoitureSerializer(read_only=True)
    class Meta:
        model=Location
        fields=[
            'id',
            'client',
            'voiture',
            'date_debut',
            'date_fin',
            'prix_total',
            'created_at',
            'updated_at'
        ]

class LocationWriteSerializer(serializers.ModelSerializer):
    client_id=serializers.IntegerField(write_only=True)
    voiture_id=serializers.IntegerField(write_only=True)
    class Meta:
        model=Location
        fields=[
            'id',
            'client_id',
            'voiture_id',
            'date_debut',
            'date_fin',
            'statut',
            'created_at',
            'updated_at'
        ]
        read_only_fields=['id','prix_total','created_at','updated_at']
        
        
    def validate(self, attrs):
        client_id=attrs.get('client_id')
        voiture_id=attrs.get('voiture_id')
        date_debut=attrs.get('date_debut')
        date_fin=attrs.get('date_fin')
        
        from clients.models import Client
        from voitures.models import Voiture
        
        #1.Client existe et est actif
        try:
            client=Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            raise serializers.ValidationError({'client_id':"Client Introuvable"})
        if not client.actif:
            raise serializers.ValidationError({
                'client_id':"Ce client est inactif et ne peut pas louer"
            })
            
        #2 Voiture existe
        try:
            voiture=Voiture.objects.get(id=voiture_id)
        except Voiture.DoesNotExist:
            raise serializers.ValidationError({'voiture_id':"Voiture introuvable"})
        
        #3 Voiture pas en maintenance
        if voiture.statut=='maintenance':
            raise serializers.ValidationError({
                'voiture_id':'Cette voiture est en maintenance'
            })
            
        if date_debut and date_fin and date_fin<= date_debut:
            raise serializers.ValidationError({
                'date_fin':"La date de fin doit etre apres la date de debut"
            })
        
        #5. Pas de chevauchement
        if date_debut and date_fin:
            chevauchement=Location.objects.filter(
                voiture_id=voiture_id,
                statut__in=['en_attente','en_cours'],
                date_debut__lt=date_fin,
                date_fin__gt=date_debut
            )
            if self.instance:
                chevauchement=chevauchement.exclude(id=self.instance.id)
                
            if chevauchement.exists():
                raise serializers.ValidationError({
                    'voiture_id':'Cette voiture est deja loué sur cette periode'
                })
            return attrs
    
    def create(self,validated_data):
        from clients.models import Client
        from voitures.models import Voiture
        client=Client.objects.get(id=validated_data.pop('client_id'))
        voiture=Voiture.objects.get(id=validated_data.pop('voiture_id'))
        
        location=Location.objects.create(
            client=client,
            voiture=voiture,
            **validated_data
        )
        
        voiture.statut='louee',
        voiture.save()
        return location
    
    def update(self,instance,validated_data):
        from clients.models import Client
        from voitures.models import Voiture
        if 'client_id' in validated_data:
            instance.client=Client.objects.get(id=validated_data.pop('client_id'))
        if 'voiture_id' in validated_data:
            instance.voiture=Voiture.objects.get(id=validated_data.pop('voiture_id'))
            
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
            
        instance.save()
        return instance