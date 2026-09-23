from django.contrib import admin


from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display=('nom','prenom','email','telephone','actif','created_at')
    list_filter=('actif',)
    search_fields=('nom','prenom','email','numero_permis')
    ordering=('nom','prenom')
    

