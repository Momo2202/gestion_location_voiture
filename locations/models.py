from django.db import models

# Create your models here.
from django.core.exceptions import ValidationError
from django.db import models

from clients.models import Client
from voitures.models import Voiture

class Location(models.Model):
    STATUT_CHOICES=[
        ('en_attente','En attente'),
        ('en_cours','En Cours'),
        ('terminee','Terminée'),
        ('annulee','Annulée'),
    ]
    client=models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name='locations'
    )
    voiture=models.ForeignKey(
        Voiture,
        on_delete=models.PROTECT,
        related_name='locations'
    )
    date_debut=models.DateField()
    date_fin=models.DateField()
    prix_total=models.DecimalField(max_digits=10,decimal_places=2,blank=True)
    statut=models.CharField(max_length=20,choices=STATUT_CHOICES,default='en_attente')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='locations'
        ordering=['-date_debut']
        verbose_name='Location'
        verbose_name_plural='Locations'
    
    def __str__(self):
        return f"Location {self.id} - {self.client} / {self.voiture}"
    
    def clean(self):
        if self.date_debut and self.date_debut:
            if self.date_fin< self.date_debut:
                raise ValidationError({
                    'date_fin':"La date de fin doit etre superieur a la date de debut"
                })
                
    
    def calculer_prix(self):
        if self.date_debut and self.date_fin:
            nb__jours=(self.date_fin-self.date_debut).days
            if nb__jours <=0:
                nb__jours=1
            return nb__jours*self.voiture.prix_journalier
        return 0
    
    def save(self,*args,**kwargs):
        if self.date_debut and self.date_fin and self.voiture_id:
            self.prix_total=self.calculer_prix()
        super().save(*args, **kwargs)