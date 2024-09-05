from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
import json

from .models import Author


User = get_user_model()


class PopulateDataMixinTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first_owner = User.objects.create_user(
            "first-owner", password="not-secure345"
        )
        cls.second_owner = User.objects.create_user(
            "second-owner", password="not-secure345"
        )

        cls.list_url = reverse("author-list")

        cls.author = Author.objects.create(
            first_name="John",
            last_name="May",
            user=cls.first_owner,
        )
        cls.detail_url = reverse("author-detail", kwargs={"pk": cls.author.pk})
        return super().setUpTestData()

    def test_write_request(self):
        self.client.force_login(self.first_owner)
        data = {"first_name": "Aurora", "last_name": "May"}
        response = self.client.post(
            self.list_url,
            data=json.dumps(data),
            content_type="application/json",
        )
        pk = response.json()["id"]
        author = Author.objects.get(pk=pk)
        self.assertEqual(author.user, self.first_owner)

    def test_update_request(self):
        self.client.force_login(self.second_owner)
        data = {"last_name": "September"}
        response = self.client.patch(
            self.detail_url,
            data=json.dumps(data),
            content_type="application/json",
        )
        pk = response.json()["id"]
        author = Author.objects.get(pk=pk)
        self.assertEqual(author.user, self.second_owner)
