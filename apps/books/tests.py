from django.db.models import ProtectedError
from rest_framework import status
from rest_framework.test import APITestCase

from apps.authors.models import Author
from apps.books.models import Book
from apps.categories.models import Category


class BookAPITests(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(
            first_name="Mohamed",
            last_name="Dicko",
            biography="Développeur informatique.",
            nationality="Malienne",
        )

        self.category = Category.objects.create(
            name="Informatique",
            description="Programmation et technologies.",
        )

        self.book_data = {
            "title": "Introduction à Python",
            "isbn": "9781234567890",
            "publication_year": 2025,
            "quantity": 10,
            "author_id": self.author.id,
            "category_id": self.category.id,
        }

        self.list_url = "/api/books/"

    def test_create_book(self):
        response = self.client.post(
            self.list_url,
            self.book_data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(
            response.data["title"],
            "Introduction à Python",
        )
        self.assertEqual(
            response.data["author"]["id"],
            self.author.id,
        )
        self.assertEqual(
            response.data["category"]["id"],
            self.category.id,
        )

    def test_list_books(self):
        Book.objects.create(
            title="Introduction à Python",
            isbn="9781234567890",
            quantity=10,
            author=self.author,
            category=self.category,
        )

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), 1)
        self.assertIn("author", response.data[0])
        self.assertIn("category", response.data[0])

    def test_retrieve_book_with_complete_relations(self):
        book = Book.objects.create(
            title="Introduction à Python",
            isbn="9781234567890",
            quantity=10,
            author=self.author,
            category=self.category,
        )

        response = self.client.get(
            f"{self.list_url}{book.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["author"]["first_name"],
            "Mohamed",
        )
        self.assertEqual(
            response.data["author"]["last_name"],
            "Dicko",
        )
        self.assertIn(
            "biography",
            response.data["author"],
        )
        self.assertEqual(
            response.data["category"]["name"],
            "Informatique",
        )
        self.assertIn(
            "description",
            response.data["category"],
        )

    def test_update_book(self):
        book = Book.objects.create(
            title="Ancien titre",
            isbn="9781234567890",
            quantity=5,
            author=self.author,
            category=self.category,
        )

        data = {
            **self.book_data,
            "title": "Nouveau titre",
            "isbn": "9789876543210",
        }

        response = self.client.put(
            f"{self.list_url}{book.id}/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["title"],
            "Nouveau titre",
        )

    def test_partial_update_book(self):
        book = Book.objects.create(
            title="Introduction à Python",
            isbn="9781234567890",
            quantity=10,
            author=self.author,
            category=self.category,
        )

        response = self.client.patch(
            f"{self.list_url}{book.id}/",
            {"title": "Python avancé"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["title"],
            "Python avancé",
        )

    def test_delete_book(self):
        book = Book.objects.create(
            title="Introduction à Python",
            isbn="9781234567890",
            quantity=10,
            author=self.author,
            category=self.category,
        )

        response = self.client.delete(
            f"{self.list_url}{book.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Book.objects.filter(pk=book.id).exists(),
        )

    def test_duplicate_isbn_is_rejected(self):
        Book.objects.create(
            title="Premier livre",
            isbn="9781234567890",
            quantity=5,
            author=self.author,
            category=self.category,
        )

        response = self.client.post(
            self.list_url,
            self.book_data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_nonexistent_author_is_rejected(self):
        data = {
            **self.book_data,
            "author_id": 99999,
        }

        response = self.client.post(
            self.list_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_nonexistent_category_is_rejected(self):
        data = {
            **self.book_data,
            "category_id": 99999,
        }

        response = self.client.post(
            self.list_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_missing_title_is_rejected(self):
        data = {
            **self.book_data,
            "title": "",
        }

        response = self.client.post(
            self.list_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_nonexistent_book_returns_404(self):
        response = self.client.get(
            f"{self.list_url}99999/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_author_with_books_cannot_be_deleted(self):
        Book.objects.create(
            title="Introduction à Python",
            isbn="9781234567890",
            quantity=10,
            author=self.author,
            category=self.category,
        )

        with self.assertRaises(ProtectedError):
            self.author.delete()

    def test_category_with_books_cannot_be_deleted(self):
        Book.objects.create(
            title="Introduction à Python",
            isbn="9781234567890",
            quantity=10,
            author=self.author,
            category=self.category,
        )

        with self.assertRaises(ProtectedError):
            self.category.delete()
