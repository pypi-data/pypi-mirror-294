from drf_around.permissions import IsRelatedToUserOrReadOnly
from drf_around.viewsets import PopulateDataMixin

from rest_framework.viewsets import ModelViewSet

from .serializers import AuthorSerializer
from .models import Author


class AuthorViewSetWithIsRelatedToUserPermission(ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def get_permissions(self):
        permissions = super().get_permissions()
        return permissions + [IsRelatedToUserOrReadOnly("user")]


class AuthorViewSet(PopulateDataMixin, ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def get_populated_data(self):
        return {"user": self.request.user.pk}
