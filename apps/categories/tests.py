# Create your tests here.

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.categories.models import Category


class CategoryAPITestCase(APITestCase):
    """Tests automatisés des opérations CRUD de l'API Categories."""

    def setUp(self):
        self.category = Category.objects.create(
            name="Informatique",
            description="Programmation et technologies.",
        )

        self.list_url = reverse("categories:category-list-create")

        self.detail_url = reverse(
            "categories:category-detail",
            kwargs={"pk": self.category.pk},
        )

        self.valid_payload = {
            "name": "Littérature",
            "description": "Romans et œuvres littéraires.",
        }

    def test_create_category(self):
        response = self.client.post(
            self.list_url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(response.data["name"], "Littérature")

    def test_list_categories(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_category(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Informatique")

    def test_update_category(self):
        response = self.client.put(
            self.detail_url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.category.refresh_from_db()

        self.assertEqual(self.category.name, "Littérature")
        self.assertEqual(
            self.category.description,
            "Romans et œuvres littéraires.",
        )

    def test_partial_update_category(self):
        payload = {"description": "Livres de programmation."}

        response = self.client.patch(
            self.detail_url,
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.category.refresh_from_db()

        self.assertEqual(
            self.category.description,
            "Livres de programmation.",
        )
        self.assertEqual(self.category.name, "Informatique")

    def test_delete_category(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)

    def test_create_category_with_empty_name(self):
        payload = {
            "name": "",
            "description": "Description de test.",
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Category.objects.count(), 1)

    def test_create_category_with_duplicate_name(self):
        payload = {
            "name": "Informatique",
            "description": "Une autre description.",
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Category.objects.count(), 1)

    def test_retrieve_nonexistent_category(self):
        url = reverse(
            "categories:category-detail",
            kwargs={"pk": 999999},
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
