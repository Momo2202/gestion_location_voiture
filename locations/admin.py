from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Location

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display=('id','client','voiture','date_debut','date_fin','prix_total','created_at')
    
    list_filter=('statut','date_debut','date_fin')
    search_fields=('client_nom','client_prenom','voiture_marque','voiture_modele','voiture_immatriculation')
    
    ordering=('-date_debut',)
    readonly_fields=('prix_total','created_at','updated_at')
    