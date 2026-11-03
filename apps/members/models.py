# Create your models here.
from django.db import models

from apps.core.models import BaseModel


class Member(BaseModel):
    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    email = models.EmailField(
        unique=True,
        verbose_name="Adresse Email",
    )
    phone = models.CharField(
        max_length=20,
        default="+223 00 00 00 00",
        verbose_name="Télephone",
    )
    address = models.TextField(blank=True, null=True, verbose_name="Adresse")
    registration_date = models.DateField(
        auto_now_add=True,
        verbose_name="Date d'inscription",
    )
    is_active = models.BooleanField(default=True, verbose_name="Membre actif")

    class Meta:
        verbose_name = "Membre"
        verbose_name_plural = "Membres"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
