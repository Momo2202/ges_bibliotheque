from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from apps.authors.models import Author
from apps.authors.serializers import AuthorSerializer


class AuthorListCreateView(ListCreateAPIView):
    """
    Permet de lister les auteurs et d'en créer un nouveau
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetailView(RetrieveUpdateDestroyAPIView):
    """
    Permet de consulter, modifier et supprimer un auteur.
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
