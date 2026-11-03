# Create your views here.
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from apps.categories.models import Category
from apps.categories.serializers import CategorySerializer


class CategoryListCreateView(ListCreateAPIView):
    """
    Vue permettant de lister et créer les catégories
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    """
    Vue permettant de consulter , modifier et supprimer une
    categorie a partir de son indentifiant
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
