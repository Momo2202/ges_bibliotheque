from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from apps.members.models import Member
from apps.members.serializers import MemberSerializer


class MemberListCreateView(ListCreateAPIView):
    """
    Permet de lister les membres et d'en créer de nouveaux.
    """

    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class MemberDetailView(RetrieveUpdateDestroyAPIView):
    """
    Permet de consulter, modifier et supprimer un membre.
    """

    queryset = Member.objects.all()
    serializer_class = MemberSerializer
