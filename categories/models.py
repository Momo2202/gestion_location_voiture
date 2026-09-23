from django.db import models

class Categorie(models.Model):
    nom=models.CharField(max_length=100,unique=True)
    description=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'categories'
        ordering=['nom']
        verbose_name = 'Categorie'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.nom
