from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.authors.models import Author


class AuthorAPITestCase(APITestCase):
    """Tests automatisés des opérations CRUD de l'API Authors."""

    def setUp(self):
        self.author = Author.objects.create(
            first_name="Amadou",
            last_name="Hampâté Bâ",
            biography="Écrivain et ethnologue malien.",
            birth_date="1901-01-01",
            nationality="Malienne",
        )

        self.list_url = reverse("authors:author-list-create")
        self.detail_url = reverse(
            "authors:author-detail",
            kwargs={"pk": self.author.pk},
        )

        self.valid_payload = {
            "first_name": "Massa",
            "last_name": "Makan Diabaté",
            "biography": "Écrivain malien.",
            "birth_date": "1938-06-12",
            "nationality": "Malienne",
        }

    def test_create_author(self):
        response = self.client.post(
            self.list_url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)
        self.assertEqual(response.data["first_name"], "Massa")

    def test_list_authors(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_author(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Amadou")

    def test_update_author(self):
        response = self.client.put(
            self.detail_url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.author.refresh_from_db()

        self.assertEqual(self.author.first_name, "Massa")
        self.assertEqual(self.author.last_name, "Makan Diabaté")

    def test_partial_update_author(self):
        payload = {"nationality": "Malienne"}

        response = self.client.patch(
            self.detail_url,
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.author.refresh_from_db()

        self.assertEqual(self.author.nationality, "Malienne")
        self.assertEqual(self.author.first_name, "Amadou")

    def test_delete_author(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)

    def test_create_author_with_invalid_data(self):
        invalid_payload = {
            "first_name": "",
            "last_name": "Traoré",
        }

        response = self.client.post(
            self.list_url,
            invalid_payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Author.objects.count(), 1)
