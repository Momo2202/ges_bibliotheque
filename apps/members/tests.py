from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.members.models import Member


class MemberAPITestCase(APITestCase):
    def setUp(self):
        self.member = Member.objects.create(
            first_name="Mohamed",
            last_name="DICKO",
            email="mohamed@example.com",
            phone="+22371939656",
            address="Bamako",
        )

        self.list_url = reverse("members:member-list-create")
        self.detail_url = reverse(
            "members:member-detail",
            kwargs={"pk": self.member.pk},
        )

        self.valid_payload = {
            "first_name": "Amadou",
            "last_name": "TRAORE",
            "email": "amadou@example.com",
            "phone": "+22370000000",
            "address": "Sikasso",
        }

    def test_create_member(self):
        response = self.client.post(
            self.list_url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Member.objects.count(), 2)
        self.assertEqual(response.data["first_name"], "Amadou")

    def test_list_members(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_member(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "mohamed@example.com")

    def test_update_member(self):
        response = self.client.put(
            self.detail_url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Amadou")
        self.assertEqual(response.data["last_name"], "TRAORE")

    def test_partial_update_member(self):
        response = self.client.patch(
            self.detail_url,
            {"phone": "+22376000000"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone"], "+22376000000")
        self.assertEqual(response.data["first_name"], "Mohamed")

    def test_delete_member(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Member.objects.filter(pk=self.member.pk).exists())

    def test_duplicate_email_is_rejected(self):
        payload = self.valid_payload.copy()
        payload["email"] = "mohamed@example.com"

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_email_is_rejected(self):
        payload = self.valid_payload.copy()
        payload["email"] = "adresse-invalide"

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_first_name_is_rejected(self):
        payload = self.valid_payload.copy()
        payload.pop("first_name")

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_last_name_is_rejected(self):
        payload = self.valid_payload.copy()
        payload.pop("last_name")

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_nonexistent_member(self):
        url = reverse(
            "members:member-detail",
            kwargs={"pk": 999999},
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
