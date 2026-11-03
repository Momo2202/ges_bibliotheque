from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from apps.books.models import Book
from apps.books.serializers import BookSerializer


class BookListCreateView(ListCreateAPIView):
    """
    Permet de consulter la liste des livres
    et d'enregistrer un nouveau livre.
    """

    queryset = Book.objects.select_related(
        "author",
        "category",
    ).all()
    serializer_class = BookSerializer


class BookDetailView(RetrieveUpdateDestroyAPIView):
    """
    Permet de consulter, modifier et supprimer
    un livre à partir de son identifiant.
    """

    queryset = Book.objects.select_related(
        "author",
        "category",
    ).all()
    serializer_class = BookSerializer
