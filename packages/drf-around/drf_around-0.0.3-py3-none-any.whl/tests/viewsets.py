from src.drf_around.permissions import IsRelatedToUserOrReadOnly

from rest_framework.viewsets import ModelViewSet

from .serializers import AuthorSerializer
from .models import Author


class AuthorViewSet(ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def get_permissions(self):
        permissions = super().get_permissions()
        return permissions + [IsRelatedToUserOrReadOnly("user")]
