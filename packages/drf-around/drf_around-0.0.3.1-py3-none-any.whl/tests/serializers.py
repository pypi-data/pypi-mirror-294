from rest_framework import serializers
from src.drf_around.serializers import AnnotationsAsFieldsMixin

from .models import Author


class AuthorSerializer(AnnotationsAsFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class ContainsASerializer(AnnotationsAsFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

    queryset = Author.contains_a.all()
