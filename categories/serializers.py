from rest_framework import serializers

from .models import Categorie



class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model=Categorie
        fields=['id','nom','description','created_at','updated_at']
        read_only_fields=['id','created_at','updated_at']