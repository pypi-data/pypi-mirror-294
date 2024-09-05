from django.test import TestCase
from rest_framework.serializers import empty

from .models import Author
from .serializers import AuthorSerializer, ContainsASerializer


class AnnotationsAsFieldsTest:
    def setUp(self):
        self.get_queryset().create(**self.writable_data)
        return super().setUp()

    def get_serializer(self, instance=None, data=empty, **kwargs):
        return self.serializer_class(instance, data, **kwargs)

    def get_queryset(self):
        return self.queryset

    def _test_serializer(self, serializer):
        field = serializer.data.get("full_name", None)
        self.assertIsNotNone(field)
        self.assertEqual(field, self.annotation_data["full_name"])

    def test_read(self):
        instance = self.get_queryset().get(**self.writable_data)
        serializer = self.get_serializer(instance=instance)
        self._test_serializer(serializer)

    def test_read_after_create(self):
        serializer = self.get_serializer(data=self.writable_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self._test_serializer(serializer)

    def test_is_read_only(self):
        instance = self.get_queryset().get(**self.writable_data)
        serializer = self.get_serializer(instance=instance, data=self.annotation_data)
        serializer.is_valid()
        field = serializer.data.get("full_name", None)
        self.assertIsNone(field)


class DefaultManagerTestCase(AnnotationsAsFieldsTest, TestCase):
    writable_data = {"first_name": "Joanne", "last_name": "Rowling"}
    annotation_data = {"full_name": "Joanne Rowling"}

    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


class ContainsAManagerTestCase(AnnotationsAsFieldsTest, TestCase):
    writable_data = {"first_name": "Joanne", "last_name": "Rowling"}
    annotation_data = {"full_name": "Joanne Rowling"}

    serializer_class = ContainsASerializer
    queryset = Author.contains_a.all()
