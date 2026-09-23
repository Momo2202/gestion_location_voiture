from django.contrib import admin

# Register your models here.
from .models import Voiture

@admin.register(Voiture)
class VoitureAdmin(admin.ModelAdmin):
    list_display=('immatriculation','marque','modele','categorie','prix_journalier')
    list_filter=('categorie',)
    search_fields=('immatriculation','marque','modele')
    ordering=('marque','modele')