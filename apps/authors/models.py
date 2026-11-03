from django.db import models

from apps.core.models import BaseModel


class Author(BaseModel):
    first_name = models.CharField(
        max_length=100,
        verbose_name="Prénom",
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name="Nom",
    )
    biography = models.TextField(blank=True, null=True, verbose_name="Biographie")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Date de Naissance")
    nationality = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Nationalité"
    )

    class Meta:
        verbose_name = "Auteur"
        verbose_name_plural = "Auteurs"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
