from django.db import models

class Client(models.Model):
    nom=models.CharField(max_length=100)
    prenom=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    telephone=models.CharField(max_length=20)
    adresse=models.TextField(blank=True)
    numero_permis=models.CharField(max_length=50,unique=True)
    actif=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='clients'
        ordering=['nom','prenom']
        verbose_name='Client',
        verbose_name_plural='Clients'
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"
