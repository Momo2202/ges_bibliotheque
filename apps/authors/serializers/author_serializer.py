from rest_framework import serializers

from apps.authors.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer permettant de convertir et valider
    les données du modele Author
    """

    class Meta:
        model = Author

        fields = [
            "id",
            "first_name",
            "last_name",
            "biography",
            "birth_date",
            "nationality",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
