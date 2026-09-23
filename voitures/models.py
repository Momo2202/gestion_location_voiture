from django.db import models


from categories.models import Categorie

class Voiture(models.Model):
    STATUT_CHOICES=[
        ('disponible','DISPONIBLE'),
        ('louee','Louée'),
        ('maintenance','En maintenance')
    ]
    immatriculation=models.CharField(max_length=20,unique=True)
    marque=models.CharField(max_length=50)
    modele=models.CharField(max_length=50)
    annee=models.PositiveIntegerField()
    couleur=models.CharField(max_length=30,blank=True)
    categorie=models.ForeignKey(
        Categorie,
        on_delete=models.PROTECT,
        related_name='voitures'
    )
    prix_journalier=models.DecimalField(max_digits=10,decimal_places=2)
    statut=models.CharField(max_length=20,choices=STATUT_CHOICES,default='disponible')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='voitures'
        ordering=['marque','modele']
        verbose_name='Voiture'
        verbose_name_plural='Voitures'
        
    def __str__(self):
        return f"{self.marque} {self.modele} ({self.immatriculation})"
