from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
import json

from .models import Author


User = get_user_model()


class IsUserRelatedPermissionTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user("owner", password="not-secure345")
        cls.not_owner = User.objects.create_user("not-owner", password="not-secure345")

        cls.author = Author.objects.create(
            first_name="John",
            last_name="May",
            user=cls.owner,
        )
        cls.url = reverse("author-detail", kwargs={"pk": cls.author.pk})
        return super().setUpTestData()

    def test_safe_request_without_relation(self):
        self.client.force_login(self.not_owner)
        response = self.client.get(self.url)
        self.assertTrue(status.is_success(response.status_code))

    def test_write_request_with_relation(self):
        self.client.force_login(self.owner)
        data = {"last_name": "December"}
        response = self.client.patch(
            self.url,
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertTrue(status.is_success(response.status_code))

    def test_write_request_without_relation(self):
        self.client.force_login(self.not_owner)
        data = {"last_name": "December"}
        response = self.client.patch(
            self.url,
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertTrue(status.is_client_error(response.status_code))
