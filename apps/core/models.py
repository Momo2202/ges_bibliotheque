from django.db import models


# Create your models here.
class BaseModel(models.Model):
    """
    Modele abstrait contenant les champs
    communs aux modeles metier de l'application
    """

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de creation")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de Modification")

    class Meta:
        abstract = True
