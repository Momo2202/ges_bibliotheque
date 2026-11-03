# Create your models here.
from django.db import models

from apps.authors.models import Author
from apps.categories.models import Category
from apps.core.models import BaseModel


class Book(BaseModel):
    title = models.CharField(
        max_length=255,
        verbose_name="Titre",
    )
    isbn = models.CharField(max_length=20, unique=True, verbose_name="ISBN")
    publication_year = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Description",
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name="Quantité")
    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        related_name="books",
        verbose_name="Auteur",
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="books", verbose_name="Catégorie"
    )

    class Meta:
        verbose_name = "Livre"
        verbose_name_plural = "Livres"
        ordering = ["title"]

    def __str__(self):
        return self.title
