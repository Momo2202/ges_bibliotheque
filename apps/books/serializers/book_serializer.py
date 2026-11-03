from rest_framework import serializers

from apps.authors.models import Author
from apps.authors.serializers import AuthorSerializer
from apps.books.models import Book
from apps.categories.models import Category
from apps.categories.serializers import CategorySerializer


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source="author",
        write_only=True,
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True,
    )

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "isbn",
            "publication_year",
            "quantity",
            "author",
            "author_id",
            "category",
            "category_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]
