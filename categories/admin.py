from django.contrib import admin

from categories.models import Categorie

# Register your models here.
@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display=('nom','created_at')
    search_fields=('nom',)
    ordering=('nom',)